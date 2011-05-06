#!/bin/bash

export PYTHONROOT="/Users/stirls/lib/python/file_manipulation"
echo "Finding python directory ${PYTHONROOT}"


ARRAY2=( 'mRNA_WT' 'IP_WT')

ARRAY=( 's_1_align1.txt,s_1_align2.txt,s_2_align1.txt,s_2_align2.txt,s_3_align1.txt,s_3_align2.txt,../../../091007/Alignment/100225/s_5_align1.txt,../../../091007/Alignment/100225/s_5_align2.txt' \
's_7_align1.txt,s_7_align2.txt,s_6_align1.txt,s_6_align2.txt,s_5_align1.txt,s_5_align2.txt,s_4_align1.txt,s_4_align2.txt,../../../091007/Alignment/100225/s_6_align1.txt,../../../091007/Alignment/100225/s_6_align2.txt')


# get number of elements in the array
ELEMENTS=${#ARRAY[@]}
cp ${PYTHONROOT}/bowtie_stats.py .

for (( i=0;i<$ELEMENTS;i++)); do
    echo ${ARRAY[${i}]}
    echo ${ARRAY2[${i}]}
    ${PYTHONROOT}/bowtie_stats.py -f ${ARRAY[${i}]} -o ${ARRAY2[${i}]}
done

