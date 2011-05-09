#!/bin/bash

export PYTHONROOT="/Users/jsh/proj/churchman_align/"
echo "Finding python directory ${PYTHONROOT}"
export PRIMERROOT="/Users/jsh/proj/churchman_align/genomes/"

# Change this directory!!
export OUTPUTDIR="/Users/jsh/proj/churchman_align/output/"
# Change this directory!!
export DATAROOT="/Users/jsh/proj/churchman_align/rawdata/stirlingchurchman_NETseq_files1/"

cd ${DATAROOT}
cp ${PYTHONROOT}align_to_primer.py ${OUTPUTDIR}

for f in $( ls *.fastq ); do
        echo $f
        ${PYTHONROOT}align_to_primer.py -s $f -l  ${PRIMERROOT}oLSC003.fna \
            -o ${OUTPUTDIR}${f/"fastq"/"trimmed.fastq"} -r ${OUTPUTDIR}${f/"fastq"/"orig.fastq"} &
done

