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


def random_interval(reference, int_size, N, output="random_intervals.bed"):
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

    def sanify_ref_size(ref_size):
        out_name = "ref.sanify.fai"
        with open(ref_size, "r") as f, open(out_name, "w") as out:
            targets = "".join([x for x in f.readlines() if "chr" in x])
            out.write(targets)
        return out_name

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

    # ref_chrom_size = sanify_ref_size(ref_chrom_size)

    cmd = f"bedtools random -l {int_size} -n {N} -g {ref_chrom_size} > {output}"

    print(cmd)

    subprocess.run(cmd, shell=True, encoding="utf-8")

    return output


def intersect(interval_a, interval_b, opt="", outname="filtered.bed"):
    """
    Fun runs bedtools intersect on a 
    pair of intervals.

    paramenters:
    interval_a=file 1
    interval_b=file 2
    N=sample size
    opt=bedtools intersect opt
    """
    cmd = f"bedtools intersect {opt} -a {interval_a} -b {interval_b} > {outname}"

    print(cmd)

    subprocess.run(cmd, shell=True, encoding="utf-8")

    return outname
