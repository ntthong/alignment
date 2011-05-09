#!/usr/local/bin/python3

HELP_STRING = """
bowtie_stats.py

Author: Stirling Churchman
Date: April 20, 2010


     -h     print this help message
     -f     input files, comma separated list (required)
     -o     output file (required)

"""


import sys
from getopt import getopt
from align_functions import recordAlignment
import time as t

def main(argv=None):
    if argv is None:
        argv = sys.argv

    inputFiles = ""

    outputFile = ""
   # number_files = 1
    sj_on=0

    try:
        optlist, args = getopt(argv[1:], "hf:o:")
    except:
        print("")
        print(HELP_STRING)
        sys.exit(1)

    if len(optlist) == 0:

        print("")
        print(HELP_STRING)
        sys.exit(1)

    for (opt, opt_arg) in optlist:
        #print opt
        #print opt_arg
        if opt == '-h':
            print("")
            print(HELP_STRING)
            sys.exit(1)
       # elif opt == '-n':
        #    number_files = opt_arg
         #   for i in range(number_files):
          #      inputFile[i]=""
        elif opt == '-f':
            inputFiles = opt_arg.split(',')

        elif opt == '-o':
            outputFile = opt_arg


    if inputFiles == "" or outputFile == "" :
        print(HELP_STRING)
        sys.exit(1)


    print(inputFiles)
    logFile = 'log-all-bowtie.txt'
    stats={}
    condition=['trimmed','trimmed_tRNA','trimmed_rRNA',\
                   'orig','orig_tRNA','orig_rRNA']
    for lane in inputFiles:
        base = lane[-14:-11]
        if base in stats:continue
        stats[base]={}
        filecondition={}
        for item in condition:
            filecondition[base+item] = item
        if '/' not in lane:
            statFile = logFile
        else:
            statFile = lane[:-14]+logFile
        sFile=open(statFile, 'r')
        line = sFile.readline().replace('\n','')
        while line != '':
            #print line
            #print base+'_trimmed.txt'
            if line == base+'_trimmed.txt':
                reads_processed=sFile.readline().split(':')
                stats[base]['trimmed']=int(reads_processed[1])
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['trimmed_tRNA']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            if line == base+'_trimmed_tRNA.txt':
                reads_aligned = sFile.readline().split(':')
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['trimmed_rRNA']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            if line == base+'_trimmed_rRNA.txt':
                reads_aligned = sFile.readline().split(':')
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['trimmed_align']=int(reads_aligned[0])
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['trimmed_notalign']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            if line == base+'_orig.txt':
                reads_processed=sFile.readline().split(':')
                stats[base]['orig']=int(reads_processed[1])
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['orig_tRNA']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            if line == base+'_orig_tRNA.txt':
                reads_aligned = sFile.readline().split(':')
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['orig_rRNA']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            if line == base+'_orig_rRNA.txt':
                reads_aligned = sFile.readline().split(':')
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['orig_align']=int(reads_aligned[0])
                reads_aligned = sFile.readline().split(':')
                reads_aligned = reads_aligned[1].split('(')
                stats[base]['orig_notalign']=int(reads_aligned[0])
                line = sFile.readline().replace('\n','')
            line=sFile.readline().replace('\n','')
    oFile = open(outputFile+'_stats.txt', 'w')
    condition_raw=0
    condition_align=0
    condition_tRNA=0
    condition_rRNA=0
    condition_link=0
    condition_nolink=0
    for base in stats:
        total_align=stats[base]['trimmed_align']+stats[base]['orig_align']
        total_reads=stats[base]['trimmed']+stats[base]['orig']
        condition_align+=total_align
        condition_raw+=total_reads
        condition_tRNA+=stats[base]['trimmed_tRNA']+stats[base]['orig_tRNA']
        condition_rRNA+=stats[base]['trimmed_rRNA']+stats[base]['orig_rRNA']
        condition_link+=stats[base]['trimmed']
        condition_nolink+=stats[base]['orig']
        oFile.write(base+'\t total number\t fraction of total\n')
        oFile.write('number of reads\t%s\t%s\n'%(total_reads, float(total_reads)/total_reads))
        oFile.write('trimmed \t%s\t%s\n'%(stats[base]['trimmed'], float(stats[base]['trimmed'],)/total_reads))
        oFile.write('trimmed tRNA\t%s\t%s\n'%(stats[base]['trimmed_tRNA'], float(stats[base]['trimmed_tRNA'],)/total_reads))

        oFile.write('trimmed rRNA\t%s\t%s\n'%(stats[base]['trimmed_rRNA'], float(stats[base]['trimmed_rRNA'],)/total_reads))
        oFile.write('trimmed aligned\t%s\t%s\n'%(stats[base]['trimmed_align'], float(stats[base]['trimmed_align'],)/total_reads))
        oFile.write('trimmed not aligned\t%s\t%s\n'%(stats[base]['trimmed_notalign'], float(stats[base]['trimmed_notalign'],)/total_reads))


        oFile.write('orig \t%s\t%s\n'%(stats[base]['orig'], float(stats[base]['orig'],)/total_reads))
        oFile.write('orig tRNA\t%s\t%s\n'%(stats[base]['orig_tRNA'], float(stats[base]['orig_tRNA'],)/total_reads))

        oFile.write('orig rRNA\t%s\t%s\n'%(stats[base]['orig_rRNA'], float(stats[base]['orig_rRNA'],)/total_reads))
        oFile.write('orig aligned\t%s\t%s\n'%(stats[base]['orig_align'], float(stats[base]['orig_align'],)/total_reads))
        oFile.write('orig not aligned\t%s\t%s\n'%(stats[base]['orig_notalign'], float(stats[base]['orig_notalign'],)/total_reads))
    oFile.write('-----------------------------------\n')
    oFile.write('total raw sequences\t%s\n' % condition_raw)
    oFile.write('total aligned\t%s\t%s\n' % (condition_align,float(condition_align)/condition_raw))
    oFile.write('total tRNA\t%s\t%s\n' % (condition_tRNA,float(condition_tRNA)/condition_raw))
    oFile.write('total rRNA\t%s\t%s\n' % (condition_rRNA,float(condition_rRNA)/condition_raw))
    oFile.write('total linker\t%s\t%s\n' % (condition_link,float(condition_link)/condition_raw))
    oFile.write('total no linker\t%s\t%s\n' % (condition_nolink,float(condition_nolink)/condition_raw))
    oFile.close()


##############################################
if __name__ == "__main__":
    sys.exit(main())
