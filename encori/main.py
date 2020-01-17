from modules import prepare_db
from modules import filter_df
from modules import clean_encori
from modules import mirna_db
from modules import extract_sequences


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

## mirna db info
mirbase_db = "/home/angri/Desktop/project/special-couscous/encori/data/hsa.GRCh38.gff3"
targetscan_db = "/home/angri/Desktop/project/special-couscous/encori/data/TargetScan_v7.2_miR_Family_info.txt"
fasta = "/home/angri/Desktop/project/special-couscous/encori/data/GRCh38.primary_assembly.genome.fa"
cons_test = (
    "/home/angri/Desktop/project/special-couscous/encori/data/hg38.phyloP100way.bw"
)

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
    print("prepared_mirna_db")
    mirna_db = mirna_db.wrapper(
        targetscan_db, mirbase_db, fasta, cons_test, species=9606
    )
    # merge tables
    completed_table = encori_cons_seq_bs.merge(mirna_db, on="miRNAid")
    completed_table.to_csv("final_encori_with_info.tsv", sep="\t")
