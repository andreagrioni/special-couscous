from pybedtools import BedTool
import pandas as pd
import random


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


def remove_duplicates(df):
    """
    function drops duplicates
    and return pd dataframe.
    """
    print(df.shape)
    df_dedup = df.drop_duplicates(inplace=False)
    print(df_dedup.shape)
    return df_dedup


def add_centroid(df):
    """
    function get centroid of 
    binding site start end coordinates.
    """
    y = df.copy()
    y["centroid"] = y[["broadStart", "broadEnd"]].mean(axis=1).astype(int)
    return y


def extend_bs(df, size):
    """
    function randomly extend binding site
    centroids. returns new df updated with
    new bs start and end.
    

    paramenters:
    df=input encori df
    size=interval size (int)
    """

    def random_resize(row, size):
        centroid = row.centroid
        start = centroid - random.randint(1, size)
        end = start + 200
        return pd.Series([start, end], index=["start", "end"])

    df_intervals = df.apply(random_resize, axis=1, size=size)
    df_concat = pd.concat([df, df_intervals], axis=1)
    return df_concat


def sanify(encori_df, interval_size):
    """
    wrapper for above functions; apply 
    df deduplication, get binding site 
    centroid, and randomly generates
    start,end coordiantes for bs.
    returns the same df with new columns
    start,end
    
    paramenters:
    encori_df=encori pandas df
    interval_size=size to extend intervals
    """

    dedup = remove_duplicates(encori_df)
    centroid = add_centroid(dedup)
    df_extend_bindings = extend_bs(centroid, size=interval_size)
    return df_extend_bindings


if __name__ == "__main__":
    test_file = (
        "/home/angri/Desktop/project/special-couscous/encori/data/test_clean_encori.bed"
    )
    encori_names = "chromosome,broadStart,broadEnd,miRNAid,clipExpNum,strand".split(",")
    encori_df = pd.read_csv(test_file, sep="\t", names=encori_names)
    final_df = sanify(encori_df, interval_size=200)
    final_df.to_csv("./after_clean_encori.tsv", header=True, index=False, sep="\t")
