randomseq

generates nucleotide sequences of random intervals from target genome.

requirements:

conda install pybigwig -c bioconda
conda install --channel conda-forge --channel bioconda pybedtools
conda install --channel conda-forge --channel bioconda bedtools htslib
conda install -c anaconda jupyter


Input paramenters:

genome = reference genome in Fasta format (file path)
N = generate N number of samples (int)
int_size = interval size ( length of the sequence)

optionals:
output= sequence output name (default:sequence.tsv)
seed=random seed (default: 1989)


## usage:

### generate random intervals in BED format
python randomseq.py \
        --reference path/to/genome/reference/
        --N integer
        --int_size integer


### extend input bed file of user defined window:

python randomseq.py --extend --bed random_intervals.bed --extend_win 500 --extend_times 10 --output random_int.extended.bed