import argparse
from modules import bedtools


def parse_args(parser):
    """
    get script arguments and returns 
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

    args = parser.parse_args()

    return args


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="create 'N' random sequences of length 'int_size' from reference genome"
    )

    arguments = parse_args(parser)

    random_bed = bedtools.random_interval(
        arguments.reference, arguments.int_size, arguments.N, arguments.random_seed
    )

    bedtools.get_fasta(
        arguments.reference, random_bed, arguments.output_name, opt="-tab"
    )
