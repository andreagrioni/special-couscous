import argparse
from modules import bedtools
from modules import intervals
from modules import make_random


def parse_args(parser):
    """
    get script OPT and return
    object with OPT as attributes.
    
    paramenters:
    parser = ArgumentParser object
    """

    parser.add_argument(
        "--reference",
        type=str,
        dest="reference",
        help="path to reference genome",
        required=False,
    )
    parser.add_argument(
        "--N",
        type=int,
        dest="N",
        help="generate N number of samples (int)",
        required=False,
    )
    parser.add_argument(
        "--int_size",
        type=int,
        dest="int_size",
        help="length of output sequences (int)",
        required=False,
    ),
    parser.add_argument(
        "--avoid_int",
        type=str,
        dest="avoid_int",
        help="remove random interval overlapping the input bed file regions.",
        required=False,
    ),
    parser.add_argument(
        "--fasta",
        action="store_true",
        dest="fasta_flag",
        help="get fasta sequences",
        required=False,
        default=False,
    ),
    parser.add_argument(
        "--output",
        type=str,
        dest="output_name",
        help="output name",
        required=False,
        default="sequences.tsv",
    ),
    parser.add_argument(
        "--bed",
        type=str,
        dest="input_bed",
        help="input intervals as bed file",
        required=False,
    ),
    parser.add_argument(
        "--gtf",
        type=str,
        dest="gtf_anno",
        help="make random intervals from gtf input file",
        required=False,
    ),
    parser.add_argument(
        "--gtf_target",
        type=str,
        dest="feature",
        help="filter gtf file for features",
        required=False,
        default="all",
    ),
    parser.add_argument(
        "--getfasta_opt",
        type=str,
        dest="getfasta_opt",
        help="bedtools options for get fasta [default -tab]",
        required=False,
        default="-tab",
        nargs="+",
    ),
    parser.add_argument(
        "--intersect_opt",
        type=str,
        dest="intersect_opt",
        help="bedtools options for intersect [default -v]",
        required=False,
        default="-v",
        nargs="+",
    ),
    parser.add_argument(
        "--extend",
        dest="extend",
        help="extend bed intervals [+;-;all]",
        action="store_true",
    ),
    parser.add_argument(
        "--extend_win",
        type=int,
        dest="extend_win",
        help="extend window size",
        required=False,
    ),
    parser.add_argument(
        "--extend_times",
        type=int,
        dest="extend_times",
        help="how many times extend interval",
        required=False,
    )

    args = parser.parse_args()

    args.intersect_opt = "".join(args.intersect_opt)

    args.getfasta_opt = "".join(args.getfasta_opt)

    return args


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(
        description="create 'N' random sequences of length 'int_size' from reference genome"
    )

    OPT = parse_args(PARSER)

    if not OPT.extend:
        RANDOM_BED = make_random.make_set(OPT)
    else:
        RANDOM_BED = False

    if OPT.fasta_flag and RANDOM_BED:
        print(f"extract sequences from BED file {RANDOM_BED}")
        bedtools.get_fasta(
            OPT.reference, RANDOM_BED, OPT.output_name, opt=OPT.getfasta_opt,
        )

    elif not OPT.fasta_flag and RANDOM_BED:
        print(f"random intervals stored at {RANDOM_BED}")
    elif OPT.extend:
        intervals.extend_intervals(
            OPT.input_bed, OPT.extend_win, OPT.extend_times, OPT.output_name
        )
    else:
        print("nothing to do")
