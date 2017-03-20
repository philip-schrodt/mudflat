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
        if li[7].startswith("dobj"):
            print("dobj:",li[1], "(" + li[7] + ") [" + li[0] + "]")
    print()
    
def find_code(thetext):
    if thetext:
        thetext = thetext.upper()
        words = thetext.split(' ')
        for wd in words:
#            print("checking",wd)
            if wd in globals.ActorDict:
                try:
                    code = globals.ActorDict[wd]['#'][0][0]
                except:  # this is a bit messy and will be modified once I do more with the dictionary
                    pass
                if code:
                    return code
        return None
    else:
        return None
    
def code_actors():
    srctext, srccode = "", ""
    tartext, tarcode = "", ""
    roottext, rootcode = "", ""

    for li in plist:
        if li[7] == "root":
#            print("root:",li[1], "[" + li[0] + "]")
            iroot = li[0]
            if not roottext:
                rootcode = li[1].upper()
                roottext = li[1]
        if "nsubj" in li[7]:
#            print("nsubj:",li[1], "[" + li[0] + "] --> ", get_nsubj(li))
            srctext = get_nsubj(li)
        if li[7].startswith("ob"):
            pass
#            print("obj:",li[1], "(" + li[7] + ") [" + li[0] + "]")
        if li[7].startswith("dobj"):
#            print("dobj:",li[1], "(" + li[7] + ") [" + li[0] + "]")
            tartext = li[1]

    srccode = find_code(srctext)
    tarcode = find_code(tartext)
                    
    if srccode and tarcode:
        return [srccode, tarcode, rootcode], [srctext, tartext, roottext]
    else:
        return None, None

def do_coding(parg, plovrec):
    global plist
    plist = parg
    codes, texts = code_actors()
    if codes:
        plovrec["source"] = [{"code" : codes[0], "actorText" : texts[0]}]
        plovrec["target"] = [{"code" : codes[1], "actorText" : texts[1]}]
        plovrec["event"] = codes[2]
        plovrec["eventText"] = texts[2]
        plovrec["mode"] = "mode-holder"
        plovrec["context"] = "context-holder"
        return True
    else:
        return False
 