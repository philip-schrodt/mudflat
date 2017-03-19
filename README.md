# mudflat

Minimal universal dependency friendly little automated tagger

A coding system supporting PLOVER (of course): https://github.com/openeventdata/PLOVER; http://ploverdata.org

Files
=====

All programs are Python 3.5 and open source under the MIT License.

mudflat.py
----------
Main driver program

mf_globals.py
-------------
Globals, adapted from PETRARCH-2 (https://github.com/openeventdata/petrarch2)

mf_reader.py
------------
Configuration and dictionary input adapted from PETRARCH-2; CoNNL input

write_PLOVER.py
---------------
Routine for writing PLOVER records

extract_UD_parse.py
-------------------
Utility program for experimenting with CoNLL-U format routines
