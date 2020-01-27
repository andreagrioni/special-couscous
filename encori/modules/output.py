import pandas as pd
import json
import sys


def generate_table(combined_df, col=None, output_name=None):
    """
    function merges encori and mirna db to a new pandas df; this
    pandas df is saved as tsv table with name==output_name.

    paramenters:
    encori=encori pandas df
    mirna_db=mirna df
    col=target column to subset from join table
    output_name=path to output name 
    """

    # path_1 = "/home/angri/Desktop/project/special-couscous/encori/encori_tmp.tsv"
    # path_2 = "/home/angri/Desktop/project/special-couscous/encori/mirna_tmp.tsv"

    # join_df = encori.merge(mirna_db, how="inner", on="miRNAid")

    # encori.to_csv(path_1, sep="\t", index=False, header=True)
    # mirna_db.to_csv(path_2, sep="\t", index=False, header=True)

    output_df = combined_df[col].dropna().copy()
    output_df.to_csv(output_name, sep="\t", index=False)
    return output_name


def load_config(infile=None):
    if infile:
        with open(infile, "r") as fo:
            return json.load(fo)
    else:
        print("provide config joson file")
        sys.exit()
