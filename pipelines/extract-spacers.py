import os
import re

data = "../data/"

crt_re = re.compile('.*\.crt\.report')
dir_list = os.listdir(data)

# keep track of progress
number_of_folders = len([name for name in os.listdir(data)])
count = 1

#no_result_re = re.compile('No CRISPR elements were found')

for genome_dir in dir_list:
    genome_dir_list = os.listdir(data + genome_dir)
    print("Processing folder %i out of %i" % (count, number_of_folders))
    count += 1

    for _file in genome_dir_list:
        crt_report_file_name = re.search(crt_re, _file)
        
        if(crt_report_file_name):
            path_to_crt_report = data + genome_dir + '/' + crt_report_file_name.group()
            crt_report_file = open(path_to_crt_report, 'r')
            #if(re.search(no_result_re, crt_report_file.read())):
             #   crt_report_file.close()
                #continue

            crt_report_file = open(path_to_crt_report, 'r')
            crt_output = crt_report_file.readlines()
            
            ls = []
            for line in crt_output:
                i = line.rstrip("\n").split("\t")
                ls.append(i)
                
            # regex for position 
            position_regex = re.compile("^[0-9]+$")
            nucleotide_regex = re.compile("^[ACTG]+$")
            
            # crispr_ls = [position, repeat, spacer, [repeat_length, spacer_length]]
            crispr_ls = []
            for entry in ls:
                if bool(re.match(position_regex, entry[0])) == True:
                    line = []
                    if bool(re.match(nucleotide_regex, entry[3])) == True:
                        line.extend([entry[0], entry[2], entry[3], entry[4]])
                        crispr_ls.append(line)
            
            if(crispr_ls):
                spacerout_file = open(path_to_crt_report + ".spacers", 'w')
                spacerout_file.write(str(crispr_ls))
                spacerout_file.close()
            
            crt_report_file.close()

