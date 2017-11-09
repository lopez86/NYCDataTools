#! /usr/bin/env python3
""" PrepareCensusData.py

    Reads in the basic population and economic characteristics data
    from the US American Community Survey and 
"""


import pandas as pd
from sqlalchemy import create_engine
""" Reads in the raw CSV census files and outputs a combined file.

Currently, two output formats are allowed: A CSV file, and
a MySQL table. CSV will be good for shorter datafiles. A database
will likely be much more effective if a large dataset, such as the census 
tracts for the entire country, is used.

I may add Hive support as well. This would be useful on a large dataset,
as things like partitioning by states would allow for fast lookup.

Required packages: Pandas, SQLalchemy.

Args:
    pop_file: The path to the file holding the population data.
              Should be table DP05.
    econ_file: The path to the economic data. Should be table DP03.
    output_csv: Create a CSV file as output.
    csv_fname: The name of the output csv file.
    output_mysql: Adds as a table to a MySQL database using SQLalchemy.
    mysql_uname: The MySQL username.
    mysql_password: The MySQL password for that user.
    mysql_dbname: The MySQL database to use on localhost.
"""
def prepare_census_data(pop_file='raw_census_data/ACS_15_5YR_DP05.csv',
                        econ_file='raw_census_data/ACS_15_5YR_DP03.csv',
                        output_csv=True,
                        csv_fname='nyc_census_data.csv',
                        output_mysql=False,
                        mysql_uname='',
                        mysql_password='',
                        mysql_dbname='nyc'):

    df1 = pd.read_csv(pop_file,index_col=1) ## Population 
    df2 = pd.read_csv(econ_file,index_col=1) ## Economic characteristics

  
    df = df1[['HC01_VC03']] 
    df.index.name = 'CensusTract'

    df.columns = (['TotalPop'])
    df['Borough'] = (df.index.values//1000000) % 100
    df['County'] = df['Borough']
    df['Borough'] = df['Borough'].map({5:'Bronx',47:'Brooklyn',
                                       61:'Manhattan',81:'Queens',
                                       85:'Staten Island'})
    df['County'] = df['County'].map({5:'Bronx',47:'Kings',
                                     61:'New York',81:'Queens',
                                     85:'Richmond'})
    df = df[['County','Borough','TotalPop']]
    df['Men'] = df1['HC01_VC04']
    df['Women'] = df1['HC01_VC05']
    df['Hispanic'] = df1['HC03_VC88']

    df['White'] = df1['HC03_VC94']
    df['Black'] = df1['HC03_VC95']
    df['Native'] = df1['HC03_VC96']
    df['Asian'] = df1['HC03_VC97']
    df['Citizen'] = df1['HC03_VC108']
    df['Income'] = df2['HC01_VC85'] # Median household income
    df['IncomeErr'] = df2['HC02_VC85'] # Median household income
    df['IncomePerCap'] = df2['HC01_VC118'] # Median household income
    df['IncomePerCapErr'] = df2['HC02_VC118'] # Median household income
    df['Poverty'] = df2['HC03_VC171'] # 
    df['ChildPoverty'] = df2['HC03_VC172'] # Median household income
    df['Professional'] = df2['HC03_VC41']
    df['Service'] = df2['HC03_VC42']
    df['Office'] = df2['HC03_VC43']
    df['Construction'] = df2['HC03_VC44']
    df['Production'] = df2['HC03_VC45']
  ##
    df['Drive'] = df2['HC03_VC28']
    df['Carpool'] = df2['HC03_VC29']
    df['Transit'] = df2['HC03_VC30']
    df['Walk'] = df2['HC03_VC31']
    df['OtherTransp'] = df2['HC03_VC32']
    df['WorkAtHome'] = df2['HC03_VC33']
    df['MeanCommute'] = df2['HC01_VC36']

  ## 
    df['Employed'] = df2['HC03_VC66']
    df['PrivateWork'] = df2['HC03_VC67']
    df['PublicWork'] = df2['HC03_VC68']
    df['SelfEmployed'] = df2['HC03_VC69']
    df['FamilyWork'] = df2['HC03_VC70']

    df['Unemployment'] = df2['HC03_VC12']
 
    for col in df.columns[3:]:
        df[col] = pd.to_numeric(df[col],errors='coerce')

    if output_csv==True:
        df.to_csv(csv_fname,index=True)

    if output_mysql==True:
        engine = create_engine(
                     'mysql+mysqldb://{}:{}@localhost/{}'.format(
                          mysql_uname,mysql_password,mysql_dbname)
                     )
        df.to_sql('acs2015',engine,if_exists='fail')

""" Runs the default arguments (CSV file only). """
def main():
    prepare_census_data()

if __name__=='__main__':
    main()
