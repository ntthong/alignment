#!/bin/bash

export PYTHONROOT="/Users/jsh/proj/churchman_align/"
echo "Finding python directory ${PYTHONROOT}"
export PRIMERROOT="/Users/jsh/proj/churchman_align/genomes/"

# Change this directory!!
export OUTPUTDIR="/Users/jsh/proj/churchman_align/output"
# Change this directory!!
export DATAROOT="/Users/jsh/proj/churchman_align/rawdata"

cd ${DATAROOT}
cp ${PYTHONROOT}align_to_primer.py ${OUTPUTDIR}

for f in $( ls s_?_sequence.txt ); do
        echo $f
        ${PYTHONROOT}align_to_primer.py -s $f -l  ${PRIMERROOT}oLSC003.fna \
            -o ${OUTPUTDIR}${f/"sequence.txt"/"trimmed.txt"} -r ${OUTPUTDIR}${f/"sequence.txt"/"orig.txt"} &
done

