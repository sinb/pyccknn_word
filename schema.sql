# word table
create table `russian_chn` (id int primary key auto_increment, word varchar(20) not null, variants text, meaning text not null) charset=utf8;
# user table 

#random select
SELECT * FROM `russian_chn` AS t1 JOIN (SELECT ROUND( RAND( ) * (SELECT MAX( id ) FROM `russian_chn` ) ) AS id) AS t2 WHERE t1.id >= t2.id ORDER BY t1.id ASC LIMIT 1 
