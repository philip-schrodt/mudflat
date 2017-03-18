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

import mf_reader
import mf_globals
import utilities

import os
import sys
import glob
import time
import types
import logging
import argparse

def get_nsubj(subji):
    subjstrg = subji[1]
    for li in reversed(plist[:int(subji[0]) - 1]):
#        print(li)
        if li[6] == subji[0]:
            subjstrg = li[1] + ' ' + subjstrg
    for li in plist[int(subji[0]):]:
#        print(li)
        if li[6] == subji[0]:
            subjstrg = subjstrg + ' ' + li[1]
    return subjstrg       
    
    
def print_info():
    if not thesent:
        return
    print(thesent)
    for li in plist:
        if li[7] == "root":
            print("root:",li[1], "[" + li[0] + "]")
            iroot = li[0]
        if "nsubj" in li[7]:
            print("nsubj:",li[1], "[" + li[0] + "] --> ", get_nsubj(li))
        if li[7].startswith("ob"):
            print("obj:",li[1], "(" + li[7] + ") [" + li[0] + "]")
    print()
    
def print_plover():
    if not thesent:
        return
#    print(thesent)
    for li in plist:
        if li[7] == "root" and li[2].upper() in mf_globals.VerbDict['verbs']:
            print('"' + li[2].upper() + '"')
            print_info()
            break
        """if "nsubj" in li[7]:
            print("nsubj:",li[1], "[" + li[0] + "] --> ", get_nsubj(li))
        if li[7].startswith("ob"):
            print("obj:",li[1], "(" + li[7] + ") [" + li[0] + "]")"""
#    print()

def read_dictionaries(validation=False):
    """ Modified from PETR-2 """

    print('Verb dictionary:', mf_globals.VerbFileName)
    verb_path = utilities._get_data(
        'data/dictionaries',
        mf_globals.VerbFileName)
    mf_reader.read_verb_dictionary(verb_path)
    
    print('Actor dictionaries:', mf_globals.ActorFileList)
    for actdict in mf_globals.ActorFileList:
        actor_path = utilities._get_data('data/dictionaries', actdict)
        mf_reader.read_actor_dictionary(actor_path)

    print('Agent dictionary:', mf_globals.AgentFileName)
    agent_path = utilities._get_data('data/dictionaries',
                                     mf_globals.AgentFileName)
    mf_reader.read_agent_dictionary(agent_path)

    print('Discard dictionary:', mf_globals.DiscardFileName)
    discard_path = utilities._get_data('data/dictionaries',
                                       mf_globals.DiscardFileName)
    mf_reader.read_discard_list(discard_path)

    if mf_globals.IssueFileName != "":
        print('Issues dictionary:', mf_globals.IssueFileName)
        issue_path = utilities._get_data('data/dictionaries',
                                         mf_globals.IssueFileName)
        mf_reader.read_issue_list(issue_path)

utilities.init_logger('mudflat.log')
logger = logging.getLogger('mf_log')

config = False
if config:
    print('Using user-specified config: {}'.format(config))
    logger.info('Using user-specified config: {}'.format(config))
    mf_reader.parse_Config(config)
else:
    logger.info('Using default config file.')
    logger.info('Config path: {}'.format(utilities._get_data('data/config/',
                                                             'mudflat_config.ini')))
    mf_reader.parse_Config(utilities._get_data('data/config/',
                                                    'mudflat_config.ini'))
read_dictionaries()
print(mf_globals.VerbDict['verbs']["KILL"])  
"""fout = open("verb.dict.txt",'w')
for k,v in sorted(mf_globals.VerbDict.items()):
    fout.write(k + '\n')
    for i,j in v.items():
        fout.write(str(i) + ' ' + str(j) + '\n')
fout.close()

fout = open("actor.dict.txt",'w')
for j,k in sorted(mf_globals.ActorDict.items()):
    fout.write(j + '\t\t' + str(k) + '\n')
#    fout.write(j + '\t\t' + k + '\n')
fout.close()
#mf_reader.show_verb_dictionary("verb.dict.txt")
sys.exit()"""

thesent = None
#fin = open("evetn_text_subset1.txt",'r')
fin = open("en-ud-dev.conllu.events.txt",'r')
ka = 0
line = fin.readline() 
while len(line) > 0:  # loop through the file
    if line.startswith("# sent_id"):
#        print_info()
        print_plover()
        ka += 1
        if ka > 256: break
    elif line.startswith("# text"):
        thesent = line[9:-1]
    elif line.startswith("1"):
        plist = [line[:-1].split('\t')]
        line = fin.readline() 
        while len(line) > 1:
            plist.append(line[:-1].split('\t'))
            line = fin.readline() 
    line = fin.readline() 

fin.close()
print("Finished")