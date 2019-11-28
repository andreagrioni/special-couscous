randomseq

generates nucleotide sequences of ranodm intervals from target genome.

requirements:

bedtools
samtools
Python3.6 or greater;


Input paramenters:

genome = reference genome in Fasta format (file path)
N = generate N number of samples (int)
int_size = interval size ( length of the sequence)

optionals:
output= sequence output name (default:sequence.tsv)
seed=random seed (default: 1989)


usage:

python randomseq.py \
        --reference path/to/genome/reference/
        --N integer
        --int_size integer