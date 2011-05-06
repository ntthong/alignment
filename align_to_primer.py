#!/usr/local/bin/python3

HELP_STRING = """
align_to_primer.py

Author: Stirling Churchman
Date: December 29, 2009

     -h     print this help message
     -s     sequencing file input (required)
     -l     primer sequence(required)
     -o     output file with primer removed (required)
     -r     output file of reads w/o primer (required)

"""
import sys
import difflib
from getopt import getopt


def main(argv=None):
    if argv is None:
        argv = sys.argv

    sequenceFile = ""
    libFile = ""
    outFile = ""
    origFile = ""
    print_stats = 0
    perfect = 0

    try:
        optlist, args = getopt(argv[1:], "hs:l:o:r:")
    except:
        print ""
        print HELP_STRING
        sys.exit(1)

    if len(optlist) == 0:
        print ""
        print HELP_STRING
        sys.exit(1)

    for (opt, opt_arg) in optlist:

        if opt == '-h':
            print ""
            print HELP_STRING
            sys.exit(1)
        elif opt == '-s':
            sequenceFile = opt_arg
        elif opt == '-l':
            libFile = opt_arg
        elif opt == '-o':
            outFile = opt_arg
        elif opt == '-r':
            origFile = opt_arg

    if sequenceFile == "":
        print HELP_STRING
        sys.exit(1)
    if libFile == "":
        print HELP_STRING
        sys.exit(1)
    if outFile == "":
        print HELP_STRING
        sys.exit(1)
    if origFile == "":
        print HELP_STRING
        sys.exit(1)

    # read in RT primer
    libFile = file(libFile, 'r')
    primer = libFile.readline()
    primer_length = len(primer)
    min_primer_match = 10
    max_offset = 1
    min_insert_size = 18
    seed_length = 25
    seqInfo =[]
    seqFile = file(sequenceFile,'r')
    for i in range(4):
        seqInfo.append(seqFile.readline())


    o1File = open(outFile, 'w')
    o2File = open(origFile, 'w')
    line_num = 1
    #for k in range(10):
    while seqInfo[0] != '' :

        if line_num%100000==0:
            print line_num
        line = seqInfo[1]
        s = difflib.SequenceMatcher(None, line, primer)
        alignment = s.find_longest_match(0, len(line)-1, 0, primer_length-1)
        if alignment[2] <min_primer_match or alignment[1] >=max_offset:
            for entry in seqInfo:
                o2File.write(entry)
        elif alignment[0] >min_insert_size:
            if alignment[0]<=seed_length:
                o1File.write(seqInfo[0])
                o1File.write(line[0:alignment[0]]+'\n')
                o1File.write(seqInfo[2])
                o1File.write(seqInfo[3])
            else:
                o1File.write(seqInfo[0])
                o1File.write(line[0:seed_length]+'\n')
                o1File.write(seqInfo[2])
                o1File.write(seqInfo[3])
        # sequences are every fourth line
        seqInfo = []
        for i in range(4):
            seqInfo.append(seqFile.readline())
        line_num += 1

    seqFile.close()
    o1File.close()
    o2File.close()

##############################################
if __name__ == "__main__":
    sys.exit(main())
