import pandas as pd
import pybedtools
import io


def load_encori(file_path):
    dataset = pd.read_csv(file_path, comment="#", sep="\t")
    return dataset


def dump_columns(df, column_names):
    out_df = df.copy()
    out_df.drop(column_names, axis=1, inplace=True)
    return out_df


def encori_to_bed(df, column_names):
    dest_file = io.StringIO()
    df[column_names].to_csv(dest_file, sep="\t", header=False)
    return dest_file


def intersect(bed_file, target_file, v=False):
    encori = pybedtools.BedTool(bed_file)
    target = pybedtools.BedTool(target_file)
    negative_intersection = encori.intersect(target, s=True, v=v)
    return negative_intersection.fn


# def filter_gtf(gtf_file, targets):
# ToDo

