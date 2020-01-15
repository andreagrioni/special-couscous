import pandas as pd
import random


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


def extend_bs(df, size=200):
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
    df_extend_bindings = extend_bs(centroid, size=200)
    return df_extend_bindings


if __name__ == "__main__":
    test_file = (
        "/home/angri/Desktop/project/special-couscous/encori/data/test_clean_encori.bed"
    )
    encori_names = "chromosome,broadStart,broadEnd,miRNAid,clipExpNum,strand".split(",")
    encori_df = pd.read_csv(test_file, sep="\t", names=encori_names)
    final_df = sanify(encori_df, interval_size=200)
    final_df.to_csv("./after_clean_encori.tsv", header=True, index=False, sep="\t")
