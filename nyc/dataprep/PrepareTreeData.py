#! /usr/bin/env python3
""" PrepareTreeData.py
Prepares the tree data a bit for inclusion into a database.


"""
import pandas as pd
import numpy as np


""" Prepare the tree data for inclusion into a database.

Args:
    inname: Input file
    outname: Output file
"""
def PrepareTreeData(inname='data/street_trees_2015.csv',
                    outname='trees_2015.csv'):

    trees = pd.read_csv(inname,index_col=0)
    trees = trees.drop(['state','x_sp','y_sp','zip_city',
                        'cncldist','st_assem','st_senate',
                        'problems','address'
                        ],axis=1)

    boromap = {'1':'36061','2':'36005','3':'36047','4':'36081','5':'36085'}

    def map_date(date):
        m = date[0:2]
        d = date[3:5]
        y = date[-4:]
        return y + '-'+m+'-'+d
    trees.created_at = trees.created_at.map(map_date)

    def get_tract(boro_ct):
        boro_ct = str(boro_ct)
        return int(boromap[boro_ct[0]] + boro_ct[1:])
    trees['tract'] = trees.boro_ct.map(get_tract)
    trees = trees.drop('boro_ct',axis=1)
    cols = [col for col in trees.columns]
    cols.remove('boroname')
    cols.append('boroname')
    trees = trees.loc[:,cols]
    trees.to_csv(outname)

    
""" Runs with default arguments"""
def main():
    PrepareTreeData()

if __name__=='__main__':
    main()
