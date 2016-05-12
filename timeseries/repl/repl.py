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

# https://docs.python.org/3/library/cmd.html#cmd.Cmd.cmdloop

class DumbREPL(cmd.Cmd):
    """
    TODO
    tests
    docstrings for everything
    clean up code and defensive coding checks
    prepare demo, understand! (ply vs. hand parsers)
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
        super(DumbREPL, self).__init__()
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
        # ignores arg
        self.print('Goodbye...')
        sys.exit(0)

    def do_insert(self, arg):
        """
        "[1, 3, 5] @ [5, 6, 7] into primarykey"
        where the second [] are the timestamps
        first [] are the values
        """
        first_split = arg.split('@')
        if len(first_split) != 2:
            self.print('Bad syntax!')
            return

        second_split = first_split[1].split('into')
        if len(second_split) != 2:
            self.print('Bad syntax!')
            return

        # TODO loop through and check list of all numbers and two lists are same length.

        # TODO put in try except for invalid JSON syntax
        values = json.loads(first_split[0].strip())
        timestamps = json.loads(second_split[0].strip())
        self.print(values)
        self.print(timestamps)

        pk = second_split[1].strip()

        self.client.insert_ts(pk, ts.TimeSeries(timestamps, values))

        self.print('OK!')

    def do_newinsert(self, arg):
        lex = lexer.new_lexer()
        ast = self.parser.parse('insert ' + arg, lexer=lex)
        if ast is None:
            print('Error!')
            return

        self.print('OK!')

    def do_select(self, arg):
        """
        TODO see console for command used

        look in procs directory for available procs
            - stats(): returns means and std
        """
        lex = lexer.new_lexer()

        ast = self.parser.parse('select ' + arg, lexer=lex)
        # catch parse error condition
        if ast is None:
            print('Error!')
            return

        if ast.pk:
            metadata_dict = {'pk': ast.pk}
        else:
            metadata_dict = None

        additional = {}
        if ast.orderby:
            # + for ascending, - for descending
            if ast.ascending:
                additional['sort_by'] = '+' + ast.orderby
            else:
                additional['sort_by'] = '-' + ast.orderby

        if ast.limit is not None:
            additional['limit'] = ast.limit

        if isinstance(ast.selector, AST_proc):
            self.print_select_result(self.client.augmented_select(
                proc=ast.selector.id,
                target=ast.selector.targets,
                metadata_dict=metadata_dict,
                additional=(additional or None))
            )
        else:
            if ast.selector:
                fields = ast.selector
            else:
                fields = []

            self.print_select_result(self.client.select(
                    metadata_dict=metadata_dict,
                    fields=fields,
                    additional=(additional or None))
                    )

    def do_dump(self, arg):
        self.print_select_result(self.client.select(fields=['ts']))

    def do_upsert(self, arg):
        """
        UPSERT pk {'hi': 'bye'}

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
        status, payload = result
        if status is not TSDBStatus.OK:
            self.print('Error! %r' % payload)
            return

        for key, values in payload.items():
            self.print(key)
            for vkey, vvalues in values.items():
                if isinstance(vvalues, OrderedDict):
                    self.print('    ', vkey)
                    for hkey, hvalues in vvalues.items():
                        self.print('      ', hkey, ': ', hvalues)
                else:
                    self.print('   ', vkey, ': ', vvalues)


if __name__ == '__main__':
    client = TSDBClient()
    r = DumbREPL(client)
    r.onecmd("insert [1,2,3] @ [4, 5, 6] into tabby")
    r.onecmd("insert [8,9,10] @ [11, 12, 13] into ginger")
    r.cmdloop()

