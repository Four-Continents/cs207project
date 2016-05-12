#!/usr/bin/env python3

import cmd
import sys
import re
from . import lexer
from . import parser
from tsdb.tsdb_client import TSDBClient
from tsdb.tsdb_error import TSDBStatus
import timeseries as ts
import json
from collections import OrderedDict
from .ast import AST_proc


class REPL(cmd.Cmd):
    """
    TODO
    https://docs.python.org/3/library/cmd.html#cmd.Cmd.cmdloop

    - tests
    - help, docstrings for everything, error handling
    - clean up code and defensive coding checks

    - implement DELETE
    - need to be able to connect to persistent database.. should be trivial
    - implement transactions from database persistence and on the REPL side?
    - port everything over all to ply?

    - write a paragraph on what you did (a para on the architecture of the persistence, your additional part,
    and REST api)
    how to install your project, where to find the docs (for the rest api, running the server, populating the database

    - prepare demo! (ply vs. hand parsers)
      leverage from json parser - in ply would have required delimiters to wrap, then would have had to define lexer
    to understand escaping to deal with delimiters
    upsert - hand hack index and

    two approach in ply:
    1) write JSON grammar with all the productions and understand all of JSON. JSON dict and key-value pairs
    2) alternative use delimiters to send a raw string to ply, then do json loads in parser to parse everything in the
    delimiter, but then have to deal with escaping or have to specify in the docs can't include that delimiter which
    restricts users from using certain json values

    with upsert, just defined syntax to just chop off beginning and do JSON loads.

    select, helpful to have ply, because pretty complicated custom syntax
    """
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
        insert [1, 3, 5] @ [5, 6, 7] into primarykey
        where the second [] are the timestamps
        first [] are the values

        insert [1,2,3] @ [4, 5, 6] into pke
        insert [1,2] @ [3,4] into k

        insert [1,2,3] @ [4,5,6] into k

        insert abc @ [4,5,6] into pke
        Error handling!

        Parse Error: LexToken(ID,'abc',1,7)
        Error!
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
        TODO see console for command used

        look in procs directory for available procs
            - stats(): returns means and std

        select ts

        select field1, field2, field2
        select ts, pk from pke

        select from pke
        select ts from something

        select limit 1
        select ts limit 2

        select ts order by pk
        select ts order by pk desc (ascending is by default, though can also pass in explicity asc)

        select stats() as mean, std
        select stats() as mean, std from ginger
        select stats() as mean, std limit 2
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
            self.print_select_result(self.client.augmented_select(
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

            print('metadata_dict:', metadata_dict)
            res = self.client.select(
                metadata_dict=metadata_dict,
                fields=fields,
                additional=(additional or None))
            self.print_select_result(res)


    def do_dump(self, arg):
        """
        prints ts field for all rows in database
        """
        self.print_select_result(self.client.select(fields=['ts']))

    def do_upsert(self, arg):
        """
        UPSERT pk {'hi': 'bye'}

        upsert ginger {"label": "cute"}

        NOT case insensitive

        attaches metadata to an existing TimeSeries
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


    def print_select_result(self, result):
        """
        :param result:
        :return:
        """
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
    client = TSDBClient()
    r = REPL(client)
    r.onecmd("insert [1,2,3] @ [4, 5, 6] into tabby")
    r.onecmd("insert [8,9,10] @ [11, 12, 13] into ginger")
    r.cmdloop()

