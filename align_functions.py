def getInsertLength(genomeFile,alignFile,align_length,seq_length,primer,min_primer,MMlim):
    Comp = {'C':'g','G':'c','A':'t','T':'a', 'N':'n'}
# read in genome
    intron_seq = {}
    intron_length = {}
    intron_RT = {}
    inFile = file(genomeFile, 'r')
    line = inFile.readline()
    
    while line != "":
        line2 = inFile.readline()
        line2 = line2.replace('\n','')
        line = line.replace('\n','')
        intron_seq[line[1:]]=line2
        intron_length[line[1:]]=len(line2)
        intron_RT[line[1:]]=[]
        line = inFile.readline()
    
   
    for i,line in enumerate(open(alignFile)):
        geneinfo = line.replace('\n','').split('\t')
        if i%1000==0:
            print(i)
        # check to see whether alignment is to end of intron
        if int(geneinfo[3])+align_length==intron_length[geneinfo[2]]-1:
            print('found one!')
            print(geneinfo)
            print(intron_length[geneinfo[2]]-align_length)
            # now find full read sequence
            not_found = 1
            sequence = geneinfo[4]
            
            intron = intron_seq[geneinfo[2]]
            MM=0
            for i,base in enumerate(sequence[align_length:-min_primer]):
                if MM <= MMlim:
                    if sequence[align_length+i:align_length+1+min_primer]==primer[:min_primer]:
                        intron_RT[geneinfo[2]].append(align_length+i)
                    elif Comp[base] != intron[-align_length-1]:
                        MM+=1
            if MM<=MMlim:
                intron_RT[geneinfo[2]].append(intron_length[geneinfo[2]]-min_primer)
                
    return intron_RT

def sortThroughAlignments(alignFile):
    read_names = []
    all_align = {}
    read_names = []
    mult_align = {}
    not_exon = []
    filter_reads=[]
    for i,line in enumerate(open(alignFile)):
        if i%100000==0:print(i)
        aligninfo = line.replace('\n','').split('\t')
        if aligninfo[0] in read_names:
            if aligninfo[0] in mult_align:
                mult_align[aligninfo[0]].append(aligninfo)
            else:
                mult_align[aligninfo[0]]=aligninfo
                mult_align[aligninfo[0]].append(all_align[aligninfo[0]])
        else:
            if len(read_names) > 1000:
                all_align.pop(read_names[0])
                read_names.pop(0)
            read_names.append(aligninfo[0])
            all_align[aligninfo[0]]=aligninfo
            
    for read in mult_align:
        num_alignments = len(mult_align[read])
        if num_alignments <3:
            for alignment in mult_align[read]:
                if '_' in alignment[2]:
                    not_exon.append(read)
                    break
        if read not in not_exon:
            filter_reads.append(read)
    return [filter_reads,not_exon]
            
def recordAlignment(position_sum1,position_sum2,alignment):
    chromosome = alignment[0]
    pos = alignment[1]
    exon = alignment[2]
    read_length = alignment[3]
    sign2 = alignment[4] #+, 1; -, 0
    armLength=36
    if exon:
        print('exon found!')
        print(alignment)
        fields = chromosome.split('_')
        chr = fields[1]
        juncPos=int(fields[2])
        strand=fields[3]
        if strand =='+':
            if chr not in position_sum1:
                position_sum1[chr]={}
            location = juncPos-armLength+1+pos+read_length
            if location in position_sum1[chr]:
                position_sum1[chr][location]+=1
            else:
                position_sum1[chr][location]=1
        else:
            if chr not in position_sum2:
                position_sum2[chr]={}
            location = juncPos+armLength-1-pos
            if location in position_sum2[chr]:
                position_sum2[chr][location]+=1
            else:
                position_sum2[chr][location]=1    
    else:
        if sign2:
            # after converting my RNA libraries to DNA libraries, I end up
            # sequencing the RC of the original RNA molecule. So reads aligning
            # to the minus strand are now marked as being on the plus strand
            if chromosome not in position_sum2:
                position_sum2[chromosome]={}
            # bowtie alignments are zero-based and wiggle files are 1 based
            location = pos+1
            if location in position_sum2[chromosome]:
                position_sum2[chromosome][location]+=1
            else:
                position_sum2[chromosome][location]=1
                
        elif not sign2:
            if chromosome not in position_sum1:
                position_sum1[chromosome]={}
            # you add the read length because of the way that bowtie aligns 
            # to the reverse reference strand
            location = pos+read_length
            if location in position_sum1[chromosome]:
                position_sum1[chromosome][location]+=1
            else:
                position_sum1[chromosome][location]=1
        else:
            print(sign2)
def removeAlignment(position_sum1,position_sum2,alignment):
    chromosome = alignment[0]
    pos = alignment[1]
    exon = alignment[2]
    read_length = alignment[3]
    sign2 = alignment[4] #+, 1; -, 0
    armLength=36
    if exon:
        print('exon found!')
        print(alignment)
        fields = chromosome.split('_')
        chr = fields[1]
        juncPos=int(fields[2])
        strand=fields[3]
        if strand =='+':
            if chr not in position_sum1:
                position_sum1[chr]={}
            location = juncPos-armLength+1+pos+read_length
            if location in position_sum1[chr]:
                position_sum1[chr][location]+=1
            else:
                position_sum1[chr][location]=1
        else:
            if chr not in position_sum2:
                position_sum2[chr]={}
            location = juncPos+armLength-1-pos
            if location in position_sum2[chr]:
                position_sum2[chr][location]+=1
            else:
                position_sum2[chr][location]=1    
    else:
        if sign2:
            # after converting my RNA libraries to DNA libraries, I end up
            # sequencing the RC of the original RNA molecule. So reads aligning
            # to the minus strand are now marked as being on the plus strand
            if chromosome not in position_sum2:
                position_sum2[chromosome]={}
            # bowtie alignments are zero-based and wiggle files are 1 based
            location = pos+1
            if location in position_sum2[chromosome]:
                position_sum2[chromosome][location]-=1
            else:
                print('wtf')
                print(alignmen)
                
        elif not sign2:
            if chromosome not in position_sum1:
                position_sum1[chromosome]={}
            # you add the read length because of the way that bowtie aligns 
            # to the reverse reference strand
            location = pos+read_length
            if location in position_sum1[chromosome]:
                position_sum1[chromosome][location]-=1
            else:
                print('wtf2')
                print(alignment)
        else:
            print('wtf3')
            print(sign2)
