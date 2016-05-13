# cs207project

[![Build Status](https://travis-ci.org/Four-Continents/cs207project.svg?branch=master)](https://travis-ci.org/Four-Continents/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/Four-Continents/cs207project/badge.svg?branch=master)](https://coveralls.io/github/Four-Continents/cs207project?branch=master)


Description
===========

This packages implements a persistent timeseries database with a REST API.  

### REPL

For the additional feature, we chose to implement a new database language with a REPL as a client for the database because we were interested in tying together concepts learned from all three major modules of CS207: timeseries, pype, and databases. The REPL leverages Python's cmd library while the database language uses the ply library covered in the pype module to manage some of the production rules and grammars. Though this may not be the "purist" approach, we made an explicit design choice to implement the language using a hybrid approach in which simpler database commands were parsed and executed directly in the Python code for the REPL, whereas more complex commands such as SELECT involving a wide permutation of optional arguments such as limit, order by ascending and descending order, and procs were handled by ply with separate scripts housing the AST classes, lexer, and parser.  

As an example of why we felt this was a justifiable design choice, consider the example of `upsert_meta`, which could have involved 3 possible approaches: 1) write JSON grammar with all production rules to understand the various types of valid JSON, 2) use delimiters to send a raw string to ply to then handle the json loads within the parser, or 3) define a simple yet effective syntax to simply chop off the beginning and leverage the JSON parser directly within the REPL script. The issue with the second option is that it would require the use of delimiters, which would restrict the user from using certain json values unless we were to then introduce the concept of escaping and escape characters to our grammars. Ultimately, we chose approach #3 over #1 and #2 for simplicity over introducing unnecessary complexity that still efficiently satisfies the database API specs provided to us by our customer.  

The REPL also has a help feature similar to man-pages that allows users to look up help pages for the commands and syntax rules of the database language.  


Instructions and Technical Details
=================================
### Install
The package can be installed by running `python setup.py install`.  

### Instructions on how to run the database REPL: 
1. From the parent directory above the tsdb directory, launch the server by entering into the command line `PYTHONPATH=. python –m tsdb.tsdb_server`  
2. From the parent directoy above the tsdb directory, launch the repl by entering into the command line `PYTHONPATH=. python -m repl.repl`  
3. To get started on what commands are available, type `help`. To read documentation on specific commands, type `help <command name>`.  


Note
====

This project has been set up using PyScaffold 2.5.5. For details and usage
information on PyScaffold see http://pyscaffold.readthedocs.org/.


==========
Developers
==========

* Amy Lee <amymaelee@g.harvard.edu>  
* Fanny Heneine <fannyheneine@g.harvard.edu>   
* Isadora Nun <isadoranun@g.harvard.edu>  
* Vinay Subbiah <vinayps89@gmail.com>  
* Victor Lei <vlei@g.harvard.edu>  
