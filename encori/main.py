import modules as md

# to define
file_path = path to encori db
column_names = encori db columns to dump
repeat_mask = path to repeat mask bed file
annotation = path to annotation GTF file


if __name__ == "__main__":

    ## encori processing
    # load encori as pd dataframe
    encori = md.load_encori(file_path)

    # keep columns miRNAid, miRNAname, chromosome, broadStart, broadEnd, strand
    encori_bindings = md.dump_columns(
        encori, column_names
        )

    # write as bed file format file (allows use with bedtools)
    encori_bed = md.encori_to_bed(encori_bindings, column_names)

    # optional cleanups:
    # 1) remove bindings in repeat mask regions.
    intersected_path = md.intersect(
        encori_bed, repeat_mask, v=True
        )
    
    # 2) remove non-UTR binding site regions.
    intersected_path = md.intersect(
        intersected_path, annotation
        )

    # 3) remove duplicated
        #ToDo

    # get binding site centroid
    # randomly extend bs from centroid to 200 nt
    # create test (chr1) and train bed files
    # extract sequences with bedtools from hg19
    # extract conservation with pyBigWig module (hg19)

    ## mirna processing
    # 1) pick 1 miRNA per family
    # 2) sequence complexity?