"""
mudflat.py

Utility for experimenting with extract various elements from a CoNLL-U parse. Uses the a subset of the
en-ud-dev.conllu file from https://github.com/UniversalDependencies/UD_English

TO RUN PROGRAM:

python3 mudflat.py


PROGRAMMING NOTES: None

SYSTEM REQUIREMENTS
This program has been successfully run under Mac OS 10.10.5; it is standard Python 3.5
so it should also run in Unix or Windows. 

PROVENANCE:
Programmer: Philip A. Schrodt
            Parus Analytics
            Charlottesville, VA, 22901 U.S.A.
            http://eventdata.parusanalytics.com

Copyright (c) 2017	Philip A. Schrodt.	All rights reserved.

This code is covered under the MIT license: http://opensource.org/licenses/MIT

Report bugs to: schrodt735@gmail.com

REVISION HISTORY:
17-Mar-17:	Initial version

=========================================================================================================
"""

import reader
import globals
import utilities
import coder

import os
import sys
import glob
import time
import types
import logging
import argparse


def read_dictionaries(validation=False):
    """ Modified from PETR-2 """

    print('Verb dictionary:', globals.VerbFileName)
    verb_path = utilities._get_data(
        'data/dictionaries',
        globals.VerbFileName)
    reader.read_verb_dictionary(verb_path)
    
    print('Actor dictionaries:', globals.ActorFileList)
    for actdict in globals.ActorFileList:
        actor_path = utilities._get_data('data/dictionaries', actdict)
        reader.read_actor_dictionary(actor_path)

    """print('Agent dictionary:', globals.AgentFileName)
    agent_path = utilities._get_data('data/dictionaries',
                                     globals.AgentFileName)
    reader.read_agent_dictionary(agent_path)

    print('Discard dictionary:', globals.DiscardFileName)
    discard_path = utilities._get_data('data/dictionaries',
                                       globals.DiscardFileName)
    reader.read_discard_list(discard_path)

    if globals.IssueFileName != "":
        print('Issues dictionary:', globals.IssueFileName)
        issue_path = utilities._get_data('data/dictionaries',
                                         globals.IssueFileName)
        reader.read_issue_list(issue_path)"""

utilities.init_logger('mudflat.log')
logger = logging.getLogger('mf_log')

config = False
if config:
    print('Using user-specified config: {}'.format(config))
    logger.info('Using user-specified config: {}'.format(config))
    reader.parse_Config(config)
else:
    logger.info('Using default config file.')
    logger.info('Config path: {}'.format(utilities._get_data('data/config/',
                                                             'mudflat_config.ini')))
    reader.parse_Config(utilities._get_data('data/config/',
                                                    'mudflat_config.ini'))
read_dictionaries()

#fin = open("evetn_text_subset1.txt",'r')
#fin = open("en-ud-dev.conllu.events.txt",'r')
#fin = open("conll_test_records_edited_3.txt",'r')
fin = open("mudflat_testdata_Mk1.txt",'r')
fout = open("test2_output.txt",'w')
ka = 0
line = fin.readline()  # read past initial sent-id
idstrg = line[12:-1]
thesent = ""
line = fin.readline() 
while len(line) > 0:  # loop through the file
    if line.startswith("# sent_id"):
#        print_info()
        plovrec = utilities.get_plover_template(idstrg, datestrg, publicatnstrg, thesent)
        if coder.do_coding(plist, plovrec):
            utilities.write_record(plovrec,fout)
        idstrg = line[12:-1]
        thesent = ""
        ka += 1
        if ka > 4: break
    elif line.startswith("# text"):
        thesent += line[9:-1] + ' '
    elif line.startswith("# source"):
        publicatnstrg = line[11:-1]
    elif line.startswith("# date"):
        datestrg = line[9:-1]
    elif line.startswith("1"):
        plist = [line[:-1].split('\t')]
        line = fin.readline() 
        while len(line) > 1:
            plist.append(line[:-1].split('\t'))
            line = fin.readline() 
    line = fin.readline() 

fin.close()
fout.close()
print("Finished")