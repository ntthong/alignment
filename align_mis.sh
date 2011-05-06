#!/bin/bash

export EXPTROOT="/Users/stirls/lib/data/091113/Alignment/100225"

cd ${EXPTROOT}
export BOWTIE_LOG="${EXPTROOT}/log-mis-bowtie.txt"
export BOWTIEROOT="/Users/stirls/lib/bowtie-0.12.0/"
echo "Finding bowtie directory ${BOWTIEROOT}" >${BOWTIE_LOG}
genome="indexes/sc_sgd_gff_20091011_plus"

for f in $( ls s_?_trimmed.txt ); do
    echo $f >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -m 1 -p 7 -v 3 --suppress 6,7 ${BOWTIEROOT}$genome ${f/".txt"/"_rRNA_free.txt"}>${f/"trimmed.txt"/"align_mis1.txt"} 2>>${BOWTIE_LOG}
    echo ${f/"trimmed.txt"/"align_mis1.txt"}
done

for f in $( ls s_?_orig.txt ); do
    echo $f >>${BOWTIE_LOG}
       ${BOWTIEROOT}bowtie -m 1 -p 7 -v 3 --suppress 6,7 ${BOWTIEROOT}$genome ${f/".txt"/"_rRNA_free.txt"}>${f/"orig.txt"/"align_mis2.txt"} 2>>${BOWTIE_LOG}
    echo ${f/"orig.txt"/"align_mis2.txt"}
done

echo 'All done!'
