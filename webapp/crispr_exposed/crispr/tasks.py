from celery import task

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@task()
def blastn(FASTA):
    fasta_file = open(os.path.join(BASE_DIR, "crispr/blast/tmp/input.fasta") ,'w')
    fasta_file.writelines(">input\n"+FASTA)
    fasta_file.close()
    
    ## blastn command
    os.system("blastn -query " + 
              str(os.path.join(BASE_DIR, 'crispr/blast/tmp/input.fasta')) + " -db " + 
              str(os.path.join(BASE_DIR, 'crispr/blast/db/spacers.fasta')) + " -out " + 
              str(os.path.join(BASE_DIR, 'crispr/blast/tmp/blast_result.txt')))

    ## loop until file is generated
    while(True):
        try:
            blast_result_file = open(os.path.join(BASE_DIR, "crispr/blast/tmp/blast_result.txt"), 'r')
            if(blast_result_file):
                ## reading blast result file into memory
                blast_result_txt = blast_result_file.read()
                blast_result_file.close()
                
                ## removing temp files
                os.system("rm " + str(os.path.join(BASE_DIR, "crispr/blast/input.fasta")) +
                          " " + str(os.path.join(BASE_DIR, "crispr/blast/blast_result.txt")))
                break
        except File.DoesNotExist:
            pass
    return blast_result_txt

