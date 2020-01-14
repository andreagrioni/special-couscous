from modules import prepare_db
from modules import filter_df


# to define
# ENCORI_PATH = path to encori db
# column_names = encori db columns to dump
# REPEAT_MASK = path to repeat mask bed file
# ANNOTATION = path to annotation GTF file
BIOTYPE = ["UTR"]


# REPEAT_MASK = "./data/repeat_mask_hg19.bed"
# ENCORI_PATH = "./data/toy_encori.tsv"
# ANNOTATION = "./data/toy_gencode.gtf"


REPEAT_MASK = "./data/repeat_mask_hg19.bed"
ENCORI_PATH = "./data/ENCORI_hg19_all.txt"
ANNOTATION = "./data/gencode.v19.chr_patch_hapl_scaff.annotation.gtf"

if __name__ == "__main__":
    ## prepared db
    encori_df, anno_df, mask_df = prepare_db.prepare_db(
        ANNOTATION, BIOTYPE, REPEAT_MASK, ENCORI_PATH
    )

    ## filter encori db
    encori_filtered_df = filter_df.filter_encori(encori_df, anno_df, mask_df)

    # 3) remove duplicated
    # ToDo

    # get binding site centroid
    # randomly extend bs from centroid to 200 nt
    # create test (chr1) and train bed files
    # extract sequences with bedtools from hg19
    # extract conservation with pyBigWig module (hg19)

    ## mirna processing
    # 1) pick 1 miRNA per family
    # 2) sequence complexity?
