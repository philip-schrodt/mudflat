# -*- coding: utf-8 -*-

##	utilities.py [module]
##
# Utilities for the PETRARCH event data coder
##
# SYSTEM REQUIREMENTS
# This program has been successfully run under Mac OS 10.10; it is standard Python 2.7
# so it should also run in Unix or Windows.
#
# INITIAL PROVENANCE:
# Programmer:
#             John Beieler
#			  Caerus Associates/Penn State University
#			  Washington, DC / State College, PA, 16801 U.S.A.
#			  http://caerusassociates.com
#             http://bdss.psu.edu
#
# GitHub repository: https://github.com/openeventdata/petrarch
#
# Copyright (c) 2014	John Beieler.	All rights reserved.
#
# This project is part of the Open Event Data Alliance tool set
#
# This code is covered under the MIT license
#
# Report bugs to: john.b30@gmail.com
#
# REVISION HISTORY:
#    Summer-14:	 Initial version
#    April 2016: added extract_phrases() 

# pas 16.04.22: print() statements commented-out with '# --' were used in the debugging and can probably be removed
# ------------------------------------------------------------------------

# import globals

import os
import logging
import dateutil.parser
from collections import defaultdict, Counter
from datetime import datetime
import json

field_order = ["id", "date", "source","target", "event", "eventText", "mode", "context", "text", 
               "language", "publication", "coder", "version", "dateCoded", "comment"]

nulllist = []  # used when PETRglobals.NullVerbs == True
""" <16.06.27 pas> This might be better placed in PETRtree but I'm leaving it here so that it is clear it is a global. 
    Someone who can better grok recursion than I might also be able to eliminate the need for it."""




def parse_to_text(parse):
    x = filter(lambda a : not a.startswith("("), parse.replace(")","").split())
    r = "" + x[0]
    for item in x[1:]:
        r += " " + item
    return r


def extract_phrases(sent_dict,sent_id):
    """  
    Text extraction for PETRglobals.WriteActorText and PETRglobals.WriteEventText 

    Parameters
    ----------

    story_dict: Dictionary.
                Story-level dictionary as stored in the main event-holding dictionary within PETRARCH.

    story_id: String.
                Unique StoryID in standard PETRARCH format.

    Returns
    -------

    text_dict: Dictionary indexed by event 3-tuple.
               List of texts in the order  [source_actor, target_actor, event]
    """

    def get_text_phrase(phst):
        """ find the words in original sentence text corresponding to the string phst, putting in ... when the words
            are not consecutive and < wd > for elements not recognized, which are usually actor codes or synonym sets. """
        phlist = phst.split(' ')  
        curloc = 0
        lcphst = ''
        for wd in phlist:
            newloc = ucont.find(wd,curloc)
            if newloc >= 0:
                if lcphst and newloc > curloc + 1: # add elipses if words are not consecutive
                    lcphst += ' ...'
                curloc = newloc + len(wd)
                lcphst += ' ' + content[newloc:curloc]
            else:
                lcphst += ' <' + wd + '>'  # use <...> for elements not recognized
# --        print('   GTP:',lcphst)
        return lcphst.strip()    
    
    def get_noun_list():
        """ Make (text, code, root) tuples from any sets of compounds """
# --        print('gnl: ',sent_dict['meta']['nouns'])
        noun_list = []
        for ca in sent_dict['meta']['nouns']:  # 
            if len(ca[1]) == 1:
                noun_list.append(ca)
            else:
                for ka in range(len(ca[1])):
                    #noun_list.append((ca[0][ka],ca[1][ka],ca[2][ka]))
                    try:
                        if ka < len(ca[0]):   
                            noun_list.append((ca[0][ka],ca[1][ka],ca[2][ka]))
                        else:
                            noun_list.append((ca[0][-1],ca[1][ka],ca[2][-1]))  # appears this can occur if the same string, e.g. "MINISTER" applies to multiple codes
                    except:
                        pass  # 16.06.27 occasionally fails due to lists not being same length, so just do nothing
                    
        return noun_list                                 

    def get_actor_phrase(code,typest):
        if code.startswith('---'):
            code = '~' + code[3:]
        noun_list = get_noun_list()
                                            
# --        print(' -- ',noun_list)
        for ca in noun_list:
            if code in ca[1]:
# --                print(' -- match:',code, ca)
                tarst = ''
                for st in ca[0]:
                    tarst += st
