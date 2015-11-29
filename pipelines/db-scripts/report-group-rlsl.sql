/* Script used during development to export unique counts of given (group, repeat length, spacer length)
   to /var/lib/mysql/crisprdb/report_group_rl_sl.csv for dataviz */

USE crisprdb;

SELECT temp.group, temp.length_repeat, temp.length_spacer, count(*) AS count 
FROM (
     SELECT CS.group, CE.length_repeat, CE.length_spacer 
     FROM crispr_crisprentry CE 
     JOIN crispr_crisprarray CA ON CE.array_id = CA.id 
     JOIN crispr_strain CS ON CA.refseq_id_id = CS.id LIMIT 10
) AS temp
GROUP BY temp.group, temp.length_repeat, temp.length_spacer 
INTO OUTFILE 'report_group_sl_rl.csv' 
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"' 
LINES TERMINATED BY '\n';
