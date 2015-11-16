import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crispr_exposed.settings')

import django
django.setup()

from crispr.models import Strain, CrisprArray, CrisprEntry

input_folder = "../../data/"
crt_re = re.compile('.*\.crt\.report')
spacers_re = re.compile('.*\.crt\.report\.spacers')
meta_handle = "_meta.txt"

# keep track of progress
number_of_folders = len([name for name in os.listdir(input_folder)])
count = 1

def add_strain(
        refseq_id,
        slug,
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
    
    strain = Strain.objects.get_or_create(
        refseq_id=refseq_id,
        slug=slug,
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
        
def add_crispr_array(refseq_id, array_id):
    crispr_array = CrisprArray.objects.get_or_create(
        refseq_id=refseq_id, array_id=array_id)[0]
    return crispr_array

def add_crispr_entry(array, position, repeat, spacer, length_repeat, length_spacer):
    crispr_entry = CrisprEntry.objects.get_or_create(
        array=array, 
        position=position, 
        left_flank=left_flank,
        repeat=repeat, 
        spacer=spacer,
        length_repeat=length_repeat,
        length_spacer=length_spacer)[0]

def populate_db():
    pass

if __name__ == '__main__':
    print("Starting crispr population script...")
    populate_db()
    print("Done!")
