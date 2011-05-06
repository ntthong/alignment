#!/bin/bash

export EXPTROOT="/Users/stirls/lib/data/091113/Alignment/100225"

cd ${EXPTROOT}
export BOWTIE_LOG="${EXPTROOT}/log-all-bowtie.txt"
export BOWTIEROOT="/Users/stirls/lib/bowtie-0.12.0/"
echo "Finding bowtie directory ${BOWTIEROOT}" >${BOWTIE_LOG}
genome="indexes/sc_sgd_gff_20091011_plus"



for f in $( ls s_?_trimmed.txt ); do
    echo $f >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -a -m 20 -p 7 -v 3 --nofw --max ${f/".txt"/"_tRNA_toomany.txt"} --un ${f/".txt"/"_tRNA_free.txt"} ${BOWTIEROOT}indexes/sc_tRNA_snoRNA $f\
         > ${f/".txt"/"_tRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".txt"/"_tRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${BOWTIEROOT}indexes/rrna  -a -m 20 -p 7 -v 3 --nofw --max ${f/".txt"/"_rRNA_toomany.txt"} --un ${f/".txt"/"_rRNA_free.txt"} ${f/".txt"/"_tRNA_free.txt"}\
         > ${f/".txt"/"_rRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".txt"/"_rRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -a -m 20 -p 7 -v 3 --suppress 6,7 --max ${f/".txt"/"_toomany.txt"} --un ${f/".txt"/"_fail.txt"} \
        ${BOWTIEROOT}$genome ${f/".txt"/"_rRNA_free.txt"}>${f/"trimmed.txt"/"align1.txt"} 2>>${BOWTIE_LOG}
    echo ${f/"trimmed.txt"/"align1.txt"}
done

for f in $( ls s_?_orig.txt ); do
    echo $f >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${BOWTIEROOT}indexes/sc_tRNA_snoRNA -3 10 -a -m 20 -p 7 --nofw -v 3 --max ${f/".txt"/"_tRNA_toomany.txt"} --un ${f/".txt"/"_tRNA_free.txt"} $f\
         > ${f/".txt"/"_tRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".txt"/"_tRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${BOWTIEROOT}indexes/rrna -3 10 -a -m 20 -p 7 -v 3 --nofw --max ${f/".txt"/"_rRNA_toomany.txt"} --un ${f/".txt"/"_rRNA_free.txt"} ${f/".txt"/"_tRNA_free.txt"}\
         > ${f/".txt"/"_rRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".txt"/"_rRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -3 10 -a -m 20 -p 7 -v 3 --suppress 6,7 --max ${f/".txt"/"_toomany.txt"} --un ${f/".txt"/"_fail.txt"} \
        ${BOWTIEROOT}$genome ${f/".txt"/"_rRNA_free.txt"}>${f/"orig.txt"/"align2.txt"} 2>>${BOWTIE_LOG}
    echo ${f/"orig.txt"/"align2.txt"}
done

echo 'All done!'
