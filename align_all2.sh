#!/bin/bash

export OUTPUT="/Users/jsh/proj/churchman_align/output"

cd ${OUTPUT}
export BOWTIE_LOG="${OUTPUT}/log-all-bowtie.txt"
# export BOWTIEROOT="/Users/jsh/bin/bowtie-0.12.7/"
export BOWTIEROOT="/Users/jsh/bin/bowtie-0.12.0/"
export INDEXROOT="/Users/jsh/proj/churchman_align/indexes"
echo "Finding bowtie directory ${BOWTIEROOT}" >${BOWTIE_LOG}
genome="indexes/sc_sgd_gff_20091011_plus"



for f in $( ls *trimmed* ); do
    echo $f >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -a -m 20 -p 7 -v 3 --nofw \
      --max ${f/".fastq"/"_tRNA_toomany.txt"} \
      --un ${f/".fastq"/"_tRNA_free.txt"} ${INDEXROOT}/sc_tRNA_snoRNA $f \
         > ${f/".fastq"/"_tRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".fastq"/"_tRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${INDEXROOT}/rrna  -a -m 20 -p 7 -v 3 --nofw \
      --max ${f/".fastq"/"_rRNA_toomany.txt"} \
      --un ${f/".fastq"/"_rRNA_free.txt"} ${f/".fastq"/"_tRNA_free.txt"}\
         > ${f/".fastq"/"_rRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".fastq"/"_rRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -a -m 20 -p 7 -v 3 --suppress 6,7 \
      --max ${f/".fastq"/"_toomany.txt"} \
      --un ${f/".fastq"/"_fail.txt"} \
        ${BOWTIEROOT}$genome \
        ${f/".fastq"/"_rRNA_free.txt"} \
        > ${f/"trimmed.fastq"/"align1.txt"} \
        2>>${BOWTIE_LOG}
    echo ${f/"trimmed.fastq"/"align1.txt"}
done

for f in $( ls *orig* ); do
    echo $f >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${INDEXROOT}/sc_tRNA_snoRNA \
      -3 10 -a -m 20 -p 7 --nofw -v 3 \
      --max ${f/".fastq"/"_tRNA_toomany.txt"} \
      --un ${f/".fastq"/"_tRNA_free.txt"} $f \
         > ${f/".fastq"/"_tRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".fastq"/"_tRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie ${INDEXROOT}/rrna \
      -3 10 -a -m 20 -p 7 -v 3 --nofw \
      --max ${f/".fastq"/"_rRNA_toomany.txt"} \
      --un ${f/".fastq"/"_rRNA_free.txt"} ${f/".fastq"/"_tRNA_free.txt"}\
         > ${f/".fastq"/"_rRNA.txt"} 2>>${BOWTIE_LOG}
    echo ${f/".fastq"/"_rRNA.txt"} >>${BOWTIE_LOG}
    ${BOWTIEROOT}bowtie -3 10 -a -m 20 -p 7 -v 3 \
      --suppress 6,7 --max ${f/".fastq"/"_toomany.txt"} \
      --un ${f/".fastq"/"_fail.txt"} \
        ${BOWTIEROOT}$genome ${f/".fastq"/"_rRNA_free.txt"} \
        > ${f/"orig.fastq"/"align2.txt"} 2>>${BOWTIE_LOG}
    echo ${f/"orig.fastq"/"align2.txt"}
done

echo 'All done!'
