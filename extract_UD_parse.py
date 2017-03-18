"""
extract_UD_parse.py

Utility for experimenting with extract various elements from a CoNLL-U parse. Uses the a subset of the
en-ud-dev.conllu file from 

TO RUN PROGRAM:

python3 extract_UD_parse.py


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
    
thesent = None
fin = open("evetn_text_subset1.txt",'r')
ka = 0
line = fin.readline() 
while len(line) > 0:  # loop through the file
    if line.startswith("# sent_id"):
        print_info()
        ka += 1
        if ka > 6: break
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
