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
    bed_input["miRNAid"] = bed_input.apply(lambda x: x.miRNAid.split(":")[0], axis=1)

    if anno_df and mask_df:
        bed_df = cleanup_wrapper(bed_input, anno_df, mask_df, binding_win_size)
    else:
        bed_df = bed_input.copy()

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
    file_path, anno_df, mask_df, binding_win_size,
):
    """
    function loads encori table as pandas df and 
    returned a filtered table.

    paramenters:
    file_path=path to encori file
    anno_df=pandas df of annotation
    mask_df=pandas df of repeat mask
    binding_win_size=binding window size (int)
    """
    # load encori
    df_encori = pd.read_csv(file_path, comment="#", sep="\t")
    df_encori_clean = cleanup_wrapper(df_encori, anno_df, mask_df, binding_win_size)
    df_encori_clean["label"] = "positive"
    return df_encori_clean


def shuffle_to_negative(df, mirna_cons_seq_df):
    """
    function shuffle miRNAid column of
    input df to generate negative class
    returns input df with negative samples

    paramenters:
    df=positive df
    """

    def randomize(row, mirna_cons_seq_df):
        real_mirna = row.miRNAid
        random_mirna = row.miRNAid
        while real_mirna == random_mirna:
            random_row = mirna_cons_seq_df.sample(n=1)
            random_mirna = random_row.miRNAid.iloc[0]
            random_seq = random_row.mirna_binding_sequence.iloc[0]
            random_cons = random_row.mirna_cons_score.iloc[0]
        return pd.Series(
            data=[random_mirna, random_cons, random_seq],
            index=["miRNAid", "mirna_cons_score", "mirna_binding_sequence"],
        )

    print("shuffle miRNA of input table to create negative class")
    df_negative = df.copy().drop(
        ["miRNAid", "mirna_cons_score", "mirna_binding_sequence"], axis=1
    )

    df_random = df.apply(randomize, mirna_cons_seq_df=mirna_cons_seq_df, axis=1)

    df_tmp = df_negative.join(df_random)
    df_tmp["label"] = "negative"

    df_final = pd.concat(
        [df, df_tmp], axis=0, ignore_index=False, sort=False
    ).reset_index(drop=True)

    return df_final


if __name__ == "__main__":
    pass
