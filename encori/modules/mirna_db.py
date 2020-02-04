import pandas as pd
import re
import io
import os
from modules.extract_sequences import extractor
import sys


def load_targetscan(infile, species):
    targetscan = pd.read_csv(infile, sep="\t")
    return targetscan[targetscan["Species ID"] == species]


def format_mirbase_db(infile, win_size, bed_output="/tmp/mirna_extened.bed"):
    """
    function formats GFF3 file to 
    bed (name as mirna ID).
    returns bed file name

    paramenters:
    infile=db name
    """

    # outfile_name = os.path.basename(infile).replace(".gff3", ".formated.bed")

    def get_id(info):
        # extract mirna id from info field
        return re.search("(?=MIMAT).+?(?=;)", info).group(0)

    def to_bed(chrom, start, end, strand, mirna_id):
        return ("\t").join(map(str, [chrom, start, end, mirna_id, ".", strand])) + "\n"

    def resize_mirna(start, end, strand, win):
        """
        function extends miRNA from 5 prime to
        win size.

        parameters:
        start=int.
        end=int.
        strand=coding strand
        win=extend of N bases from 5 prime (int)
        """
        if strand == "+":
            new_start = int(start) - 1
            new_end = new_start + win
            return new_start, new_end
        elif strand == "-":
            new_end = int(end) + 1
            new_start = new_end - (win + 1)
            return new_start, end

    with open(infile) as fi, open(bed_output, "w") as fo:
        new_bed = ""
        for line in fi.readlines():
            if line[0] == "#":
                continue
            if "miRNA_primary_transcript" in line:
                continue
            column = line.strip().split("\t")
            chrom, start, end, strand, info = (
                column[0],
                column[3],
                column[4],
                column[6],
                column[8],
            )
            mirna_id = get_id(info)
            start, end = resize_mirna(start, end, strand, win_size)
            new_bed += to_bed(chrom, start, end, strand, mirna_id)

        fo.write(new_bed)
        # out = io.StringIO(new_bed)

    return bed_output


def wrapper(
    # targetscan_path,
    mirbase_path,
    reference,
    cons_track,
    species=9606,
    win_size=20,
):
    """
    function load targetscan and mirbase db, merge then together and retrive
    information of miRNA conservation and nucleotide sequence. It returns
    a new pandas df of targetscan + mirbase + cons + sequence.


    parameters:
    targetscan_path=path to targetscan file
    mirbase_path=path to mirbase file
    reference=path to corresponding reference genome used in previous db
    cons_track=path to conservation track
    """

    # targetscan_df = load_targetscan(targetscan_path, species=species)
    mirbase_df = format_mirbase_db(mirbase_path, win_size)
    mirbase_seq = extractor(mirbase_df, cons_track, reference, mirna=True)

    # names = ["miRNAid", "binding_cons_score", "binding_sequence"]
    # to_return = output_df[names].copy()
    # to_return = mirbase_seq[names].copy()

    if reference and cons_track:
        names = ["miRNAid", "binding_sequence", "binding_cons_score"]
        to_return = mirbase_seq[names].copy()
        to_return.columns = ["miRNAid", "mirna_cons_score", "mirna_binding_sequence"]
    elif not cons_track:
        names = ["miRNAid", "binding_sequence"]
        to_return = mirbase_seq[names].copy()
        to_return.columns = ["miRNAid", "mirna_binding_sequence"]
    elif not reference:
        names = ["miRNAid", "binding_cons_score"]
        to_return = mirbase_seq[names].copy()
        to_return.columns = ["miRNAid", "mirna_cons_score"]

    return to_return


if __name__ == "__main__":
    mirbase_db = (
        "/home/angri/Desktop/project/special-couscous/encori/data/hsa.GRCh38.gff3"
    )
    targetscan_db = "/home/angri/Desktop/project/special-couscous/encori/data/TargetScan_v7.2_miR_Family_info.txt"
    fasta = "/home/angri/Desktop/project/special-couscous/encori/data/GRCh38.primary_assembly.genome.fa"
    cons_test = (
        "/home/angri/Desktop/project/special-couscous/encori/data/hg38.phyloP100way.bw"
    )
    wrapper(targetscan_db, mirbase_db, fasta, cons_test, species=9606)
