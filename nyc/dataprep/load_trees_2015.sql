USE nyc;
DROP TABLE trees2015;
DROP TABLE trees2015_tmp;
CREATE TABLE trees2015_tmp (
                tree_id       INT,
                block_id      INT,
                created_at    DATE,
                tree_dbh      SMALLINT,
                stump_diam    SMALLINT,
                curb_loc      string,
                status        string,
                health        string,
                spc_latin     string,
                spc_common    string,
                steward       string,
                guards        string,
                sidewalk      string,
                user_type     string,
                root_stone    string,
                root_grate    string,
                root_other    string,
                trunk_wire    string,
                trnk_light    string,
                trnk_other    string,
                brch_light    string,
                brch_shoe     string,
                brch_other    string,
                zipcode       SMALLINT,
                cb_num        SMALLINT,
                borocode      TINYINT,
                nta           string,
                nta_name      string,
                latitude      DOUBLE,
                longitude     DOUBLE,
                tract         BIGINT,
                boroname      string)
                    ROW FORMAT DELIMITED FIELDS 
                         TERMINATED BY ',' 
                     STORED AS TEXTFILE
                     TBLPROPERTIES ("skip.header.line.count"="1");

LOAD DATA INPATH 'trees_2015.csv' OVERWRITE INTO TABLE trees2015_tmp;

SET hive.exec.dynamic.partition=true;
SET hive.exec.dynamic.partition.mode=nonstrict;

CREATE TABLE trees2015 (
                tree_id       INT,
                block_id      INT,
                created_at    DATE,
                tree_dbh      SMALLINT,
                stump_diam    SMALLINT,
                curb_loc      string,
                status        string,
                health        string,
                spc_latin     string,
                spc_common    string,
                steward       string,
                guards        string,
                sidewalk      string,
                user_type     string,
                root_stone    string,
                root_grate    string,
                root_other    string,
                trunk_wire    string,
                trnk_light    string,
                trnk_other    string,
                brch_light    string,
                brch_shoe     string,
                brch_other    string,
                zipcode       SMALLINT,
                cb_num        SMALLINT,
                borocode      TINYINT,
                nta           string,
                nta_name      string,
                latitude      DOUBLE,
                longitude     DOUBLE,
                tract         BIGINT)
                PARTITIONED BY (boroname string)
                CLUSTERED BY (cb_num) SORTED BY(spc_common) INTO 16 BUCKETS
                     ROW FORMAT DELIMITED FIELDS 
                         TERMINATED BY ',' 
                     STORED AS TEXTFILE
                     TBLPROPERTIES ("skip.header.line.count"="1");

INSERT OVERWRITE TABLE trees2015 PARTITION(boroname) 
       SELECT * FROM trees2015_tmp;

DROP TABLE trees2015_tmp;
