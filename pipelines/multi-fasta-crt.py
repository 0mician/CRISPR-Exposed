import os
import re

from utils.fastas import *

crt = "../configuration/tools/CRT1.2-CLI.jar"
data = "../data/"
error_file = open("crt_error.txt", 'w')
fasta_re = re.compile('.*\_genomic.fna$')
dir_list = os.listdir(data)

# tracking progress
number_of_folders = len([name for name in os.listdir(data)])
count = 1

## loop in genomes in Data directory
for genome_dir in dir_list:
    genome_dir_list = os.listdir(data+genome_dir)
    print("Processing folder %i out of %i (%s)" % (count, number_of_folders, genome_dir))
    count += 1

    ## loop in genome directory looking for genome fasta file(s)
    for fasta_file in genome_dir_list:
        input_file = re.search(fasta_re,fasta_file)
        try:
            if(input_file):
            
                ## set the absolute path to genome dir
                path = data + genome_dir + '/'
                fastas = Fastas(path + input_file.group())
                
                ## loop in (multi)fasta files using Utils.fastas
                for fasta in fastas:
                    if(len(fasta.seq) < 5000):
                        continue
                    ## creating a temporary fasta file from a fasta in a multifasta
                    fasta_content = ">" + fasta.header + '\n' + fasta.seq
                    fasta_output_path = path + fasta.header.split(' ', 1)[0]
                    fasta_output = open(fasta_output_path + ".fasta.tmp", 'w')
                    fasta_output.write(fasta_content)
                    fasta_output.close()
                    
                    ## applying CRT > java -cp /path/to/CRT crt [input] [output]
                    os.system('java -cp ' + crt + ' crt ' + fasta_output_path + ".fasta.tmp" + ' ' + fasta_output_path + '.crt.report' + '>> crt.log 2>&1')
                    ## removing temporary fasta files
                    os.system('rm ' + path + '*.tmp')
        except FileNotFoundError as e:
            print("not found")
            error_file.write(e)

error_file.close()
print("Done!\n")
