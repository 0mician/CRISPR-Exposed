/* Script used during development to clean all table records before
   new data import */

USE crisprdb;
SET SQL_SAFE_UPDATES = 0;

/* 3 tables to go through */

DELETE FROM crispr_crisprentry;
ALTER TABLE crispr_crisprentry AUTO_INCREMENT=1;

DELETE FROM crispr_crisprarray;
ALTER TABLE crispr_crisprarray AUTO_INCREMENT=1;

DELETE FROM crispr_strain;
ALTER TABLE crispr_strain AUTO_INCREMENT=1;

SET SQL_SAFE_UPDATES = 1;
