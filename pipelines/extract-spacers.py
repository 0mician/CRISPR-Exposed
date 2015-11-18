import os
import re
import json 

data = "../data/"

crt_re = re.compile('.*\.crt\.report')
no_result_re = re.compile('No CRISPR elements were found.')
dir_list = os.listdir(data)

# keep track of progress
number_of_folders = len([name for name in os.listdir(data)])
count = 1

for genome_dir in dir_list:
    genome_dir_list = os.listdir(data + genome_dir)
    print("Processing folder %i out of %i" % (count, number_of_folders))
    count += 1

    for _file in genome_dir_list:
        crt_report_file_name = re.search(crt_re, _file)
        
        if(crt_report_file_name):
            path_to_crt_report = data + genome_dir + '/' + crt_report_file_name.group()
            crt_report_file = open(path_to_crt_report, 'r')
            if(re.search(no_result_re, crt_report_file.read())):
                crt_report_file.close()
                continue

            crt_report_file.seek(0)
            crt_output = crt_report_file.readlines()
            
            ls = []
            for line in crt_output:
                i = line.rstrip("\n").split("\t")
                ls.append(i)

            # regex for position 
            position_regex = re.compile("^[0-9]+$")
            nucleotide_regex = re.compile("^[ACTG]+$")
            crispr_array_regex = re.compile("^CRISPR")
            
            # crispr = [position, repeat, spacer, [repeat_length, spacer_length]]
            crispr = {}
            array_details = []
            crispr_ls = []
            new_array = False
            counter = 1

            for entry in ls:
                # empty line after crispr array?
                if(entry[0] == "" and new_array):
                    new_array = False
                    crispr[counter] = { "details" : array_details, "array" : crispr_ls } 
                    array_details = []
                    crispr_ls = []
                    counter += 1
                    continue

                # CRISPR Array entry?
                if(re.search(crispr_array_regex, entry[0])):
                    array = entry[0].split(' ') # CRISPR 1   Range: 3076611 - 3077005
                    array_details.extend((array[5], array[7]))
                    new_array = True
                    continue

                # Item in CRISPR array?
                if(new_array and re.match(position_regex, entry[0])):
                    line = []
                    if(re.match(nucleotide_regex, entry[3])):
                        lengths = re.findall(r'\d+', entry[4])
                        line.extend((entry[0], entry[2], entry[3], lengths[0], lengths[1]))
                        crispr_ls.append(line)

            if(crispr):
                json.dump(crispr, open(path_to_crt_report + ".spacers", 'w'))
 
