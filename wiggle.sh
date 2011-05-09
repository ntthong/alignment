#!/bin/bash

export PYTHONROOT="/Users/jsh/proj/churchman_align"
echo "Finding python directory ${PYTHONROOT}"


ARRAY2=( 'WT_NT')

ARRAY=( 'WT_NT1.align1.txt,WT_NT2.align1.txt,WT_NT3.align1.txt,WT_NT4.align1.txt,WT_NT5.align1.txt,WT_NT1.align2.txt,WT_NT2.align2.txt,WT_NT3.align2.txt,WT_NT4.align2.txt,WT_NT5.align2.txt')

ARRAY3=( 0)
# get number of elements in the array
ELEMENTS=${#ARRAY[@]}
cp ${PYTHONROOT}/bowtie_align_wiggle.py .

for (( i=0;i<$ELEMENTS;i++)); do
    echo ${ARRAY[${i}]}
    echo ${ARRAY2[${i}]}
    ${PYTHONROOT}/bowtie_align_wiggle.py -f ${ARRAY[${i}]} -o ${ARRAY2[${i}]} -m ${ARRAY3[${i}]}
done

