"""
coder.py

Coding routines for mudflat

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
20-Mar-17:	Initial version

"""

import globals

plist = [] # create a local for this


def get_NP(sdex):
    """ construct noun phrase based on word at sdex """
    index = int(sdex) - 1
    return ' '.join(reversed(
            [li[1] for li in reversed(plist[:index]) if li[6] == sdex and li[7] in ["compound", "amod"]]
            )) + ' ' + plist[index][1] + ' ' + \
            ' '.join([li[1] for li in plist[index + 1:] if li[6] == sdex and li[7] in ["compound", "amod"]])

    
def get_conj(sdex):
    """ check if there are compound elements """
    return [sdex] + [li[0] for li in plist if li[6] == sdex and li[7] == "conj"]       

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
        if li[7].startswith("dobj"):
            print("dobj:",li[1], "(" + li[7] + ") [" + li[0] + "]")
    print()
    
def find_code(thetext):
    if thetext:
        thetext = thetext.upper()
        words = thetext.split(' ')
        code = ""
        for wd in words:
#            print("checking",wd)
            if wd in globals.ActorDict:
                try:
                    code = globals.ActorDict[wd]['#'][0][0]
                except:  # this is a bit messy and will be modified once I do more with the dictionary
                    code = None
                if code:
                    return code
        return None
    else:
        return None
    
def find_sec_code(thetext):
    if thetext:
        thetext = thetext.upper()
        words = thetext.split(' ')
        codestrg = ""
        for wd in words:
#            print("checking",wd)
            if wd in globals.ActorDict:
                try:
                    code = globals.AgentDict[wd]['#']
                except:  # this is a bit messy and will be modified once I do more with the dictionary
                    code = None
                if code:
                    codestrg += code[1:]
        return codestrg
    else:
        return None

def code_events():
    srctext, srccode, srcseccode, srclist = [], [], [], []
    tartext, tarcode, tarseccode, tarlist = [], [], [], []
    roottext, rootcode = "", ""

    for li in plist:
        if "nsubj" == li[7]:
#            print("nsubj:",li[1], "[" + li[0] + "] --> ", get_nsubj(li))
            srclist = get_conj(li[0])
#            srctext = get_NP(li[0])
            iroot = int(li[6])
            rootcode = plist[iroot - 1][2].upper()  # adjust for zero indexing
            roottext = plist[iroot - 1][1]
            tarlist = []
            for lobj in plist:
                if lobj[7] == "dobj" and lobj[6] == li[6]:
#                    tartext = get_NP(lobj[0])
                    tarlist = get_conj(lobj[0])
            if tarlist:
#                print(srclist, tarlist)
                break

    for idx in srclist:
        text = get_NP(idx)
        code = find_code(text)
        seccode = find_sec_code(text)
        if code or seccode:
            srctext.append(text)
            srccode.append(code)
            srcseccode.append(seccode)
        
    for idx in tarlist:
        text = get_NP(idx)
        code = find_code(text)
        seccode = find_sec_code(text)
        if code or seccode:
            tarcode.append(code)
            tartext.append(text)
            tarseccode.append(seccode)
                    
    if (srccode or srcseccode) and (tarcode or tarseccode):
        return [srccode, srcseccode, tarcode, tarseccode, rootcode], [srctext, tartext, roottext]
    else:
        return None, None


def do_coding(parg, plovrec):
    global plist
    
    def make_actrec(code, sect, text):
        """ create an actor record """
        actrec = {"actorText" : text}
        if code:
            actrec["code"] = code
        if sect:
            actrec["sector"] = sect
        return actrec

    plist = parg
    codes, texts = code_events()
    if codes:
        plovrec["source"] = []
        for ka in range(len(codes[0])):
            plovrec["source"].append(make_actrec(codes[0][ka], codes[1][ka], texts[0][ka]))
        plovrec["target"] = []
        for ka in range(len(codes[2])):
            plovrec["target"].append(make_actrec(codes[2][ka], codes[3][ka], texts[1][ka]))
        plovrec["event"] = codes[4]
        plovrec["eventText"] = texts[2]
        plovrec["mode"] = "mode-holder"
        plovrec["context"] = "context-holder"
        return True
    else:
        return False
 