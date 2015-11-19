# quick script to get rid of reports during dev

import os
import re

data = "../data/"

crt_re = re.compile('.*\.crt\.report$')
spacers_re = re.compile('.*\.crt\.report\.spacers$')
temp_re = re.compile('.*\.fasta\.tmp$')

dir_list = os.listdir(data)

# keep track of progress
number_of_folders = len([name for name in os.listdir(data)])
count = 1

for genome_dir in dir_list:
    print("Processing folder %i out of %i" % (count, number_of_folders))
    count += 1

    path = data + genome_dir + '/'
    genome_dir_list = os.listdir(path)

    for _file in genome_dir_list:
        spacers_report_file_name = re.search(spacers_re, _file)        
        crt_report_file_name = re.search(crt_re, _file)
        tmp_fasta = re.search(temp_re, _file)

        if(spacers_report_file_name):
            os.system('rm ' + path + spacers_report_file_name.group())

        if(crt_report_file_name):
            os.system('rm ' + path + crt_report_file_name.group())
        
        if(tmp_fasta):
            os.system('rm ' + path + tmp_fasta.group())

