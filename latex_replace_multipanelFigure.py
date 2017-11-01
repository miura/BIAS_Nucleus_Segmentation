'''
Replaces the figure with subfigures with figure linking a single PDF with those subfigure images merged as a single file.

Scans though merged tex file and look for a figure with a specified label (\label{<argument>})
For that detected figure
1. cut and paste the figure block to a simple tex document only for that figure. 
2. compiled this figure tex file as a single PDF
3. that PDF is inserted in the search .tex file as a figure at the position where the figure with subfigure was. 

20171023-5 Kota @ NEUBIAS WG6 project
'''

import fileinput
import re, os, sys, subprocess

#FIGURE_TEMPLATE_PATH = "/Users/miura/Dropbox/templates/latex_templates/template-standalone-figure.tex"
FIGURE_TEMPLATE_PATH = "template-standalone-figure.tex"
targettex = sys.argv[1] # target tex file, to be replaced with subfigured block. 
figlabel = sys.argv[2] # the second argument is the figure label fig:XXXX - without "fig:" prefix
#f = 'mod2all.tex'

def processOneFile(tex, lab):
    ffile = os.path.basename(tex)
    fbasename = os.path.splitext(tex)[0] # filename without extension
    outfilename = fbasename + 'fig-' + lab + '.tex'
    outpdfname = fbasename + 'fig-' + lab + '.pdf'
    outmergedfilename =  fbasename + 'subfigreplaced.tex'
    parentdir = os.path.dirname(tex)
    print(outfilename)
    #lines  = [line.rstrip('\n') for line in open(f)]
    # Read in the file
    with open(tex, 'r') as file :
      filedata = file.read()

    # match the target string
    #matched = re.search(r"^.*(\\begin{figure}.+)(?:\n.+\\.+)+(\n.*\\label{fig:NucOverlayDilate}.*(?:\n.+)+\\end{figure})", filedata, re.MULTILINE)
    #regex = r"^.*(\\begin{figure}(.+))((?:\n.+\\.+)+)(\n.*\\label{fig:"+lab+"}.*(?:\n.+)+\\end{figure})"
    regex = r"^.*(\\begin{figure}(.+))((?:\n.+\\.+)+)(\n.*\\caption.*(?:\n+)*)(\n.*\\label{fig:"+lab+"}.*(?:\n.+)+\\end{figure})"
    compiledRe = re.compile(regex, re.MULTILINE)
    #matched = re.search(r"^.*(\\begin{figure}(.+))((?:\n.+\\.+)+)(\n.*\\label{fig:"+lab+"}.*(?:\n.+)+\\end{figure})", filedata, re.MULTILINE)
    matched = re.search(compiledRe, filedata)
    if matched is None:
        print("no match found with label", lab)
    else:
        figureblock = matched.group(0)
        fighead = matched.group(1)
        figureposition = matched.group(2)
        subfigblock = matched.group(3)
        figcaption = matched.group(4)
        figlabel = matched.group(5)
        #figureblock = figureblock.replace("\\", "\\\\")  # avoid latex markup recognized as escape in python
        matchedInner = re.search(r"^.*(\centering)((?:\n.+)+)(\n.+caption)", figureblock, re.MULTILINE)
        if matchedInner is None:
            print("no match for subfoats")
        else: 
            #subfigblock = matchedInner.group(2)
            subfigblock = subfigblock.replace("\\", "\\\\")
            print("====== extracted block backslash replaced")
            print subfigblock
            with open(FIGURE_TEMPLATE_PATH, 'r') as file :
                templatedata = file.read()
                #replacedTex = re.sub(r"%placeholder1", figureposition, templatedata)
                replacedTex = re.sub(r"%placeholder2", subfigblock, templatedata)
                print("====== template figure tex replaced with contents")
                print(replacedTex)
                print("====== removed with individual labels")
                # remove \label markup. this interferes with standalone document class
                matchIndLabel = re.compile(r"(^.*\\subfloat\[.*\]{)(\\label.*\})(\\include)", re.MULTILINE) 
                replacedTex = re.sub(matchIndLabel, r"\1\3", replacedTex)
                # adjust size. 
                replacedTex = re.sub(r"(.*includegraphics\[)height(.*)\]", r"\1height= 2in]", replacedTex, re.MULTILINE)
                print(replacedTex)
            # write figure text file. to be compiled as a PDF. 
            with open(outfilename, 'w') as file:
                file.write(replacedTex)
            # compile figure PDF
            subprocess.check_call(['pdflatex', outfilename]) #-output-directory
            newinnerFigBlock = \
                    fighead + "\n" + \
                    "\\centering" + "\n" + \
                    "\\includegraphics[width=3in]{" + \
                    os.path.basename(outpdfname) + \
                    "}\n" + \
                    figcaption + "\n" + \
                    figlabel + "\n"
            newinnerFigBlock = newinnerFigBlock.replace("\\", "\\\\")
            print("====== contents for injection")
            print(newinnerFigBlock)
            replacedfiledata = re.sub(compiledRe, newinnerFigBlock, filedata)
            print("==== writing replaced file")
            #print(replacedfiledata)
            #with open(outmergedfilename, 'w') as file:
            with open(tex, 'w') as file:
                file.write(replacedfiledata)

def batchProcessTexFiles(layoutmd):
    parentdir = os.path.dirname(layoutmd)
    lines  = [line.rstrip('\n') for line in open(layoutmd)]
    for ll in lines:
        if ll.endswith('.tex'):
            targettex = os.path.join(parentdir, ll)
            print ( targettex )
            processOneFile(targettex)
        else:
            print ( ll )


layoutmd = figlabel
#batchProcessTexFiles(layoutmd)
processOneFile(targettex, figlabel)


