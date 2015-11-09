from Utils.fastas import *

import os

fastas = Fastas(os.path.abspath("multi.fasta"))

for fasta in fastas:
    print fasta.header
    print fasta.seq

