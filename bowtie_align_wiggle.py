#!/usr/local/bin/python3

HELP_STRING = """
bowtie_align_wiggle.py

Author: Stirling Churchman
Date: October 12, 2009
Updated: February 25, 2010 to deal with multiple alignments
Updated: March 4, 2010 to try and deal with splice junctions. Doesn't work so
sj_on should always be set to 0.


     -h     print this help message
     -f     input files, comma separated list (required)
     -o     output file (required)
     -m     include splice junctions
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
        optlist, args = getopt(argv[1:], "hf:o:m:")
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
        elif opt == '-m':
            sj_on = int(opt_arg)

    if inputFiles == "" or outputFile == "" :
        print(HELP_STRING)
        sys.exit(1)


    print(inputFiles)
    chr = {1:'chrI', 2:'chrII', 3:'chrIII', 4:'chrIV', 5:'chrV', 6:'chrVI', 7:'chrVII', 8:'chrVIII', 9:'chrIX', 10:'chrX',
           11:'chrXI', 12:'chrXII', 13:'chrXIII', 14:'chrXIV', 15:'chrXV', 16:'chrXVI', 17:'chrMito', 18:'2-micron'}

    position_sum1 = {}
    position_sum2 = {}
    totalReads=0

    print("sj_on is %s" % sj_on)

    for inputFile in inputFiles:
        print(inputFile)
        seqAlignments = {}
        for i,line in enumerate(open(inputFile)):
            if i%500000==0:
                print(i)
            fields = line.split('\t')
            if fields[0] in seqAlignments:
                seqAlignments[fields[0]].append(fields)
            else:
                seqAlignments[fields[0]]=[fields]

        for seq in seqAlignments:
            flag=0
            if len(seqAlignments[seq])==1:
                fields = seqAlignments[seq][0]
                sign = fields[1]
                if sign[-1] == '+':
                    sign2 = 1
                elif sign[-1] == '-':
                    sign2 = 0
                if '_' in fields[2]:
                    if sign2==1:continue
                    exon=1
                else:exon=0
                chromosome = fields[2]
                pos = int(fields[3])
                #print fields[4]
                read_length = len(fields[4])
                alignment = [chromosome,pos,exon,read_length,sign2]
                if (not exon or sj_on):
                    recordAlignment(position_sum1,position_sum2,alignment)
                    totalReads+=1
                else:continue
            elif len(seqAlignments[seq])==2:
                #determine whether one is an exon otherwise continue
                exon = [0, 0]
                fields = seqAlignments[seq]
                if '_' in fields[0][2]:
                    if fields[0][1]== '+':flag=1
                    exon[0]=1
                else:exon[0]=0
                if '_' in fields[1][2]:
                    if fields[1][2]=='+':flag=1
                    exon[1]=1
                else:exon[1]=0
                if sum(exon) == 1:
                    if sj_on and not flag:
                        if exon[0]:index=0
                        else:index=1
                    else:
                        if exon[0]:index=1
                        else:index=0
                    chromosome = fields[index][2]
                    pos = int(fields[index][3])
                    read_length = len(fields[index][4])
                    sign = fields[index][1]
                    if sign[-1] == '+':
                        sign2 = 1
                    elif sign[-1] == '-':
                        sign2 = 0
                    alignment = [chromosome,pos,exon[index],read_length,sign2]
                    recordAlignment(position_sum1,position_sum2,alignment)
                    totalReads+=1
                else:continue
            elif len(seqAlignments[seq])>2:
                continue


    #Output a wiggle file. These locations are 1 relative
    filename = 'w_'+outputFile+'_plus.wig'
    outFile1= open(filename, 'w')
    outFile1.write('track type=wiggle_0')
    outFile1.write('\n')
    filename = 'w_'+outputFile+'_minus.wig'
    outFile2= open(filename, 'w')
    outFile2.write('track type=wiggle_0')
    outFile2.write('\n')
    for chr_num in range(1,18):
        chromosome = chr[chr_num]
        if chromosome not in ['chrMito']:
            outFile1.write('variableStep chrom=%s' % chromosome)
            outFile1.write('\n')
            loc_dic = position_sum1[chromosome]
            locations = list(loc_dic.keys())
            locations.sort()
            for l in locations:
                outFile1.write('%s %s' % (l, loc_dic[l]))
                outFile1.write('\n')
            outFile2.write('variableStep chrom=%s' % chromosome)
            outFile2.write('\n')
            loc_dic = position_sum2[chromosome]
            locations = list(loc_dic.keys())
            locations.sort()
            for l in locations:
                outFile2.write('%s %s' % (l, loc_dic[l]))
                outFile2.write('\n')
    outFile1.close()
    outFile2.close()

    #output a normalized wig file
    # The data in this file have units of 'reads per normFactor
    # eg. reads per 10 million
    normFactor = 10000000
    filename = 'w_'+outputFile+'_norm_plus.wig'
    outFile1= open(filename, 'w')
    outFile1.write('track type=wiggle_0')
    outFile1.write('\n')
    filename = 'w_'+outputFile+'_norm_minus.wig'
    outFile2= open(filename, 'w')
    outFile2.write('track type=wiggle_0')
    outFile2.write('\n')
    for chr_num in range(1,18):
        chromosome = chr[chr_num]
        if chromosome not in ['chrMito']:
            outFile1.write('variableStep chrom=%s' % chromosome)
            outFile1.write('\n')
            loc_dic = position_sum1[chromosome]
            locations = list(loc_dic.keys())
            locations.sort()
            for l in locations:
                outFile1.write('%s %s' % (l, normFactor*float(loc_dic[l])/totalReads))
                outFile1.write('\n')
            outFile2.write('variableStep chrom=%s' % chromosome)
            outFile2.write('\n')
            loc_dic = position_sum2[chromosome]
            locations = list(loc_dic.keys())
            locations.sort()
            for l in locations:
                outFile2.write('%s %s' % (l, normFactor*float(loc_dic[l])/totalReads))
                outFile2.write('\n')
    outFile1.close()
    outFile2.close()

    #output a track file for subsequent analysis. Here zeros are listed.
    #The read counts are normalized as above.

    filename = 't_'+outputFile+'_plus.txt'
    outFile1= open(filename, 'w')
    filename = 't_'+outputFile+'_minus.txt'
    outFile2= open(filename, 'w')
    chr_seek1=[]
    chr_seek2=[]
    chrSizeFile= '/Users/jsh/proj/churchman_align/chrSize.txt'
    chrSize = {}
    for line in open(chrSizeFile):
        fields=line.replace('\n','').split('\t')
        chrSize[fields[0]]=int(fields[1])

    for chr_num in range(1,18):
        chromosome = chr[chr_num]
        if chromosome not in ['chrMito']:
            chr_seek1.append((chromosome,outFile1.tell()))

            outFile1.write('chrom=%s' % chromosome)
            outFile1.write('\n')
            for i in range(chrSize[chromosome]):
                if i+1 in position_sum1[chromosome]:
                    outFile1.write('%s\n' % (normFactor*float(position_sum1[chromosome][i+1])/totalReads))
                else:  outFile1.write('%s\n' % (0))


            chr_seek2.append((chromosome,outFile2.tell()))
            outFile2.write('chrom=%s' % chromosome)
            outFile2.write('\n')
            for i in range(chrSize[chromosome]):
                if i+1 in position_sum2[chromosome]:
                    outFile2.write('%s\n' % (normFactor*float(position_sum2[chromosome][i+1])/totalReads))
                else:  outFile2.write('%s\n' % (0))

    #outFile1.close()
    #outFile2.close()
    #filename ='t_'+outputFile+'_plus_index.txt'
    #outFile1= open(filename, 'w')
    #filename = 't_'+outputFile+'_minus_index.txt'
    #outFile2= open(filename, 'w')
    #for i,pos in enumerate(chr_seek1):
    #    outFile1.write('%s,%s\n' % pos)
    #    outFile2.write('%s,%s\n' % chr_seek2[i])
    #outFile1.close()
    #outFile2.close()


##############################################
if __name__ == "__main__":
    sys.exit(main())
