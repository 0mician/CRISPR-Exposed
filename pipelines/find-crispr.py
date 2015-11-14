import os
import re

from utils import *

crt = "../configuration/tools/CRT1.2-CLI.jar"

data = "../data/"

fasta_re = re.compile('.*\_genomic.fna')
dir_list = os.listdir(data)

for genome_dir in dir_list:
    #crt_input = os.listdir(data+genome_dir+'/*_genomic.fna')
    genome_dir_list = os.listdir(data+genome_dir)
    for _file in genome_dir_list:
        input_file = re.search(fasta_re,_file)
        if(input_file):
            path = data + genome_dir + '/'
            os.system('java -cp ' + crt + ' crt ' + path + input_file.group() + ' ' + path + 'crt.report.txt')
            os.system('rm ' + path + '*.tmp2')
