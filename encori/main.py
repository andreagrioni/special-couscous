from modules import prepare_db
from modules import load_binding
from modules import mirna_db
from modules import extract_sequences
from modules import output
import sys

"""
DOCSTRING TODO
"""

if __name__ == "__main__":
    infile = sys.argv[1]  # TODO change to argparser
    OPTIONS = output.load_config(infile)

    # load DBs
    anno_df, mask_df = prepare_db.load_db(
        OPTIONS["ENCORI_ANNOTATION"],
        OPTIONS["ENCORI_BIOTYPE"],
        OPTIONS["ENCORI_REPEAT_MASK"],
    )
    # mirna load
    print("prepared_mirna_db")
    mirna_cons_seq_df = mirna_db.wrapper(
        OPTIONS["MIRNA_TARGETSCAN_DB"],
        OPTIONS["MIRNA_DB"],
        OPTIONS["MIRNA_REF_FASTA"],
        OPTIONS["MIRNA_CONS_TRACK"],
        OPTIONS["TARGETSCAN_SPECIES"],
        OPTIONS["MIRNA_WINDOW"],
    )

    # ENCORI load and cleanup
    if OPTIONS["ENCORI_PATH"]:
        print("load and cleanup ENCORI DB")
        binding_df = load_binding.load_encori(
            OPTIONS["ENCORI_PATH"], anno_df, mask_df, OPTIONS["BINDING_WINDOW"]
        )

    elif OPTIONS["BINDING_BED"]:
        print("load external file (not ENCORI)")
        binding_df = load_binding.as_bed(
            OPTIONS["NEGATIVE"],
            OPTIONS["BINDING_BED_LABEL"],
            anno_df,
            mask_df,
            OPTIONS["BINDING_WINDOWS"],
        )
    elif OPTIONS["NEGATIVE_SAMPLES"]:
        # Generate Negatives
        binding_df = load_bindings.get_negatives(
            OPTIONS["NEGATIVE_SAMPLES"],
            mirna_cons_seq_df,
            anno_df,
            mask_df,
            OPTIONS["BINDING_WINDOWS"],
        )
    else:
        print("unknown operation")
        sys.exit()

    ## extract sequences (cons and nt)
    print("get sequences and conservations")
    binding_cons_seq_df = extract_sequences.extractor(
        binding_df, OPTIONS["ENCORI_CONS_TRACK"], OPTIONS["ENCORI_REF_FASTA"]
    )
    ## print output
    print("writing output table")
    output.generate_table(
        binding_cons_seq_df,
        mirna_cons_seq_df,
        OPTIONS["OUTPUT_COLUMNS"],
        OPTIONS["OUTPUT_TABLE_PATH"],
    )
