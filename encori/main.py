from modules import prepare_db
from modules import filter_df
from modules import clean_encori

# to define
# ENCORI_PATH = path to encori db
# column_names = encori db columns to dump
# REPEAT_MASK = path to repeat mask bed file
# ANNOTATION = path to annotation GTF file
BIOTYPE = ["UTR"]


# REPEAT_MASK = "./data/repeat_mask_hg19.bed"
# ENCORI_PATH = "./data/toy_encori.tsv"
# ANNOTATION = "./data/toy_gencode.gtf"


REPEAT_MASK = (
    "/home/angri/Desktop/project/special-couscous/encori/data/repeat_mask_hg19.bed"
)
ENCORI_PATH = "/home/angri/Desktop/project/special-couscous/encori/data/toy_encori.tsv"
ANNOTATION = "/home/angri/Desktop/project/special-couscous/encori/data/gencode.v19.chr_patch_hapl_scaff.annotation.gtf"
CONS_TRACK = "/home/angri/Desktop/project/special-couscous/encori/data/hg19.100way.phyloP100way.bw"
REF_FASTA = "/home/angri/Desktop/project/special-couscous/encori/data/hg19.fa"


if __name__ == "__main__":
    ## prepared db
    print("prepare_db")
    encori_df, anno_df, mask_df = prepare_db.prepare_db(
        ANNOTATION, BIOTYPE, REPEAT_MASK, ENCORI_PATH
    )

    ## filter encori db
    print("filtering encori")
    encori_filtered_df = filter_df.filter_encori(encori_df, anno_df, mask_df)

    ## sanify encori db
    print("sanify encori")
    encori_sanified = clean_encori.sanify(encori_filtered_df, interval_size=200)

    ## extract sequences (cons and nt)
    print("get sequences and conservations")
    encori_cons_seq_bs = extract_sequences.extractor(
        encori_sanified, CONS_TRACK, REF_FASTA
    )
    encori_cons_seq_bs.to_csv("final.tsv", sep="\t", index=False)
    ## mirna processing
    # 1) pick 1 miRNA per family
    # 2) sequence complexity?

    # create test (chr1) and train bed files

