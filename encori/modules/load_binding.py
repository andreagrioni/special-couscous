from modules import encori_cleanup
from modules.extract_sequences import gen_random_intervals
import pandas as pd


def as_bed(infile, label, anno_df, mask_df, binding_win_size):
    """
    function converts input BED file to pandas df,
    and returns it.

    paramenters:
    infile=path to bed file
    """
    col = ["chromosome", "start", "end", "miRNAid", "clipExpNum", "strand"]
    bed_input = pd.read_csv(infile, sep="\t", names=col)
    bed_df = cleanup_wrapper(input_df, anno_df, mask_df, binding_win_size)
    bed_df["label"] = label
    return bed_df


def cleanup_wrapper(input_df, anno_df, mask_df, binding_win_size):
    """
    functions runs sub-functions for data filtering and cleanup.
    returns pandas df cleaned.
    

    paramenters:
    input_df=pandas df
    anno_df=annotation df
    mask_df=mask df
    binding_win_size=size of the binding site
    """
    ## filter encori db
    encori_filtered_df = encori_cleanup.filter_encori(input_df, anno_df, mask_df)

    ## sanify encori db
    encori_sanified = encori_cleanup.sanify(encori_filtered_df, binding_win_size)
    return encori_sanified


def get_negatives(
    sample_size, mirna_df, anno_df, mask_df, binding_win_size,
):
    """
    function creates a table of random negatives selected from
    the genome (with random miRNA assigned). returns a pandas df


    parameters:
    sample_size=number of random samples
    mirna_df=mirna df
    anno_df=annotation df
    mask_df=mask df
    binding_win_size=size of the binding site
    """
    random_df = gen_random_intervals(sample_size, reg_genome="hg19")
    random_df["miRNAid"] = random_df["miRNAid"].sample(n=sample_size, replace=True)
    random_df["label"] = "negative"
    return cleanup_wrapper(random_df, anno_df, mask_df, binding_win_size)


def load_encori(
    file_path,
    anno_df,
    mask_df,
    binding_win_size,
    negative_sample_size,
    negative_from_shuffle_positive,
):
    """
    function loads encori table as pandas df and 
    returned a filtered table.

    paramenters:
    file_path=path to encori file
    anno_df=pandas df of annotation
    mask_df=pandas df of repeat mask
    binding_win_size=binding window size (int)
    negative_sample_size=number of negatives (int)
    shuffle_positive=negatives samples by random shuffling miRNA from positive dataset (bool)
    """
    # load encori
    df_encori = pd.read_csv(file_path, comment="#", sep="\t")
    df_encori_clean = cleanup_wrapper(df_encori, anno_df, mask_df, binding_win_size)
    df_encori_clean["label"] = "positive"
    return df_encori_clean


def shuffle_to_negative(df):
    """
    function shuffle miRNAid column of
    input df to generate negative class
    returns input df with negative samples

    paramenters:
    df=positive df
    """

    print("shuffle miRNA of input table to create negative class")
    df_negative = df.copy()
    df_negative["miRNAid"] = (
        df_negative["miRNAid"].sample(frac=1).reset_index(drop=True)
    )
    df_negative["label"] = "negative"
    update_df = pd.concat([df, df_negative], axis=0, ignore_index=True)
    return update_df


if __name__ == "__main__":
    pass
