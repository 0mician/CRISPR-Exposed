import os
import re

from utils.fastas import *

crt = "../configuration/tools/CRT1.2-CLI.jar"
data = "../data/"
fasta_re = re.compile('.*\_genomic.fna')

dir_list = os.listdir(data)

print("Generating CRT output ...\n")

## loop in genomes in Data directory
for genome_dir in dir_list:
    genome_dir_list = os.listdir(data+genome_dir)
    
    ## loop in genome directory looking for genome fasta file(s)
    for _file in genome_dir_list:
        fasta_file = re.search(fasta_re, _file)
        
        if(fasta_file):
            
            ## set the absolute path to genome dir
            path = data + genome_dir + '/'
            fastas = Fastas(path + fasta_file.group())
            
            ## loop in (multi)fasta files using Utils.fastas
            for fasta in fastas:
                
                ## creating a temporary fasta file from a fasta in a multifasta
                fasta_content = ">" + fasta.header + '\n' + fasta.seq
                fasta_output_path = path + fasta.header.split(' ', 1)[0]
                fasta_output = open(fasta_output_path + ".fasta.tmp", 'w')
                fasta_output.write(fasta_content)
                fasta_output.close()
                
                ## applying CRT > java -cp /path/to/CRT crt [input] [output]
                os.system('java -cp ' + crt + ' crt ' + fasta_output_path + ".fasta.tmp" + ' ' + fasta_output_path + '.crt.report')
                ## removing temporary fasta files
                os.system('rm ' + path + '*.tmp')

print("Done!\n")
