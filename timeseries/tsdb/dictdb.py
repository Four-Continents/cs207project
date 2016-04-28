from collections import defaultdict
from operator import and_
from functools import reduce


class DictDB:
    "Database implementation in a dict"
    def __init__(self, schema):
        "initializes database with indexed and schema"
        self.indexes = {}  # self.index['f']={1:[1,4], 2:[9], 3:[33]}
        self.rows = {}  # keys are pk of each row
        self.schema = schema
        self.pkfield = 'pk'
        for s in schema:
            indexinfo = schema[s]['index']
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

    def select(self, meta):
        sel_values = set(self.rows.keys())
        for meta_filter, v in meta.items():
            sel_values = sel_values & self.indexes[meta_filter][v]
        return list(sel_values)
        # implement select, AND'ing over the filters in the md metadata dict
        # remember that each item in the dictionary looks like key==value
