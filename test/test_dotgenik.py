import os
from dotgenik.dotgenik import make_2d

def test_make_2d():
    dir = os.getcwd()
    seq_1 = "CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGGTTTTTTTTTTTTTTTTTTTTTTTAAAAAAAA"
    seq_2 = "ACGTACGTACGTACGTACGTACGTACGTACGTACGT"
    alphabet = None
    make_2d(seq_1, seq_2, alphabet, 'test', dir, True)