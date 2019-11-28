import argparse
from modules import bedtools
from modules import intervals


def parse_args(parser):
    """
    get script arguments and return
    object with arguments as attributes.
    
    paramenters:
    parser = ArgumentParser object
    """

    parser.add_argument(
        "--reference",
        type=str,
        dest="reference",
        help="path to reference genome",
        required=True,
    )
    parser.add_argument(
        "--N",
        type=int,
        dest="N",
        help="generate N number of samples (int)",
        required=True,
    )
    parser.add_argument(
        "--int_size",
        type=int,
        dest="int_size",
        help="length of output sequences (int)",
        required=True,
    )
    parser.add_argument(
        "--output",
        type=str,
        dest="output_name",
        help="output name",
        required=False,
        default="sequences.tsv",
    ),
    parser.add_argument(
        "--seed",
        type=str,
        dest="random_seed",
        help="random seed to generate intervals (int)",
        required=False,
        default=1989,
    )
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
        help="bedtools options for get fasta [default -s -tab]",
        required=False,
        default="-s -tab",
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":

    PARSER = argparse.ArgumentParser(
        description="create 'N' random sequences of length 'int_size' from reference genome"
    )

    ARGUMENTS = parse_args(PARSER)

    if not ARGUMENTS.input_bed and not ARGUMENTS.gtf_anno:
        RANDOM_BED = bedtools.random_interval(
            ARGUMENTS.reference, ARGUMENTS.int_size, ARGUMENTS.N, ARGUMENTS.random_seed
        )
    elif ARGUMENTS.gtf_anno:
        RANDOM_BED = intervals.gtf_to_bed(
            file_name=ARGUMENTS.gtf_anno,
            feature=ARGUMENTS.feature,
            int_size=ARGUMENTS.int_size,
            N=ARGUMENTS.N,
            seed=ARGUMENTS.random_seed,
        )
    elif ARGUMENTS.input_bed:
        RANDOM_BED = ARGUMENTS.input_bed

    bedtools.get_fasta(
        ARGUMENTS.reference,
        RANDOM_BED,
        ARGUMENTS.output_name,
        opt=ARGUMENTS.getfasta_opt,
    )
