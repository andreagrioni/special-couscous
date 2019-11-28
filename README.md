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

            genome = reference genome in Fasta format (file path)
            N = generate N number of samples (int)
            int_size = interval size ( length of the sequence)

         optionals:
            output= sequence output name (default:sequence.tsv)
            seed=random seed (default: 1989)

         usage:

            python randomseq.py \
                 --reference path/to/genome/reference/ --N integer --int_size integer
