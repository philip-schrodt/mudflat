# mudflat/FJOLTYNG Documentation
Last update: 10 January 2019

## Whatzit??
This is the start of the documentation for the program, and is mostly being used to store drafts, pretty much generated
on the fly, for what will eventually be more coherent documentation. Also it is not likely to be fully synchronized
with the current commit of the code. Which is to say in the current form it is almost but not quite useless.

## Input format
The input format is what might be called "readable JSON", which is to say individual JSON records with internal
line breaks for readability without the white-space brittleness of YAML. Examples [will eventually] follow.
In Python this can be read with the relatively simple
```
import json
JSONFILENAME = "newformat.test.txt"

def read_json_file():
# generator for reading readable JSON
    jstr = ""
    for line in open(JSONFILENAME, "r"):
        if line.startswith("}"):
            yield json.loads(jstr + "}")  # returns JSON record as a dictionary
            jstr = ""
        else:
            if "\t" in line:
                line = line.replace("\t", "\\t")  # similar code if anything else needs to be double-escaped
            jstr += line[:-1].strip()

reader = read_json_file()
for jdict in reader:
    # do stuff with jdict here...
```

## Legal stuff

### Programmer: 
Philip A. Schrodt  
Parus Analytics  
Charlottesville, VA, 22901 U.S.A.  
http://parusanalytics.com

Copyright (c) 2019	Philip A. Schrodt.	All rights reserved.

Report bugs to: schrodt735@gmail.com


### Creative Commons License
This work is licensed under a Creative Commons Attribution-NonCommercial 4.0 International License.

## REVISION HISTORY:
10-Jan-2019:	Initial version
