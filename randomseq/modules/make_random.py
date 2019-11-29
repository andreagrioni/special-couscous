import pandas as pd
from modules import bedtools
from modules import intervals


def generator(ARGUMENTS):
    if not ARGUMENTS.input_bed and not ARGUMENTS.gtf_anno:
        print(f"get random intervals from genome {ARGUMENTS.reference}")
        RANDOM_BED = bedtools.random_interval(
            ARGUMENTS.reference, ARGUMENTS.int_size, ARGUMENTS.N
        )

    elif ARGUMENTS.gtf_anno:
        print(f"get intervals from annotation file {ARGUMENTS.gtf_anno}")

        RANDOM_BED = intervals.gtf_to_bed(
            file_name=ARGUMENTS.gtf_anno,
            feature=ARGUMENTS.feature,
            int_size=ARGUMENTS.int_size,
            N=ARGUMENTS.N,
        )

    elif ARGUMENTS.input_bed:
        print(f"load input bed file {ARGUMENTS.input_bed}")
        RANDOM_BED = ARGUMENTS.input_bed

    else:
        print("nothing to do")

    if ARGUMENTS.avoid_int and RANDOM_BED:
        print("removing positive intervals")
        RANDOM_BED = bedtools.intersect(
            RANDOM_BED, ARGUMENTS.avoid_int, opt=ARGUMENTS.intersect_opt
        )
    return RANDOM_BED


def make_set(ARGUMENTS):
    df_list = list()
    tmp_size = 0

    while tmp_size < ARGUMENTS.N:
        RANDOM_BED = generator(ARGUMENTS)
        tmp_df = pd.read_csv(RANDOM_BED, sep="\t", header=None)
        tmp_size += tmp_df.shape[0]
        df_list.append(tmp_df)

    if df_list:
        merge_df = pd.concat(df_list, axis=0).sample(n=ARGUMENTS.N)
        merge_df.to_csv(RANDOM_BED, sep="\t", header=False, index=False)
    return RANDOM_BED


if __name__ == "__main__":
    pass
