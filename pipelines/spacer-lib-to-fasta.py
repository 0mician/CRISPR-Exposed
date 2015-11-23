import os
import configparser
import MySQLdb

config = configparser.ConfigParser()
config.read('config.ini')

fasta_out = open('spacers.fasta', 'w')

db = MySQLdb.connect(db=config['mysql']['db'],
                     user=config['mysql']['user'], 
                     passwd=config['mysql']['passwd'])

c = db.cursor()
c.execute("""SELECT ce.id,ce.spacer,ca.id,cs.refseq_id,cs.organism_name FROM crispr_crisprentry ce JOIN crispr_crisprarray ca ON ce.array_id = ca.refseq_id_id JOIN crispr_strain cs ON ca.refseq_id_id = cs.id LIMIT 10""")

entries = c.fetchall()

# entry format: (entry_id, spacer, array_id, refseq_id, strain_name)
# output: >entry_id,array_id,refseq_id,strain_name
#         spacer
for entry in entries:
    fasta_out.write(">" + str(entry[0]) + "," + str(entry[2]) + "," +
                    str(entry[3]) + "," + str(entry[4]) + "\n")
    fasta_out.write(entry[1] + "\n")

fasta_out.close()
