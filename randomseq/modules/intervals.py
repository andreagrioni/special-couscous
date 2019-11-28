import pandas as pd
import copy
import os
import random


def load_db(file_name, feature="all"):

    if file_name.endswith(".gtf"):
        # from https://www.ensembl.org/info/website/upload/gff.html
        columns = [
            "seqname",
            "source",
            "feature",
            "start",
            "end",
            "score",
            "strand",
            "frame",
            "attribute",
        ]
    else:
        pass

    load_df = pd.read_csv(file_name, sep="\t", names=columns, comment="#")

    if feature != "all":
        load_df = copy.copy(load_df[load_df["feature"] == feature])

    return load_df


def generate_intervals(db, int_size, N, seed=1989):
    def pick_random(row, int_size):
        new_start = random.randint(row.start, row.end - int_size)
        new_end = new_start + int_size
        interval = pd.Series(
            [row.seqname, new_start, new_end, row.strand],
            index=["seqname", "start", "end", "strand"],
        )
        return interval

    y = copy.copy(db)
    y["diff"] = y["end"] - y["start"]
    y_sel = copy.copy(y[y["diff"] > int_size]).sample(n=N, random_state=seed)
    intervals = y_sel.apply(pick_random, int_size=int_size, axis=1)
    bed_df = pd.DataFrame(intervals)
    return bed_df


def gtf_to_bed(file_name, feature, int_size, N, seed=1989, bed_name="interval_gtf.bed"):
    db = load_db(file_name, feature)
    bed_df = generate_intervals(db, int_size, N, seed=1989)
    bed_df.to_csv(bed_name, sep="\t", index=False, header=False)
    return bed_name


if __name__ == "__main__":
    TEST_NAME = "/home/angri/Desktop/project/special-couscous/randomseq/test/test.gtf"
    db = load_db(TEST_NAME)
    bed_df = generate_intervals(db, 100, 10, seed=1989)
    bed_df.to_csv("test.bed", sep="\t", index=False, header=False)

