import pandas as pd
import json
import sys


def generate_table(encori=None, mirna_db=None, col=None, output_name=None):
    """
    function merges encori and mirna db to a new pandas df; this
    pandas df is saved as tsv table with name==output_name.

    paramenters:
    encori=encori pandas df
    mirna_db=mirna df
    col=target column to subset from join table
    output_name=path to output name 
    """
    join_df = encori.merge(mirna_db, on="miRNAid")
    output_df = join_df[col].copy()
    output_df.to_csv(output_name, sep="\t", index=False)
    return output_name


def load_config(infile=None):
    if infile:
        return json.load(infile)
    else:
        print("provide config joson file")
        sys.exit()
