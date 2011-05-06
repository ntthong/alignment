#!/usr/local/bin/python3

HELP_STRING = """
TSS_index.py

Author: Stirling Churchman
Date: March 4, 2010
     -f     track file base to be indexed

     -h     print this help message

"""

import sys

from getopt import getopt



def main(argv=None):
    if argv is None:
        argv = sys.argv
    trackFilename=''



    try:
        optlist, args = getopt(argv[1:], "hf:")
    except:
        print ""
        print HELP_STRING
        sys.exit(1)


    for (opt, opt_arg) in optlist:
        if opt == '-h':
            print ""
            print HELP_STRING
            sys.exit(1)
        elif opt == '-f':
            trackFilename=opt_arg



    if trackFilename == "":
        print HELP_STRING
        sys.exit(1)

#    TSSFile = open(TSSFilename, 'r')
    chrIndex={}
    trackFile1 = open(trackFilename+'_plus.txt','r')
    trackFile2 = open(trackFilename+'_minus.txt','r')

    for i in range(16):
        line=trackFile1.readline()
        while '=' not in line: line=trackFile1.readline()
        line2=trackFile2.readline()
        while '=' not in line2: line2=trackFile2.readline()
        chr2=line2.replace('\n','').split('=')
        chr2=chr2[1]
        chr1=line.replace('\n','').split('=')
        chr1=chr1[1]
        if chr2 != chr1: print chr1,chr2
        chrIndex[chr1]= [trackFile1.tell(), trackFile2.tell()]



    filename = trackFilename+'_chrindex.txt'
    outFile1= open(filename, 'w')


    #output format:
    # chr startindex+   startindex-
    for name in chrIndex:

        outFile1.write('%s\t%s\t%s\n' % (name,chrIndex[name][0],chrIndex[name][1]))

    outFile1.close()


##############################################
if __name__ == "__main__":
    sys.exit(main())
