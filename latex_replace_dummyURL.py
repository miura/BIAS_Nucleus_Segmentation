'''
batch proceess tex file to replace a url www.example.com with specified URL. 
scans though fragmented tex file in Authorea repository

works from any directory

20171025 Kota @ NEUBIAS WG6 project
'''

import fileinput
import re, os, sys

argfilename = sys.argv[1] # assume that the first argument is layout.md
githubURL = sys.argv[2] # for example

def processOneFile(f, githubURL):
    ffile = os.path.basename(f)
    fbasename = os.path.splitext(f)[0] # filename without extension
    parentdir = os.path.dirname(f)
    with open(f, 'r') as file:
        contents = file.read()
    #print contents
    tt = re.compile(r".*href{http:\/\/(.*\/)+.*}{.*\/(.*)}")
    matched = re.search(tt, contents)
    if matched:
        filename = matched.group(2).replace("\\", "")
        #print filename
        httppattern = r"(http:\/\/www\.example\.com\/contents)}({.*\/(.*)})"
        contents = re.sub(httppattern, githubURL + filename + "}\g<2>", contents)
        #print contents
        with open(f, 'w') as file:
            file.write(contents)
        print "replaced --- ", f, " ---- ", filename
    else:
        print "-------- --- ", f

def batchProcessTexFiles(layoutmd, githubURL):
    parentdir = os.path.dirname(layoutmd)
    lines  = [line.rstrip('\n') for line in open(layoutmd)]
    for ll in lines:
        if ll.endswith('.tex'):
            targettex = os.path.join(parentdir, ll)
            #print targettex
            processOneFile(targettex, githubURL)
        #else:
            #print ll


#f = 'mod3merged.tex'
#f = argfilename
#layoutmd = argfilename
batchProcessTexFiles(argfilename, githubURL)
#processOneFile(argfilename, githubURL)


