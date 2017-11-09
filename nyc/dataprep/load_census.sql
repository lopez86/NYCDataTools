USE nyc;
DROP TABLE acs2015;
CREATE TABLE acs2015 (CensusTract BIGINT, 
                         County string, 
                         Borough string, 
                         TotalPop INT, 
                         Men INT, 
                         Women INT, 
                         Hispanic DOUBLE, 
                         White DOUBLE,  
                         Black DOUBLE, 
                         Native DOUBLE, 
                         Asian DOUBLE, 
                         Citizen INT, 
                         Income DOUBLE, 
                         IncomeErr DOUBLE, 
                         IncomePerCap DOUBLE, 
                         IncomePerCapErr DOUBLE, 
                         Poverty DOUBLE, 
                         ChildPoverty DOUBLE, 
                         Professional DOUBLE, 
                         Service DOUBLE, 
                         Office DOUBLE, 
                         Construction DOUBLE, 
                         Production DOUBLE, 
                         Drive DOUBLE, 
                         Carpool DOUBLE, 
                         Transit DOUBLE, 
                         Walk DOUBLE, 
                         OtherTransp DOUBLE,  
                         WorkAtHome DOUBLE, 
                         MeanCommute DOUBLE, 
                         Employed INT, 
                         PrivateWork DOUBLE, 
                         PublicWork DOUBLE, 
                         SelfEmployed DOUBLE, 
                         FamilyWork DOUBLE, 
                         Unemployment DOUBLE) 
                         ROW FORMAT DELIMITED FIELDS 
                             TERMINATED BY ',' 
                          STORED AS TEXTFILE
                          TBLPROPERTIES ("skip.header.line.count"="1");


LOAD DATA INPATH 'nyc_census_tracts.csv' OVERWRITE INTO TABLE acs2015;

