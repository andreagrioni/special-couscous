import subprocess
import os


def get_fasta(reference, bed_input, output_name, opt=""):
    """ 
    fun runs bedtools getfasta on a pre-defined bed file,
    output to file output_name.

    paramenters:
    reference=path to genome ref
    bed_input=path to bed input name
    output_name=output file name
    opt=additional bedtools options (see bedtools documentation)
    """

    cmd = f"bedtools getfasta {opt} -fi {reference} -bed {bed_input} > {output_name}"
    subprocess.run(cmd, shell=True, encoding="utf-8")

    return output_name


def random_interval(reference, int_size, N, seed=1989, output="random_intervals.bed"):
    """
    fun runs bedtools random to generate random intervals
    based on input paramenters.

    paramenters:
    reference=path to reference genome (fasta file)
    int_size=size of the interval (int)
    N=number of samples (int)
    seed=random seed (optional)
    output=output bed filename
    """

    def index_reference(reference):
        """
        fun create reference index and
        chrom size if not available; these are required for bedtools random.

        paramenters:
        reference=path to genome
        """
        index = f"samtools faidx {reference}"
        if not os.path.exists(f"{reference}.fai"):
            subprocess.run(index, shell=True, encoding="utf-8")
        if not os.path.exists(f"{reference}.chrom.size"):
            cmd = f"cut -f 1,2 {reference}.fai > {reference}.chrom.size"
            subprocess.run(cmd, shell=True, encoding="utf-8")

        return f"{reference}.chrom.size"

    ref_chrom_size = index_reference(reference=reference)

    cmd = f"bedtools random -l {int_size} -n {N} -seed {seed} -g {ref_chrom_size} > {output}"
    subprocess.run(cmd, shell=True, encoding="utf-8")

    return output