# --                print(typest + ' text:',tarst)
                return get_text_phrase(tarst[1:])
        else:
            logger.info('ut.EP {} text not found'.format(sent_id, typest))
            print('ut.EP {} text not found'.format(sent_id, typest))
            return '---'

    def get_actor_root(code):
        if code.startswith('---'):
            return '---'
        noun_list = get_noun_list()                                            
# --        print(' ** ',noun_list)
        for ca in noun_list:
# --            print('===',ca)  # --
            if code in ca[1]:
# --                print(' -- match:',code, ca)   # --
                if len(ca) > 2 and ca[2] != '~':
                        phrst = ''
                        for li in ca[2]:
                            if isinstance(li,list):  # 16.04.28 pas I am not happy with this contigency: things should be stored in just one format, but don't have time to resolve this at the moment
                                phrst += ' ' + ' '.join(li)
                            else:
                                phrst += ' ' + li
                                                    
                        return phrst.replace(' ~','').strip()
                        
                else:
# --                    print(' -- -- \'---\'')
                    return '---'
        else:
            return '---'

    def get_event_phrase(verb_list):
        phst = ''
        words = ''
        for st in verb_list:
# --            print('   GEP1:',st)
            if isinstance(st,basestring):  # handles those  ~ a (a b Q) SAY = a b Q cases I haven't figured out yet [pas 16.04.20]
                continue
            if len(st) > 1:
                if '[' in st[1]:  # create a phrase for a pattern
                    sta = st[1][1:st[1].find('[')].strip()
                    words = sta.replace('*',st[0])
                    words = words.replace('(','')
                    words = words.replace(')','')
                elif isinstance(st[1],tuple):   # create phrase based on a tuple patterns
                    words = st[0]
                    for tp in st[1:]:
                        words += ' ' + tp[0] 
                        if len(tp[1]) > 0:
                            words += ' ' + tp[1][0]
                        else:
                            words += ' ---'
                else:
                    words = str(st)
            else:
                if st[0]:   # in very rare circumstances, st[0] == None
                    words = st[0]
            if words not in phst:  # 16.04.28: verbs are occasionally duplicated in 'meta' -- this is just a hack to get around that at the moment
                phst = words + ' ' + phst
# --            print('   GEP2:',phst)
        return get_text_phrase(phst)
               
    logger = logging.getLogger('petr_log')
    text_dict = {}  # returns texts in lists indexed by evt
    """print('EP1:',sent_dict['content']) # --
    print('EP2:',sent_dict['meta'])  # -- """
    content = sent_dict['content']
    ucont = sent_dict['content'].upper()
    keylist = list(sent_dict['meta'].keys())
    if len(keylist) < 2:
        logger.info('ut.EP {} len(keylist) < 2 {}'.format(sent_id, keylist))
        print('ut.EP {} len(keylist) < 2 {}'.format(sent_id, keylist))
    for evt in keylist:
        if evt == 'nouns':
            continue
# --        print('EP3:',evt)
        text_dict[evt] = ['','','','','']
        if PETRglobals.WriteActorText :
            text_dict[evt][0] = get_actor_phrase(evt[0],'Source')
            text_dict[evt][1] = get_actor_phrase(evt[1],'Target')
        if PETRglobals.WriteEventText :
            text_dict[evt][2] = get_event_phrase(sent_dict['meta'][evt])
        if PETRglobals.WriteActorRoot :
            text_dict[evt][3] = get_actor_root(evt[0]) # 'SRC-ROOT' 
            text_dict[evt][4] = get_actor_root(evt[1]) # 'TAR-ROOT'
    return text_dict

