# cs207project

[![Build Status](https://travis-ci.org/Four-Continents/cs207project.svg?branch=master)](https://travis-ci.org/Four-Continents/cs207project)

[![Coverage Status](https://coveralls.io/repos/github/Four-Continents/cs207project/badge.svg?branch=master)](https://coveralls.io/github/Four-Continents/cs207project?branch=master)


Description
===========

This packages implements a persistent timeseries database with a REST API.  


### Persistence
As shown in the lectures and labs, we used an append-only log to write rows to disk. Using pickle and string-based methods, we store the DB state to disk during every explicit commit() operation, or after each operation that modifies the database.  

This allows for very fast updates and deletes, but can cause the log to get large over time if it's not cleaned periodically. Internally, the primary keys are stored in a binary tree so that lookups and modifications are fast. Secondary indices are done using hash tables, which ensures a fast lookup for most data types.  

Indices are stored in a separate file to the contents of the DB. This can potentially create an issue if the program crashes between the writing of the contents to disk, and the writing of the index to disk. However, for the purposes of this project, we believe it to be a reasonable trade-off given the time constraints.  

We also have atomicity at the individual operation-level by committing to disk after each operation. If the next operation fails, it does not get persisted and we simply roll back to the last state.  

### Latest features
- The deletion was implemented by removing the index from the reference binary tree and updating all indices by removing the PK. This has the benefit of speed, but leaves the record in disk and should be cleaned up after while.  
- Similarity search is implemented by first assuming that the database is up to date in terms of populating the vantage point information. A time series is provided to the search function (call this is ‘query’ time series) which is then compared to the vantage points to find the most similar; call this distance to the most similar vantage point ‘D’. Finally, a select is performed to get all time series within `2*D` distance from the nearest vantage point.  
- Populate database is a quick way to get a database of random time series of size 100 into the database. The database is updated to the point where the similarity search can be run.  

### REPL & Database Query Language

For the additional feature, we chose to implement a new database language with a REPL as a client for the database because we were interested in tying together concepts learned from all three major modules of CS207: timeseries, pype, and databases. The REPL leverages Python's cmd library while the database language uses the ply library covered in the pype module to manage some of the production rules and grammars. Though this may not be the "purist" approach, we made an explicit design choice to implement the language using a hybrid approach in which simpler database commands were parsed and executed directly in the Python code for the REPL, whereas more complex commands such as SELECT involving a wide permutation of optional arguments such as limit, order by ascending and descending order, and procs were handled by ply with separate scripts housing the AST classes, lexer, and parser.  

As an example of why we felt this was a justifiable design choice, consider the example of `upsert_meta`, which could have involved 3 possible approaches: 1) write JSON grammar with all production rules to understand the various types of valid JSON, 2) use delimiters to send a raw string to ply to then handle the json loads within the parser, or 3) define a simple yet effective syntax to simply chop off the beginning and leverage the JSON parser directly within the REPL script. The issue with the second option is that it would require the use of delimiters, which would restrict the user from using certain json values unless we were to then introduce the concept of escaping and escape characters to our grammars. Ultimately, we chose approach #3 over #1 and #2 for simplicity over introducing unnecessary complexity that still efficiently satisfies the database API specs provided to us by our customer.  

The REPL also has a help feature similar to man-pages that allows users to look up help pages for the commands and syntax rules of the database language.  


Instructions and Technical Details
================================= 

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
