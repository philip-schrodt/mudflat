"""
write_PLOVER.py

Routines for writing PLOVER data frames from a list 

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
17-Oct-16:	Initial version for generated PLOVER records from CAMEO manual
18-Mar-17:  Modified for use as mudflat output routine

=========================================================================================================
"""
import json
from datetime import datetime

field_order = ["id", "date", "source","target", "event", "eventText", "mode", "context", "text","textInfo", 
               "language", "publication", "coder", "version", "dateCoded", "comment"]


def write_record(data):
    """ writes data[key] in field order """
    fout.write('{\n')
    for field in field_order:
#        fout.write("    \"" + field + "\": \"" + data[key][field] + "\",\n")
        fout.write("    \"" + field + "\": " + json.dumps(data[field], sort_keys=True) + ",\n")
    fout.write('},\n')
    
def make_plover_record(datalist):
    data = {
        "id": datalist[0],
        "date": datalist[1],
        "source": datalist[2],
        "target": datalist[3],
        "event": datalist[4],
        "eventText": "--event text --",
        "mode": datalist[5],
        "context": datalist[6],
        "text": "-- sentence text --",
        "textInfo":{},
        "language":"en", 
        "publication": "-- publication --", 
        "coder": "Parus Analytics",
        "version": "0.5b1",
        "dateCoded": datetime.now().strftime('%Y-%m-%d'),
        "comment": "",
        } 
    return data  

# ============ test code =============== #

if __name__ == "__main__":
    fin = open("PLOVER.test1.input.txt",'r')
    fout = open("PLOVER.test1.JSON.txt",'w')
    line = fin.readline() 
    while len(line) > 0:
        thedata = line[:-1].split('\t')  
        write_record(make_plover_record(thedata))
        line = fin.readline() 
    fout.close()
    fin.close()
print("Finished")