def story_filter(story_dict, story_id):
    """
    One-a-story filter for the events. There can only be only one unique
    (DATE, SRC, TGT, EVENT) tuple per story.

    Parameters
    ----------

    story_dict: Dictionary.
                Story-level dictionary as stored in the main event-holding
                dictionary within PETRARCH.

    story_id: String.
                Unique StoryID in standard PETRARCH format.

    Returns
    -------

    filtered: Dictionary.
                Holder for filtered events with the format
                {(EVENT TUPLE): {'issues': [], 'ids': []}} where the 'issues'
                list is optional.
    """
    filtered = defaultdict(dict)
    story_date = story_dict['meta']['date']
    for sent in story_dict['sents']:
        sent_dict = story_dict['sents'][sent]
        sent_id = '{}_{}'.format(story_id, sent)
        if 'events' in sent_dict:
            """print('ut:SF1',sent,'\n',story_dict['sents'][sent])
            print('ut:SF2: ',story_dict['meta'])
            print('ut:SF3: ',story_dict['sents'][sent]['meta'])
            print('ut:SF4: ',story_dict['sents'][sent]['events'])"""
            """if  PETRglobals.WriteActorText or PETRglobals.WriteEventText:  # this is the old call before this was moved out to do_coding()
                text_dict = extract_phrases(story_dict['sents'][sent],sent_id)
            else:
                text_dict = {}"""

            for event in story_dict['sents'][sent]['events']:
                # do not print unresolved agents
                try:
                    alist = [story_date]
                    alist.extend(event)
                    event_tuple = tuple(alist)
                    filtered[event_tuple]
                    if 'issues' in sent_dict:
                        filtered[event_tuple]['issues'] = Counter()
                        issues = sent_dict['issues']
                        for issue in issues:
                            filtered[event_tuple]['issues'][
                                issue[0]] += issue[1]

                    # Will keep track of this info, but not necessarily write it out
                    filtered[event_tuple]['ids'] = []
                    filtered[event_tuple]['ids'].append(sent_id)
#                    if event_tuple[1:] in text_dict:  # log an error here if we can't find a non-null case?
                    if 'actortext' in sent_dict['meta'] and event_tuple[1:] in sent_dict['meta']['actortext']:  # 16.04.29 this is a revised version of the above test: it catches cases where extract_phrases() returns a null
                        if PETRglobals.WriteActorText :
                            filtered[event_tuple]['actortext'] = sent_dict['meta']['actortext'][event_tuple[1:]]
                        if PETRglobals.WriteEventText :
                            filtered[event_tuple]['eventtext'] = sent_dict['meta']['eventtext'][event_tuple[1:]]
                        if PETRglobals.WriteActorRoot :
                            filtered[event_tuple]['actorroot'] = sent_dict['meta']['actorroot'][event_tuple[1:]]

                except IndexError:  # 16.04.29 pas it would be helpful to log an error here...
                    pass
        else:
            pass

    return filtered


def _format_parsed_str(parsed_str):
    if parsed_str.strip().startswith("(ROOT") and parsed_str.strip().endswith(")"):
        parsed_str = parsed_str.strip()[5:-1].strip()
    elif parsed_str.strip()[1:].strip().startswith("("):
        parsed_str = parsed_str.strip()[1:-1]
    parsed = parsed_str.split('\n')
    parsed = [line.strip() + ' ' for line in [line1.strip() for line1 in
                                              parsed if line1] if line]
    parsed = [line.replace(')', ' ) ').upper() for line in parsed]
    treestr = ''.join(parsed)
    return treestr


def _format_datestr(date):
    datetime = dateutil.parser.parse(date)
    date = '{}{:02}{:02}'.format(datetime.year, datetime.month, datetime.day)
    return date


def _get_data(dir_path, path):
    """Private function to get the absolute path to the installed files."""
    cwd = os.path.abspath(os.path.dirname(__file__))
    joined = os.path.join(dir_path, path)
    out_dir = os.path.join(cwd, joined)
    return out_dir


def _get_config(config_name):
    cwd = os.path.abspath(os.path.dirname(__file__))
    out_dir = os.path.join(cwd, config_name)
    return out_dir


def init_logger(logger_filename):

    logger = logging.getLogger('petr_log')
    logger.setLevel(logging.INFO)

    cwd = os.getcwd()
    logger_filepath = os.path.join(cwd, logger_filename)

    fh = logging.FileHandler(logger_filepath, 'w')
    formatter = logging.Formatter('%(levelname)s %(asctime)s: %(message)s')
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    logger.info('Running')

# =========== mudflat routines ===========

def write_record(data, fout):
    """ writes data[key] to fout in field order """
    fout.write('{\n')
    for field in field_order:
#        fout.write("    \"" + field + "\": \"" + data[key][field] + "\",\n")
        fout.write("    \"" + field + "\": " + json.dumps(data[field], sort_keys=True) + ",\n")
    fout.write('},\n')

    
def get_plover_template(idstrg, date, publicat = "", thesent = "-- sentence text --"):
    data = {
        "id": idstrg,
        "date": date,
        "text": thesent,
        "language":"en", 
        "publication": publicat, 
        "coder": "Parus Analytics",
        "version": "0.5b1",
        "dateCoded": datetime.now().strftime('%Y-%m-%d'),
        "comment": "test output from mudflat",
        } 
    return data  

'''def convert_code(code,forward = 1):
    """ placeholder """
    return [code, code]'''