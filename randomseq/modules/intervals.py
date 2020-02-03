import pandas as pd
import copy
import os
import random
from collections import deque


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


def generate_intervals(db, int_size, N):
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
    y_copy = copy.copy(y[y["diff"] > int_size])
    y_sel = y_copy.sample(n=N, replace=True)
    intervals = y_sel.apply(pick_random, int_size=int_size, axis=1)
    bed_df = pd.DataFrame(intervals)
    return bed_df


def gtf_to_bed(file_name, feature, int_size, N, bed_name="interval_gtf.bed"):
    db = load_db(file_name, feature)
    bed_df = generate_intervals(db, int_size, N)
    bed_df.to_csv(bed_name, sep="\t", index=False, header=False)
    return bed_name


def extend(line, win_size, times, direction="all"):

    chrom, start_0, end_0, name, score, strand = line.strip().split("\t")
    intervals_start = deque(str(), times)
    intervals_end = deque(str(), times)

    for i in range(0, times):
        start_new = int(start_0) - win_size
        end_new = int(end_0) + win_size

        intervals_start.appendleft(
            f"{chrom}\t{start_new}\t{start_0}\t{name}:extended:-{i}\t{score}\t{strand}\n"
        )
        intervals_end.appendleft(
            f"{chrom}\t{end_0}\t{end_new}\t{name}:extended:+{i}\t{score}\t{strand}\n"
        )
        start_0 = start_new
        end_0 = end_new
    return ("").join(intervals_start), ("").join(intervals_end)


def extend_intervals(bed_file, win_size, times, output):
    string_out = str()
    with open(bed_file, "r") as f, open(output, "w") as out:
        for line in f.readlines():
            intervals_start, intervals_end = extend(line, win_size, times)
            string_out += intervals_start
            string_out += line
            string_out += intervals_end
        out.write(string_out)
    return output


if __name__ == "__main__":
    TEST_BED_FILENAME = "random_intervals.bed"
    WIN_SIZE = 100
    TIMES = 3
    # db = load_db(TEST_NAME)
    print(extend_intervals(TEST_BED_FILENAME, WIN_SIZE, TIMES))
