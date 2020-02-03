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
dotgenik.py --x nt_sequence --y nt_sequence

dotgenik.py --table input_tsv --name image_name --out output_directory

options:
--samples=select N random samples from the input table.
"""

import argparse
import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import seaborn as sns
import time
from PIL import Image


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
        alphabet = {"AT": 1.0, "TA": 1.0, "GC": 1.0, "CG": 1.0}
    pair = x_nt + y_nt
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

    matrix = np.zeros((len_x, len_y))

    for i_bind in range(0, len_x):
        for i_micro in range(0, len_y):
            matrix[i_bind, i_micro] = watson_crick(
                x_seq[i_bind], y_seq[i_micro], alphabet=alphabet
            )
    return matrix


def make_2d(
    x_seq, y_seq, alphabet, file_name, out_dir, labels, matplot, pil, array_flag
):
    """
    fun plots 2D metrics of watson-crick binding
    rules of sequence x and y as heatmap

    parameters
    x_seq=sequecne on x axis
    y_seq=sequence on y axis
    alphabet=2D matrix
    file_name=image file name
    out_dir=target directory
    labels=labels ticks as nt sequences (boolean)
    matplot=generate matplot images (boolean)
    pil=generate pil image (boolean)
    array_flag=return np array (boolean)
    """
    # set output dir
    if out_dir:
        file_name = os.path.join(out_dir, file_name)

    # Create binding site - mirna interaction metrics
    array = make_set_hm(x_seq, y_seq, alphabet)
    # Default heatmap: just a visualization of this square matrix

    if matplot:
        plt.imshow(array)
        plt.savefig(file_name)
    elif pil:
        img = Image.fromarray(np.uint8(cm.gist_earth(array) * 255))
        img.save(f"{file_name}.png")
    elif array_flag:
        return array
    else:
        A = len(x_seq)
        B = len(y_seq)
        df = pd.DataFrame(array, index=list(x_seq), columns=list(y_seq))

        FIG, AX = plt.subplots(figsize=(B, A))
        AX = sns.heatmap(
            df,
            xticklabels=labels,
            yticklabels=labels,
            annot=False,
            cbar=False,
            cmap="Blues",
            # vmin=0,
            # vmax=1,
        )
        FIG.savefig(f"{file_name}.png")
        plt.cla()
        plt.close(FIG)
    return array


def make_2d_caller(row, alphabet, file_name, out_dir, labels, matplot, pil, array):
    fig_id = f"{row.name}_{file_name}"
    return make_2d(
        row.x_seq, row.y_seq, alphabet, fig_id, out_dir, labels, matplot, pil, array
    )


def make_image_batch(args):
    """
    fun prints heatmaps of 2D matrix interactions
    from input table with x,y,label.

    paramenters:
    args=parser object with arguments
    """
    if not ARGS.feature:
        connections_df = pd.read_csv(
            args.table, sep="\t", names=["x_seq", "y_seq", "label"], header=0
        )
    else:
        features = ARGS.feature
        df_all = pd.read_csv(
            args.table, sep="\t"
        )
        connections_df = df_all[features].copy()
        connections_df.columns = ["x_seq", "y_seq", "label"]
    if args.samples:
        connections_df = connections_df.sample(n=args.samples, random_state=1989)

    if not args.array:
        connections_df.apply(
            make_2d_caller,
            alphabet=args.alphabet,
            file_name=args.file_name,
            out_dir=args.out_dir,
            labels=args.labels,
            matplot=args.matplot,
            pil=args.pil,
            array=args.array,
            axis=1,
        )
    else:
        storage_list = list()
        output = os.path.join(args.out_dir, args.file_name)
        for index, row in connections_df.iterrows():
            array = make_2d_caller(
                row=row,
                alphabet=args.alphabet,
                file_name=args.file_name,
                out_dir=args.out_dir,
                labels=args.labels,
                matplot=args.matplot,
                pil=args.pil,
                array=args.array,
            )
            storage_list.append(array)
        np.savez(output, *storage_list)


def pre_process(ARGS):
    if ARGS.out_dir:
        if not os.path.exists(ARGS.out_dir):
            os.makedirs(ARGS.out_dir, exist_ok=True)
    if ARGS.alphabet:
        ARGS.alphabet = eval(ARGS.alphabet)
    if ARGS.feature:
        ARGS.feature = list(ARGS.feature.split(" "))
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
    parser.add_argument(
        "--labels",
        dest="labels",
        help="labels ticks as nt sequences (boolean)",
        action="store_true",
    ),
    parser.add_argument(
        "--matplot",
        dest="matplot",
        help="matplot image (boolean)",
        action="store_true",
    ),
    parser.add_argument(
        "--pil", dest="pil", help="pil image (boolean)", action="store_true",
    ),
    parser.add_argument(
        "--np",
        dest="array",
        help="output array of matrixes (boolean)",
        action="store_true",
    ),
    parser.add_argument(
        "--feature",
        dest="feature",
        type=str,
        help="load only feature columns separeted by single space",
        )

    args = parser.parse_args()
    args = pre_process(args)
    return args


if __name__ == "__main__":
    ARGS = get_arguments()
    start = time.time()
    try:
        if ARGS.table:
            make_image_batch(ARGS)
        else:
            make_2d(
                ARGS.x_seq,
                ARGS.y_seq,
                ARGS.alphabet,
                ARGS.file_name,
                ARGS.out_dir,
                ARGS.labels,
                ARGS.matplot,
                ARGS.pil,
                ARGS.array,
                ARGS.feature
            )
    except ValueError:
        print("no arguments\nrun dotgenik.py --help")
        sys.exit()
    end = time.time()
    print("elapsed time:", end - start, sep="\t")
