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
    config_file = "/home/grioni_andrea/repo/special_couscous/encori/config.json"  # TODO change to argparser
    # target_file = sys.argv[2]

    try:
        output_name = sys.argv[3]
        OPTIONS = output.load_config(config_file, target_file, output_name)
    except:
        OPTIONS = output.load_config(config_file)

    # load DBs
    if OPTIONS["ENCORI_ANNOTATION"]:
        print("prepared annotaton and repeat mask db")
        anno_df, mask_df = prepare_db.load_db(
            OPTIONS["ENCORI_ANNOTATION"],
            OPTIONS["ENCORI_BIOTYPE"],
            OPTIONS["ENCORI_REPEAT_MASK"],
        )
    else:
        anno_df, mask_df = None, None
    # mirna load
    if OPTIONS["MIRNA_DB"]:
        print("prepared_mirna_db")
        mirna_cons_seq_df = mirna_db.wrapper(
            # OPTIONS["MIRNA_TARGETSCAN_DB"],
            OPTIONS["MIRNA_DB"],
            OPTIONS["MIRNA_REF_FASTA"],
            OPTIONS["MIRNA_CONS_TRACK"],
            OPTIONS["TARGETSCAN_SPECIES"],
            OPTIONS["MIRNA_WINDOW"],
        )

    # ENCORI load and cleanup
    if OPTIONS["ENCORI_PATH"]:
        print("load and cleanup ENCORI DB")
        sys.exit()
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
            OPTIONS["BINDING_BED"],
            OPTIONS["BINDING_BED_LABEL"],
            anno_df,
            mask_df,
            OPTIONS["BINDING_WINDOWS"],
        )
    else:
        print("unknown operation")
        sys.exit()

    print("binding_df:", binding_df.shape, sep="\t")
    # combine df
    combine_encori_mirna_df = prepare_db.combine_df(binding_df, mirna_cons_seq_df)
    print("combine_encori_mirna_df:", combine_encori_mirna_df.shape, sep="\t")
    if OPTIONS["NEGATIVE_SAMPLES"]:
        print("generate negative samples")
        if OPTIONS["SHUFFLE_POSITIVES_TO_NEGATIVE"]:
            combine_encori_mirna_df = load_binding.shuffle_to_negative(
                combine_encori_mirna_df, mirna_cons_seq_df
            )
        else:
            pass

    ## extract sequences (cons and nt)
    print("get sequences and conservations")
    binding_cons_seq_df = extract_sequences.extractor(
        combine_encori_mirna_df,
        OPTIONS["ENCORI_CONS_TRACK"],
        OPTIONS["ENCORI_REF_FASTA"],
    )

    print("binding_cons_seq_df:", binding_cons_seq_df, sep="\t")
    ## print output
    print("writing output table")
    output.generate_table(
        binding_cons_seq_df, OPTIONS["OUTPUT_COLUMNS"], OPTIONS["OUTPUT_TABLE_PATH"],
    )
