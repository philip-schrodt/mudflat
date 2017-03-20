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

DEFAULT_INPUT_NAME = "mudflat_testdata_Mk1.txt"
DEFAULT_OUTPUT_NAME = "mf_test_output.txt"

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

    print('Agent dictionary:', globals.AgentFileName)
    agent_path = utilities._get_data('data/dictionaries',
                                     globals.AgentFileName)
    reader.read_agent_dictionary(agent_path)
#    print(globals.AgentDict)
#    exit()

    """print('Discard dictionary:', globals.DiscardFileName)
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

cli_args = utilities.parse_cli_args()
if cli_args.input:
    input_file_name = cli_args.input
else:
    input_file_name = DEFAULT_INPUT_NAME

if cli_args.output:
    output_file_name = cli_args.output
else:
    output_file_name = DEFAULT_OUTPUT_NAME

if cli_args.maxrecords:
    maxrec = int(cli_args.maxrecords)
else:
    maxrec = 0


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

reader.open_input(input_file_name)
fout = open(output_file_name,'w')
krec = 0
ncoded = 0
plist, plovrec = reader.read_conllu_record()
while plist:  # loop through the file
    if coder.do_coding(plist, plovrec):
        utilities.write_record(plovrec,fout)
        print(krec, plovrec["id"], plovrec["event"])
        ncoded += 1
    if maxrec > 0 and krec > maxrec: 
        break
    plist, plovrec = reader.read_conllu_record()

reader.close_input()
fout.close()
print("Events coded:", ncoded)
print("Finished")