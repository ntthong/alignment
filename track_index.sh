#!/bin/bash

export PYTHONROOT="/Users/stirls/lib/python/file_manipulation"
echo "Finding python directory ${PYTHONROOT}"

cp ${PYTHONROOT}/TSS_index.py .

for f in $( ls t_*_plus.txt ); do
    echo $f
    ${PYTHONROOT}/TSS_index.py -f ${f/"_plus.txt"/""} -t '/Users/stirls/lib/TSS_data/TSS.txt'
done


