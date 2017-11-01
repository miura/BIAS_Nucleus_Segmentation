'''
Processes a single flat tex file (the file given as an argument). Scans for lstinputlisting command and that command is replaced by lstlisting with injected code. 
'''
import fileinput
import re, sys, os


MOCKURL = 'http://www.example.com/'
CODEEXT = 'ijm'
#f = 'mod2all.tex'
#f = 'mod3merged.tex'
argfilename = sys.argv[1] # name of a .tex file, which should be scanned and injected with codes. 
f = argfilename

def processOneFile(f):
    ffile = os.path.basename(f)
    fbasename = os.path.splitext(f)[0] # filename without extension
    outfilename = fbasename + 'WithCodes.tex'
    parentdir = os.path.dirname(f)
    lines  = [line.rstrip('\n') for line in open(f)]
    out =  ''
    for ll in lines:
        matched = re.match(r"(.*)\\lstinputlisting(\[.*\])?{(.*\." + CODEEXT + ")}", ll)
        if matched:
            # print matched.group()
            pref = matched.group(1)
            options = matched.group(2)
            contents = matched.group(3)
            #contents = os.path.join( parentdir, os.path.basename(contents)) # in Authorea, ijm files are moved to the root
            contentsEscaped = contents.replace("_", "\\_")
            print contents
            codeurl = "\\href{" + MOCKURL + "contents}{" + contentsEscaped +"}"
            with open(contents, 'r') as file:
                codedata = file.read()

            if not options:
                options = ''
            newtext = pref + '\n' \
                    '\\begin{lstlisting}' + options + '\n' + \
                    codedata + '\n' + \
                    '\\end{lstlisting}' + '\n' \
                    '\\textbf{sourcecode}: ' + codeurl
            # print newtext
            out = out + newtext + '\n'
        else:
            out = out + ll + '\n'

    with open(f, 'w') as f2:
        f2.write(out)

processOneFile(f)


