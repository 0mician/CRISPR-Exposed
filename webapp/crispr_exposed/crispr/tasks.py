from celery import task
import tempfile

import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

@task()
def blastn(FASTA):
    ## generating random file names
    fasta_temp = tempfile.NamedTemporaryFile()
    blast_temp = tempfile.NamedTemporaryFile()
    
    fasta_file = open(os.path.join(BASE_DIR, "crispr/blast", fasta_temp.name) ,'w')
    fasta_file.writelines(FASTA)
    fasta_file.close()
    
    ## blastn command
    exit_code = os.system("blastn -query " +
                str(os.path.join(BASE_DIR, 'crispr/blast', fasta_temp.name)) + " -db " +
                str(os.path.join(BASE_DIR, 'crispr/blast/db/spacers.fasta')) + " -out " +
                str(os.path.join(BASE_DIR, 'crispr/blast', blast_temp.name)))

    ## reading blast result file into memory
    blast_result_txt = ''
    if(exit_code == 0):
        try:
            blast_result_file = open(os.path.join(BASE_DIR, "crispr/blast", blast_temp.name), 'r')
            if(blast_result_file):
                blast_result_txt = blast_result_file.read()
                blast_result_file.close()
        except File.DoesNotExist:
            pass        ## raise?
    else:
        blast_result_txt = "Oops...!\tSorry, something went wrong while running blast!\nPlease try again."
    return blast_result_txt

@task()
def crt(FASTA, parameters={}):
    
    ## path to the crt tool
    crt = "../../configuration/tools/CRT1.2-CLI.jar"
    
    ## retrieving parameters
    minNR = parameters["para1"]
    minRL = parameters["para2"]
    maxRL = parameters["para3"]
    minSL = parameters["para4"]
    maxSL = parameters["para5"]
    searchWL = parameters["para6"]      ##not used atm
    
    crt_options = "-minNR {minNR} -minRL {minRL} -maxRL {maxRL} -minSL {minSL} -maxSL {maxSL} ".format(**locals())
    
    ## generating random file names
    fasta_temp = tempfile.NamedTemporaryFile()

    fasta_temp_path = "crispr/crt" + fasta_temp.name
    crt_report_path = fasta_temp_path + ".crt.report"
    
    ## writing the FASTA input into a temporary file to be feed to crt as input
    fasta_file = open(os.path.join(BASE_DIR, fasta_temp_path) ,'w')
    fasta_file.writelines(FASTA)
    fasta_file.close()
    
    ## crt command
    exit_code = os.system('java -cp ' + crt + ' crt ' + crt_options + fasta_temp_path + ' ' + crt_report_path + '>> crt.log 2>&1')
    
    ## reads crt output into memory
    crt_report_txt = ''
    if(exit_code == 0):
        try:
            crt_report_file = open(os.path.join(BASE_DIR, crt_report_path), 'r')
            if(crt_report_file):
                crt_report_txt = crt_report_file.read()
                crt_report_file.close()
        except:
            pass        ## raise?
    else:
        crt_report_txt = "Oops...!\tSorry, something went wrong while running crt!\nPlease try again."
    
    os.system('rm crispr/crt' + fasta_temp.name + '*')
    return crt_report_txt
