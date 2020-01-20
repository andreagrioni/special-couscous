from pybedtools import BedTool
import pandas as pd
import pyBigWig


def gen_random_intervals(sample_size, ref_genome):
    """
    function creates random genomic intervals of size 10nt
    and returns a pandas df.


    paramenters:
    sample_size=random samples (int)
    ref_genome=reference genome
    """
    x = BedTool()
    y = x.random(n=sample_size, l=10, genome=ref_genome)
    bed_df = pd.read_csv(
        y.fn,
        sep="\t",
        names=["chromosome", "start", "end", "miRNAid", "clipExpNum", "strand"],
    )
    return bed_df


def get_fasta(intervals, reference, tab=True, s=True, name=True):
    """
    function extract fasta file sequences from 
    reference genome based on bed file intervals.
    return a pd dataframe of id,sequence.


    paramenters:
    intervals=pandas dataframe
    reference=path to reference genome
    tab=True
    s=True
    name=True
    """

    bed_obj = BedTool.from_dataframe(intervals)
    ref_obj = BedTool(reference)
    a = bed_obj.sequence(fi=ref_obj, tab=tab, s=s, name=name)

    seq_tab = pd.read_csv(
        a.seqfn, header=None, names=["fasta_id", "binding_sequence"], sep="\t"
    )
    seq_tab["binding_sequence"] = seq_tab["binding_sequence"].str.upper()
    return seq_tab


def get_conservation(intervals, reference):
    """
    function extracts conservation info 
    for each interval.


    paramenters:
    intervals=pandas df
    reference=path to reference file
    """

    def extract_cons(row, bw_obj):
        start = row.start
        end = row.end
        chrom = row.chromosome
        cons_score = bw_obj.values(chrom, start, end)

        return ",".join(map(str, cons_score))

    bw = pyBigWig.open(reference)
    cons_series = intervals.apply(extract_cons, bw_obj=bw, axis=1)
    cons_df = pd.DataFrame(cons_series, columns=["binding_cons_score"])
    return cons_df


def extractor(df, cons_track, ref_fasta):
    """
    fun gets conservation and sequence from 
    each interval in the encori df.
    returns an updated df with cons. score and
    sequence.
    """

    columns = ["chromosome", "start", "end", "miRNAid", "clipExpNum", "strand"]
    intervals = df[columns].copy()

    cons = get_conservation(intervals, cons_track)
    sequence = get_fasta(intervals, ref_fasta, name=True)

    final = pd.concat([df, cons, sequence], axis=1)
    return final.drop(["fasta_id"], axis=1)


if __name__ == "__main__":
    cons_track = "/home/angri/Desktop/project/special-couscous/encori/data/hg19.100way.phyloP100way.bw"
    ref_fasta = "/home/angri/Desktop/project/special-couscous/encori/data/hg19.fa"
    intervals = "/home/angri/Desktop/project/special-couscous/encori/data/test_extract_sequences.tsv"
    df = pd.read_csv(intervals, sep="\t")

    test = extractor(df, cons_track, ref_fasta)
    print(test)
