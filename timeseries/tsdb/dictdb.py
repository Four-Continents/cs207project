from collections import defaultdict, OrderedDict
from operator import and_
from functools import reduce
import operator

# this dictionary will help you in writing a generic select operation
OPMAP = {
    '<': operator.lt,
    '>': operator.gt,
    '==': operator.eq,
    '!=': operator.ne,
    '<=': operator.le,
    '>=': operator.ge
}

# Not using this code
# def metafiltered(d, schema, fieldswanted):
#     d2 = {}
#     if len(fieldswanted) == 0:
#         keys = [k for k in d.keys() if k != 'ts']
#     else:
#         keys = [k for k in d.keys() if k in fieldswanted]
#     for k in keys:
#         if k in schema:
#             d2[k] = schema[k]['convert'](d[k])
#     return d2


class DictDB:
    "Database implementation in a dict"
    def __init__(self, schema, pkfield):
        "initializes database with index and schema"
        self.indexes = {}  # self.index['f']={1:[1,4], 2:[9], 3:[33]}
        self.rows = {}  # keys are pk of each row
        self.schema = schema
        self.pkfield = pkfield
        for s in schema:
            indexinfo = schema[s]['index']
            # convert = schema[s]['convert']
            # later use binary search trees for highcard/numeric
            # bitmaps for lowcard/str_or_factor
            if indexinfo is not None:
                self.indexes[s] = defaultdict(set)

    def insert_ts(self, pk, ts):
        "given a pk and a timeseries, insert them"
        if pk not in self.rows:
            self.rows[pk] = {'pk': pk}
        else:
            raise ValueError('Duplicate primary key found during insert')
        self.rows[pk]['ts'] = ts
        # should below be a coroutine so we dont block?
        self.update_indices(pk)

    def upsert_meta(self, pk, meta):
        "implement upserting field values, as long as the fields are in \
        the schema."
        if pk not in self.rows:
            raise ValueError('Insert value into DB before attempting upsert of metadata')
        for k, v in meta.items():
            if k in self.schema.keys():
                self.rows[pk][k] = v
        # your code here
        self.update_indices(pk)
        # print("S> D> ROW", self.rows[pk])

    def index_bulk(self, pks=[]):
        if len(pks) == 0:
            pks = self.rows
        for pkid in self.pks:
            self.update_indices(pkid)

    def update_indices(self, pk):
        row = self.rows[pk]
        for field in row:
            v = row[field]
            if self.schema[field]['index'] is not None:
                idx = self.indexes[field]
                idx[v].add(pk)

    def _filter_data(self, meta_variable, filter_v, sel_values):
        if isinstance(filter_v, dict):
            filtered_values = sel_values
            for _operator, operand in filter_v.items():
                filtered_values_op = set()
                filtered_indices = [x for x in list(self.indexes[meta_variable].keys())
                                    if OPMAP[_operator](x, operand)]
                for index in filtered_indices:
                    filtered_values_op = filtered_values_op | set(self.indexes[meta_variable][index])
            filtered_values = filtered_values & filtered_values_op
            return filtered_values
        else:
            return set(self.indexes[meta_variable][filter_v])

    def _sort_and_limit(self, select_keys, additional):
        select_rows = {key: self.rows[key] for key in select_keys}
        # sorting
        if additional is not None:
            if "sort_by" in additional:
                if additional["sort_by"][0] == "+":
                    isDescending = False
                else:
                    isDescending = True
                ordered_select_rows = OrderedDict(sorted(select_rows.items(),
                                                  key=lambda t:
                                                  t[1][additional["sort_by"][1:]],
                                                  reverse=isDescending))
        else:
            ordered_select_rows = select_rows
        # limiting
        if additional is not None:
            if "limit" in additional:
                select_keys_return = []
                for i in range(additional["limit"]):
                    select_keys_return.append(list(ordered_select_rows.keys())[i])
            else:
                select_keys_return = list(ordered_select_rows.keys())
        else:
            select_keys_return = list(ordered_select_rows.keys())
        return select_keys_return

    def select(self, meta, fields, additional):
        # sanity checks on sort and limit criteria
        if additional is not None:
            add_keys = additional.keys()
            if len([key for key in add_keys if key not in ["sort_by", "limit"]]) > 0:
                raise ValueError('Currently support only sort and limit operations')
            elif len(add_keys) > 2:
                raise ValueError('Currently support only one sort and one limit operation')
            elif "sort_by" in add_keys:
                if not isinstance(additional["sort_by"], str):
                    raise ValueError('Sort by field must be a string')
                if additional["sort_by"][1:] not in self.schema.keys() or \
                   self.schema[additional["sort_by"][1:]]["index"] is None:
                    raise ValueError('Sort by field %s must exist in schema with index' % additional['sort_by'][1:])
        # Apply filters
        select_values = set(self.rows.keys())
        if meta is not None:
            for meta_variable, filter_v in meta.items():
                filtered_values = self._filter_data(meta_variable, filter_v, select_values)
                select_values = select_values & filtered_values
            select_values = list(select_values)
        # sorting and limit
        select_values = self._sort_and_limit(list(select_values), additional)
        # choose fields to display
        if fields is None:
            print('S> D> NO FIELDS')
            return select_values, None
        elif len(fields) == 0:
            print('S> D> ALL FIELDS')  # except for the 'ts' field
            field_return = []
            for row in select_values:
                fields_to_pick = list(self.rows[row].keys())
                fields_to_pick.remove('ts')
                row_field = dict()
                for k in fields_to_pick:
                    row_field[k] = self.rows[row][k]
                field_return.append(row_field)
            return select_values, field_return
        else:
            print('S> D> FIELDS', fields)
            field_return = []
            for row in select_values:
                fields_to_pick = set(fields) & set(self.rows[row].keys())
                row_field = dict()
                for k in fields_to_pick:
                    row_field[k] = self.rows[row][k]
                field_return.append(row_field)
            return select_values, field_return

        # your code here
        # if fields is None: return only pks
        # like so [pk1,pk2],[{},{}]
        # if fields is [], this means all fields
        # except for the 'ts' field. Looks like
        # ['pk1',...],[{'f1':v1, 'f2':v2},...]
        # if the names of fields are given in the list, include only those fields. `ts` ia an
        # acceptable field and can be used to just return time series.
        # see tsdb_server to see how this return
        # value is used
        # additional is a dictionary. It has two possible keys:
        # (a){'sort_by':'-order'} or {'sort_by':'+order'} where order
        # must be in the schema AND have an index. (b) limit: 'limit':10
        # which will give you the top 10 in the current sort order.
        # your code here
