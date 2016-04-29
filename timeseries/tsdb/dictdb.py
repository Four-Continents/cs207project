from collections import defaultdict
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
        print("S> D> ROW", self.rows[pk])

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

    def select(self, meta, fields):
        sel_values = set(self.rows.keys())
        for meta_variable, filter_v in meta.items():
            filtered_values = self._filter_data(meta_variable, filter_v, sel_values)
            sel_values = sel_values & filtered_values
        sel_values = list(sel_values)
        if fields is None:
            print('S> D> NO FIELDS')
            return sel_values, None
        elif len(fields) == 0:
            print('S> D> ALL FIELDS')  # except for the 'ts' field
            field_return = []
            for row in sel_values:
                fields_to_pick = list(self.rows[row].keys())
                fields_to_pick.remove('ts')
                row_field = dict()
                for k in fields_to_pick:
                    row_field[k] = self.rows[row][k]
                field_return.append(row_field)
            return sel_values, field_return
        else:
            print('S> D> FIELDS', fields, sel_values)
            field_return = []
            for row in sel_values:
                fields_to_pick = set(fields) & set(self.rows[row].keys())
                row_field = dict()
                for k in fields_to_pick:
                    row_field[k] = self.rows[row][k]
                field_return.append(row_field)
            return sel_values, field_return

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
        # return pks, matchedfielddicts
