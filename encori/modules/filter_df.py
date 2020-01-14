import pandas as pd
from pybedtools import BedTool


def make_bed(df, columns="all", outname="filtered_bed"):
    """
    function converts input df to
    BED 6 file, and retuns filename

    paramenters:
    df=pandas df
    columns=list of target columns
    outname=BED filename
    """
    if columns != "all":
        bed_df = df[columns].copy()
    else:
        bed_df = df
    bed_df.to_csv(outname, sep="\t", header=False, index=False)

    return outname


def intersect_bed(file_a, file_b, u=False, v=False):
    """
    function intersect bed files and return
    new intersection bed file

    paramenters:
    file_a=path to a bed (str)
    file_b=path to b bed (str)
    u=unique intervals (bool)
    v=not matching intervals (bool)
    """

    a_obj = BedTool(file_a)
    b_obj = BedTool(file_b)

    a_intersect_b = a_obj.intersect(b_obj, u=u, v=v)
    return a_intersect_b.fn


def filter_encori(encori_df, anno_df, mask_df):
    """
    wrapper for above filtering functions; returns an
    encori filtered pandas df.

    parameters:
    encori_df=encori df
    anno_df=annotation df
    mask_df=repeat mask df
    """

    encori_names = "chromosome,broadStart,broadEnd,miRNAid,clipExpNum,strand".split(",")
    anno_names = "chrom,start,end,biotype,score,strand".split(",")

    encori_bed = make_bed(encori_df, encori_names, "encori.bed")
    mask_bed = make_bed(mask_df, columns="all", outname="repeat.bed")
    anno_bed = make_bed(anno_df, columns=anno_names, outname="anno.bed")

    encori_no_repeat = intersect_bed(encori_bed, mask_bed, u=False, v=True)

    encori_no_repeat_only_utr = intersect_bed(
        encori_no_repeat, anno_bed, u=False, v=False
    )

    encori_filtered = pd.read_csv(
        encori_no_repeat_only_utr, sep="\t", header=None, names=encori_names
    )

    encori_filtered.to_csv("encori_filtered.bed", sep="\t", header=False, index=False)

    return encori_filtered


if __name__ == "__main__":
    pass
