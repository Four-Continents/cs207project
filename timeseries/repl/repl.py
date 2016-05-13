#!/usr/bin/env python3

import cmd
import sys
from . import lexer
from . import parser
from tsdb.tsdb_client import TSDBClient
from tsdb.tsdb_error import TSDBStatus
import timeseries as ts
import json
from collections import OrderedDict
from .ast import AST_proc
import re


class REPL(cmd.Cmd):
    def __init__(self, client):
        super(REPL, self).__init__()
        self.client = client
        self.print = print
        self.parser = parser.new_parser()

    def do_hello(self, arg):
        arg_list = [a for a in arg.split(' ') if a.strip() != '']
        if len(arg_list) == 0:
            self.print('Hello!')
            return
        self.print('Hello,', ' and '.join(arg_list))

    def do_goodbye(self, arg):
        """
        Exits the REPL
        """
        # ignores arg
        self.print('Goodbye...')
        sys.exit(0)

    def do_insert(self, arg):
        """
        Inserts TimeSeries into database under 'ts' field and adds primarykey under 'pk' field

        Use Cases:
        >> insert [1, 3, 5] @ [5, 6, 7] into primarykey
          where the [5, 6, 7] are the TimeSeries timestamps and [1, 2, 3] are the TimeSeries values

        Raises Parse Error if invalid syntax
        """
        lex = lexer.new_lexer()
        ast = self.parser.parse('insert ' + arg, lexer=lex)
        if ast is None:
            self.print('Error!')
            return

        if len(ast.timestamps) != len(ast.values):
            self.print('Error! %d timestamps and %d values must be the same length'
                  % (len(ast.timestamps), len(ast.values)))
            return

        self.client.insert_ts(ast.pk.id, ts.TimeSeries(ast.timestamps.elements, ast.values.elements))

        self.print('OK!')

    def do_select(self, arg):
        """
        Returns all or selected named fields from all or selected primary keys with options to
        limit number of rows returned, sort in ascending or descending order, or run procedures on data.

        Use Cases:

        Select all primary keys from the 'ts' field:
        > select ts

        Select specific fields from all primary keys
        > select ts, pk

        Select all fields from specific primary key
        > select from primarykey

        Select specific fields from specific primary key
        > select ts, pk from primarykey

        ---------------------------------------------------------------------------------------------------

        Limit: restrict number of observations returned

        > select limit 1
        > select ts limit 2

        ---------------------------------------------------------------------------------------------------

        Order By:

        Order data in alphabetical order by primary key. Ascending order is done by default, though it is
        possible to explicitly pass "asc". To return in descending order, type "desc".
        > select ts order by primarykey
        > select ts order by pk asc
        > select ts order by pk desc

        ---------------------------------------------------------------------------------------------------

        Procs:
        Look in procs directory for available procs
        Currently supported:
            - stats(): returns means and std of TimeSeries

        >> select stats() as mean, std
        >> select stats() as mean, std from pk
        >> select stats() as mean, std limit 2
        >> select proc() as field1, field2 order by ...
        """
        lex = lexer.new_lexer()

        ast = self.parser.parse('select ' + arg, lexer=lex)
        # catch parse error condition
        if ast is None:
            self.print('Error!')
            return

        if ast.pk:
            metadata_dict = {'pk': ast.pk.id}
        else:
            metadata_dict = None

        additional = {}
        if ast.orderby:
            # + for ascending, - for descending
            if ast.ascending:
                additional['sort_by'] = '+' + ast.orderby.id
            else:
                additional['sort_by'] = '-' + ast.orderby.id

        if ast.limit is not None:
            additional['limit'] = ast.limit

        if isinstance(ast.selector, AST_proc):
            self._print_select_result(self.client.augmented_select(
                proc=ast.selector.id.id,
                target=[i.id for i in ast.selector.targets],
                metadata_dict=metadata_dict,
                additional=(additional or None))
            )
        else:
            if ast.selector:
                fields = [i.id for i in ast.selector]
            else:
                fields = []

            res = self.client.select(
                metadata_dict=metadata_dict,
                fields=fields,
                additional=(additional or None))
            self._print_select_result(res)


    def do_dump(self, arg):
        """
        prints 'ts' field for all rows in database
        """
        self._print_select_result(self.client.select(fields=['ts']))

    def do_upsert(self, arg):
        """
        Attaches metadata to an existing TimeSeries

        Use Cases:
        >> upsert ginger {"label": "cute"}

        dict keys must be strings
        """
        arg = arg.strip()

        try:
            firstbrace_idx = arg.index('{')
        except ValueError:
            self.print('Bad syntax!')
            return

        json_str = arg[firstbrace_idx:]

        try:
            d = json.loads(json_str)
        except json.decoder.JSONDecodeError:
            self.print('Bad syntax!')
            return

        pk = arg[:firstbrace_idx].strip()
        if not pk:
            self.print('Bad syntax!')
            return

        self.client.upsert_meta(pk, d)

        self.print('OK!')

    def do_delete(self, arg):
        """
        deletes row in database by primary key

        Use Cases:
        >> delete primarykey
        """
        pk = arg.strip()
        regex = lexer.t_ID.__doc__
        if not re.match(regex, pk):
            self.print('Bad syntax!')
            return

        self.client.delete(pk)
        self.print('OK!')

    def do_populate(self, arg):
        """
        Populates the database with 10 random timeseries and 5 randomly selected vantage points.
        For each timeseries, it will populate the columns representing the distance metric to each
        vantage point.
        Takes no arguments

        Use Cases:
        >> populate

        """
        if arg.strip():
            self.print('Bad syntax!')
            return

        self.client.populate_db(numElem=50, numVp=5)
        self.print('OK!')

    def do_simsearch(self, arg):
        """
        Find `k_nearest` most similar timeseries in the DB when compared to some given timeseries

        >> simsearch 3 like primarykey
        """
        lex = lexer.new_lexer()

        ast = self.parser.parse('simsearch ' + arg, lexer=lex)
        # catch parse error condition
        if ast is None:
            self.print('Error!')
            return

        res = self.client.select(
            metadata_dict={'pk': ast.pk.id},
            fields=['ts'])

        status, payload = res
        if status is not TSDBStatus.OK:
            self.print('Error! %r' % payload)
            return

        if len(payload) != 1:
            self.print('Unexpected row count! Expected 1. Received %d, \n %r' % (len(payload), payload))
            return

        row = payload[ast.pk.id]
        ts_field = row['ts']

        times = ts_field['times']
        values = ts_field['values']

        sim_pks = self.client.find_similar(ts.TimeSeries(times, values), ast.k+1)
        print('#####sim', sim_pks)
        print(ast.k)

        for pk in sorted(sim_pks):
            if pk == ast.pk.id:
                continue
            res = self.client.select(
                metadata_dict={'pk': pk},
                fields=['ts'])
            self._print_select_result(res)

    def _print_select_result(self, result):
        status, payload = result
        if status is not TSDBStatus.OK:
            self.print('Error! %r' % payload)
            return

        for key, values in payload.items():
            self.print(key)
            for vkey in sorted(values.keys()):
                vvalues = values[vkey]
                if isinstance(vvalues, OrderedDict):
                    self.print('   ', vkey)
                    for hkey in sorted(vvalues.keys()):
                        self.print('      ', hkey, ': ', vvalues[hkey])
                else:
                    self.print('   ', vkey, ': ', vvalues)


if __name__ == '__main__':
    client = TSDBClient(port=30000)
    r = REPL(client)
    # r.onecmd("insert [1,2,3] @ [4, 5, 6] into tabby")
    # r.onecmd("insert [8,9,10] @ [11, 12, 13] into ginger")
    r.cmdloop()

