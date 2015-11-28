/* Script used during development to export data to /var/lib/mysql/crisprdb/export.csv
   for dataviz */

USE crisprdb;

-- exports to /var/lib/mysql/crisprdb/export.csv

SELECT * FROM crispr_crisprentry CE 
JOIN crispr_crisprarray CA ON CE.array_id = CA.id 
JOIN crispr_strain CS ON CA.refseq_id_id = CS.id 
INTO OUTFILE 'export.csv' 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';
