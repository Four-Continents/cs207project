#!/usr/bin/env python3

import cmd
import sys
from . import lexer
from . import parser
from tsdb.tsdb_client import TSDBClient
import timeseries as ts
import json

# https://docs.python.org/3/library/cmd.html#cmd.Cmd.cmdloop

class DumbREPL(cmd.Cmd):
    """
    DEMO - show help function (help) shows docstrings

    Must run server first

    re-prepend first word back after get it
    instantiate a lexer and pull out pieces (using ply)
    then pass through to tsdb_client.py
    start wtih really simple dumb thing...like list of integers
    can define own things like dump
    just use dumb hand coded parsers... simple languages. Get it simple things. Can add fancier things
    integrate ply to have fancier grammar
    dumb command: insert takes a list.

    insert [1, 2, 3, ... ] into whatever;
    dump whatever; # print all the points (will do a select)

    select field1, field2, ... from whatever;
    slice out fields part from select statements, do string split, these become field names
    select has a fields argument, and by default Fields gets None, pass list of fields into fields

    select ... from whatever order by f1 (order by becomes the additional argument, is the sorting key
    select ... from whatever order by f1 {"sort_by": "+f1"} - see documention of select of dictdb.py

    select ... from whatever order by f1 limit 10. see docs at bottom of dictdb.py

    in order to get self off the ground in simplest way possible, write REPL so first it instantiates client
    then inserts some hardcoded data by using insert from client
    then starts command loop
    then command loop will implement one command just dump, because simplest
    that way don't have write insert parser first

    in main, will connect to a server
    REPL: separately start a server process, start REPL,then point it to server address (port)
    tsdb_server.py see in main of tsdb_server.py, runs on localhost
    start server, then start REPL
    or write a shell script that starts server, then starts REPL
    or just have user start server, then have user start up REPL

    Parts
    1. write a parser for command language (cmd.cmd looks at first word of command line, dispatches to methods do_...method)
    in parser, going to want to write something that can parse the rest of the comamnd
    see parser.py - what do I want my command language to look like.
    1. Writing parser for command language, 2. hooking up REPL to the tsdb_client.py
    Make it SQL-like. Dumb easier parse variant of SQL SELECT FROM TIMESERIES NAME
    understand functions offered by TSDB. One command for each of TSDB Client API, 1 command type for each
    make up syntax for how to do arguments
    insert_ts takes primary key and time series... see Google Hangout
    Write pype grammar
    Set up separate module for Pype - set up lexer and parser.py
    set up one directory for REPL
    do one command at a time. Do insert and select
    instantiate lexer and parser
    lexer, parser, repl that uses cmd

    Can only use insert_ts, upsert_meta, select
    maybe augmented_select - procedures??
    """
    def __init__(self, client):
        super(DumbREPL, self).__init__()
        self.client = client
        self.print = print

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
        par = parser.new_parser()
        ast = par.parse('insert ' + arg, lexer=lex)
        print(ast)

    def do_dump(self, arg):
        # TODO make printing better
        self.print(self.client.select(fields=['ts']))

    def do_upsert(self, arg):
        """
        insert if primary key doesn't exist
        update if primary key does exist
        """
        pass

if __name__ == '__main__':
    client = TSDBClient()
    DumbREPL(client).cmdloop()
