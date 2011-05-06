#!/bin/bash

export PYTHONROOT="/Users/stirls/lib/python/file_manipulation"
echo "Finding python directory ${PYTHONROOT}"

cp ${PYTHONROOT}/chrom_index.py .

for f in $( ls t_*_plus.txt ); do
    echo $f
    ${PYTHONROOT}/chrom_index.py -f ${f/"_plus.txt"/""}
done


