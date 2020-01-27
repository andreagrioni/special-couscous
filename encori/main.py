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
    try:
        infile = sys.argv[1]  # TODO change to argparser
    except:
        infile = "/home/angri/Desktop/project/special-couscous/encori/AG_config.json"
    OPTIONS = output.load_config(infile)

    # load DBs
    print("prepared annotaton and repeat mask db")
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
            OPTIONS["ENCORI_PATH"],
            anno_df,
            mask_df,
            OPTIONS["BINDING_WINDOW"],
            OPTIONS["NEGATIVE_SAMPLES"],
            OPTIONS["SHUFFLE_POSITIVES_TO_NEGATIVE"],
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
    else:
        print("unknown operation")
        sys.exit()

    # combine df
    combine_encori_mirna_df = prepare_db.combine_df(binding_df, mirna_cons_seq_df)

    if OPTIONS["NEGATIVE_SAMPLES"]:
        print("generate negative samples")
        if OPTIONS["SHUFFLE_POSITIVES_TO_NEGATIVE"]:
            combine_encori_mirna_df = load_binding.shuffle_to_negative(
                combine_encori_mirna_df, mirna_cons_seq_df
            )
        else:
            pass
            # combine_encori_mirna_df = load_bindings.get_negatives(
            #     OPTIONS["NEGATIVE_SAMPLES"],
            #     mirna_cons_seq_df,
            #     anno_df,
            #     mask_df,
            #     OPTIONS["BINDING_WINDOWS"],
            # )

    ## extract sequences (cons and nt)
    print("get sequences and conservations")
    binding_cons_seq_df = extract_sequences.extractor(
        combine_encori_mirna_df,
        OPTIONS["ENCORI_CONS_TRACK"],
        OPTIONS["ENCORI_REF_FASTA"],
    )

    ## print output
    print("writing output table")
    output.generate_table(
        binding_cons_seq_df, OPTIONS["OUTPUT_COLUMNS"], OPTIONS["OUTPUT_TABLE_PATH"],
    )
