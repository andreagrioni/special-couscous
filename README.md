# special-couscous

repository of miscellaneous tools

* dotgenik: tool generates heatmap of sequence-sequence interactions.
   
        requirements:
            python3.7
            pandas
            seaborn
            matplotlib
            
        Feed sequences from CL:
            dotgenik.py --x nt_sequence --y nt_sequence --name image_name --out output_directory 
        Feed sequences through table:
            dotgenik.py --table input_tsv --name image_name --out output_directory

        *(input_tsv table as column: x_nt_seq, y_nt_seq, labels)

<img src="./dotgenik/test1.png" width=250 align="center">

* randomseq: tool to generate nucleotide sequences of random intervals from target genome.

         requirements:

            bedtools
            samtools
            Python3.6 or greater;

         Input paramenters:

            --reference = path to reference genome (fasta)
            --N = generate N number of samples (int)
            --int_size = interval size (length of random intervals)
         
         optionals:
            --avoid_int = path to bed file of intervals to exclude from random generation (def. None)
            --fasta = extract fasta sequence of random generated intervals (def. False)
            --output = output prefix (def. sequences.tsv)
            --bed = path to bed file of intervals from which extract sequences (def. None)
            --gtf = path to gtf file to be used for the generation of random intervals (def. None)
            --gtf_target = reduce gtf file to only feature
            --getfasta_opt = bedtools options for get fasta (def. '-tab')
            --intersect_opt = bedtools options for intersect (def. '-v')
         
         usage:
            
            generate random intervals from reference file and output fasta sequences
            python randomseq.py \
                 --reference path/to/genome/reference/ --N 100 --int_size 500 --fasta
                 
            generate random intervals from reference file and exclude user defined intervals, output fasta sequences
            python randomseq.py \
                 --reference path/to/genome/reference/ --N 100 --int_size 500 --fasta
                 
            generate random intervals from gtf file with only 'gene' feature, output fasta sequences
            python randomseq.py \
                  --gtf path/to/gtf/file --gtf_target gene --N 100 --int_size 500 --fasta
