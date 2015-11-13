import re
import os
import gzip
import json

import pandas as pd
from ftplib import FTP

ncbi_ftp = "ftp.ncbi.nlm.nih.gov"
input_report = "Data/genomes_proks_complete_and_chr.csv"
output_folder = "../Data/"
path_folder = re.compile('(?<=ftp.ncbi.nlm.nih.gov).*')
refseq = re.compile('(?<=genomes/all/).*')

try:
    print("Connection to %s" % ncbi_ftp)
    ftp = FTP(ncbi_ftp)
    ftp.login()
    print("Connected")
except:
    print("Connection issues")
    ftp.quit()

df = pd.read_csv(input_report)
nb_rows = len(df)
features = df.dtypes.index

counter = 1
limit = 10 # just for testing

for row in range(nb_rows):
    ftp_address = df.ix[row]["RefSeq FTP"]
    print("Fetching annotations and genome %i out of %i" % (counter, nb_rows))
    counter += 1
    if(counter == limit): 
        break

    if(ftp_address != "-"): # not taking genbank into account
        folder = re.search(path_folder, ftp_address).group()

        # create destination dir with refseq as folder name
        rs = re.search(refseq, folder).group()
        outdir = os.path.join(output_folder, rs)
        if not os.path.exists(outdir):
            os.makedirs(outdir)
        else:
            continue
        
        # fetch ftp files for sequence and annotation
        ftp.cwd(folder)
        sequence_handle= "_genomic.fna.gz"
        sequence_file = os.path.join(outdir, rs + sequence_handle)
        features_handle = "_feature_table.txt.gz"
        features_file = os.path.join(outdir, rs + features_handle)
        try:
            ftp.retrbinary('RETR %s' % rs + sequence_handle, open(sequence_file, 'wb').write)
            ftp.retrbinary('RETR %s' % rs + features_handle, open(features_file, 'wb').write)
        except:
            print("Error fetching file %s - does not exit" % rs)
            continue
		
        # extracting fasta 
        with gzip.open(sequence_file, 'rb') as f:
            file_content = f.read()
            output_file = open(os.path.join(outdir, rs + "_genomic.fna"), 'wb')
            output_file.write(file_content)
            output_file.close()
        
        # extracting annotation
        with gzip.open(features_file, 'rb') as f:
            file_content = f.read()
            output_file = open(os.path.join(outdir, rs + "_genomic.gff"), 'wb')
            output_file.write(file_content)	
            output_file.close()
		
        os.remove(features_file)
        os.remove(sequence_file)

        print("%s fetched!" % rs)
        
        if(df.ix[row]["RefSeq FTP"] == ftp_address):
            meta_content = { name:str(df.ix[row][name]) for name in features }
            json.dump(meta_content, open(os.path.join(outdir, rs + "_meta.txt"), 'w'))
            
print("Closing connection")
ftp.quit()
