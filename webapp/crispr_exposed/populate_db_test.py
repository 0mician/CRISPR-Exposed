import json
import re
import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crispr_exposed.settings') #crispr_exposed.settings_prod

import django
django.setup()

from crispr.models import Strain, CrisprArray, CrisprEntry

data = "../../data/"
crt_re = re.compile('.*\.crt\.report')
spacers_re = re.compile('.*\.crt\.report\.spacers')
meta_handle = "_meta.txt"

# keep track of progress
number_of_folders = len([name for name in os.listdir(data)])
count = 1

def add_strain(
        refseq_id,
        organism_name,
        strain,
        clade_id,
        bio_sample,
        bio_project,
        group,
        sub_group,
        assembly,
        size,
        gc_content,
        replicons,
        wgs,
        scaffolds,
        genes,
        proteins,
        release_date,
        modification_date,
        level,
        refseq_ftp,
        genbank_ftp):

    # problems with incomplete data - quick fix
    if(clade_id == "-"):
        clade_id = -1
    if(scaffolds == "-"):
        scaffolds = -1
    if(genes == "-"):
        genes = -1
    if(proteins == "-"):
        proteins = -1

    strain = Strain.objects.get_or_create(
        refseq_id=refseq_id,
        organism_name=organism_name,
        strain=strain,
        clade_id=clade_id,
        bio_sample=bio_sample,
        bio_project=bio_project,
        group=group,
        sub_group=sub_group,
        assembly=assembly,
        size=size,
        gc_content=gc_content,
        replicons=replicons,
        wgs=wgs,
        scaffolds=scaffolds,
        genes=genes,
        proteins=proteins,
        release_date=release_date,
        modification_date=modification_date,
        level=level,
        refseq_ftp=refseq_ftp,
        genbank_ftp=genbank_ftp)[0]
    return strain
        
def add_crispr_array(refseq_id, array_id, start, end):
    crispr_array = CrisprArray.objects.get_or_create(
        refseq_id=refseq_id, array_id=array_id,
        start=start, end=end)[0]
    return crispr_array

def add_crispr_entry(array, position, repeat, spacer, length_repeat, length_spacer):
    crispr_entry = CrisprEntry.objects.get_or_create(
        array=array, 
        position=position, 
        repeat=repeat, 
        spacer=spacer,
        length_repeat=length_repeat,
        length_spacer=length_spacer)[0]

def populate_db():
    # keep track of progress
    number_of_folders = len([name for name in os.listdir(data)])
    progress_counter = 1

    ASSEMBLY_LEVEL = {
        'Complete Genome': 'COMP',
        'Chromosome': 'CHRO',
        'Scaffold': 'SCAF',
        'Contig' : 'CONT'}

    dir_list = os.listdir(data)
    for folder in dir_list:

        print("Processing folder %i out of %i" % (progress_counter, number_of_folders))
        progress_counter += 1

        # add strain (info stored in the meta.txt file)
        strain = None
        with open(os.path.join(data + folder, folder+meta_handle), 'r') as meta:
            features = json.load(meta)
            print(features["#Organism/Name"])
            strain = add_strain(folder, features["#Organism/Name"], features["Strain"], 
                                features["CladeID"], features["BioSample"], 
                                features["BioProject"], features["Group"],
                                features["SubGroup"], features["Assembly"],
                                features["Size (Mb)"], features["GC%"], 
                                features["Replicons"], features["WGS"], 
                                features["Scaffolds"], features["Genes"],
                                features["Proteins"], 
                                datetime.datetime.strptime(features["Release Date"], '%Y/%m/%d').date(), 
                                datetime.datetime.strptime(features["Modify Date"], '%Y/%m/%d').date(),
                                ASSEMBLY_LEVEL[features["Level"]],
                                features["RefSeq FTP"], features["GenBank FTP"])
            
        # add crispr array (info stored in the .crt.report.spacers file)
        file_list = os.listdir(data + folder)
        for _file in file_list:
            spacers_report_file_name = re.search(spacers_re, _file)
            if(spacers_report_file_name):
                with open(os.path.join(data + folder, 
                                       spacers_report_file_name.group()),'r') as spacers_file:
                    spacers = json.load(spacers_file)
                    array = None
                    count = 1
                    for key in sorted(spacers):
                        details = spacers[key]['details']
                        array = add_crispr_array(strain, count, details[0], details[1])
                        spacers_list = spacers[key]['array']
                        count += 1
                        for spacer in spacers_list:
                            add_crispr_entry(array, spacer[0], 
                                             spacer[1], spacer[2],
                                             spacer[3], spacer[4])

if __name__ == '__main__':
    print("Starting crispr population script...")
    populate_db()
    print("Done!")
