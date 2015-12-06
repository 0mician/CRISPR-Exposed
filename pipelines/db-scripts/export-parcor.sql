/* Script used during development for dataviz */

USE crisprdb;

/* Export of the strains that contain putative CRISPR arrays, and the
   count of arrays present in the strain */

SELECT temp.refseq_id, temp.group, temp.level, temp.size, count(*) AS count 
FROM (
     SELECT CS.refseq_id, CS.group, CS.level, CS.size, CA.id 
     FROM crispr_strain CS 
     JOIN crispr_crisprarray CA ON CA.refseq_id_id = CS.id
) AS temp
GROUP BY temp.refseq_id, temp.group, temp.level, temp.size
INTO OUTFILE 'report_piechart_arraycount_per_strains.csv' 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';

/* Export of the strains that do not contain putative CRISPR arrays */

SELECT CS.refseq_id, CS.group, CS.level, CS.size, CA.id 
FROM crispr_strain CS 
LEFT JOIN crispr_crisprarray CA ON CA.refseq_id_id = CS.id 
WHERE CA.id IS NULL 
INTO OUTFILE 'report_piechart_0arrays.csv' 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';

