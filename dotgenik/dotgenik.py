#!/usr/bin/env python

"""
dotgenik creates heatmaps of dot matrix between nucleotide sequences.
it can be run by providing x and y sequences from the CL or it can read
an input tsv table with 3 columns: x_sequence, y_sequence, label.

dotgenik requires:
python3.7
   matplotlib
   seaborn
   pandas

Usage:
dotgenik.py --x nt_sequence --y nt_sequence --name image_name --out output_directory 

dotgenik.py --table input_tsv --name image_name --out output_directory

options:
--samples=select N random samples from the input table.
"""

import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def watson_crick(x_nt, y_nt, alphabet=None):
    """
    fun assigns 1 if input string
    is in alphabet, otherwise
    it returns 0.

    parameters:
    x_nt = nucleotide on x axis
    y_nt = nucleotide on y axis
    alphabet = dict of nt_pair:score
    """
    if not alphabet:
        alphabet = {"AT": 1, "GC": 1, "CG": 1, "TA": 1}
    pair = x_nt + y_nt
    # print(alphabet, pair, alphabet[pair], sep="\t")
    return alphabet.get(pair, 0)


def make_set_hm(x_seq, y_seq, alphabet):
    """
    fun creates a metrics of nt bindings
    according to watson crick rules.
    output is a metrics of 0 or 1 (not bind
    or bind)

    parameters
    x_seq=sequecne on x axis
    y_seq=sequence on y axis
    alphabet=2D matrix
    """
    len_x = len(x_seq)
    len_y = len(y_seq)

    metrics = np.zeros((len_x, len_y))

    for i_bind in range(0, len_x):
        for i_micro in range(0, len_y):
            metrics[i_bind, i_micro] = watson_crick(
                x_seq[i_bind], y_seq[i_micro], alphabet=alphabet
            )
    m_out = pd.DataFrame(metrics, columns=list(y_seq), index=list(x_seq))
    return m_out


def make_2d(x_seq, y_seq, alphabet, file_name, out_dir):
    """
    fun plots 2D metrics of watson-crick binding
    rules of sequence x and y as heatmap

    parameters
    x_seq=sequecne on x axis
    y_seq=sequence on y axis
    alphabet=2D matrix
    file_name=image file name
    out_dir=target directory
    """
    # Create binding site - mirna interaction metrics
    df = make_set_hm(x_seq, y_seq, alphabet)
    # Default heatmap: just a visualization of this square matrix
    FIG, AX = plt.subplots(figsize=(20, 20))
    AX = sns.heatmap(
        df,
        xticklabels=False,
        yticklabels=False,
        annot=False,
        cbar=False,
        cmap="Blues",
        # vmin=0,
        # vmax=1,
    )
    if out_dir:
        file_name = os.path.join(out_dir, file_name)
    FIG.savefig(f"{file_name}.png")
    plt.cla()
    plt.close(FIG)
    return None


def make_2d_caller(row, alphabet, file_name, out_dir):
    fig_id = f"{row.name}_{file_name}"
    make_2d(row.x_seq, row.y_seq, alphabet, fig_id, out_dir)
    return fig_id


def make_image_batch(args):
    """
    fun prints heatmaps of 2D matrix interactions
    from input table with x,y,label.

    paramenters:
    args=parser object with arguments
    """
    connections_df = pd.read_csv(args.table, sep="\t", names=["x_seq", "y_seq", "labe"])
    if args.samples:
        connections_df = connections_df.sample(n=args.samples)
    connections_df["fig_id"] = connections_df.apply(
        make_2d_caller,
        alphabet=args.alphabet,
        file_name=args.file_name,
        out_dir=args.out_dir,
        axis=1,
    )
    return None


def pre_process(ARGS):
    if ARGS.out_dir:
        if not os.path.exists(ARGS.out_dir):
            os.makedirs(ARGS.out_dir, exist_ok=True)
    if ARGS.alphabet:
        ARGS.alphabet = eval(ARGS.alphabet)
    return ARGS


def get_arguments():
    """
    fun parse arguments from
    command line and returns
    the argument objct
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--x", type=str, dest="x_seq", help="nt sequence on axis x", required=False
    )
    parser.add_argument(
        "--y", type=str, dest="y_seq", help="nt sequence on axis y", required=False
    )
    parser.add_argument(
        "--name", type=str, dest="file_name", required=False, default="2D_matrix"
    )
    parser.add_argument("--out", type=str, dest="out_dir", required=False)
    parser.add_argument(
        "--alphabet",
        type=str,
        dest="alphabet",
        help="user specific aphabet for matrix",
        required=False,
        default=None,
    )
    parser.add_argument(
        "--samples",
        type=int,
        dest="samples",
        help="print N random (int)",
        required=False,
    )
    parser.add_argument(
        "--table",
        type=str,
        dest="table",
        help="tsv table of x,y,label connections",
        required=False,
        default=None,
    )
    args = parser.parse_args()
    args = pre_process(args)
    return args


if __name__ == "__main__":
    ARGS = get_arguments()
    if ARGS.table:
        make_image_batch(ARGS)
    else:
        make_2d(ARGS.x_seq, ARGS.y_seq, ARGS.alphabet, ARGS.file_name, ARGS.out_dir)
