import os
from env import host, user, password
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


################### Connects to Sequel Ace using credentials ###################

def get_connection(db, user=user, host=host, password=password):
    '''
    This function uses my info from my env file to
    create a connection url to access the Codeup db.
    It takes in a string name of a database as an argument.
    '''
    return f'mysql+pymysql://{user}:{password}@{host}/{db}'


################### Create new dataframe from SQL db ###################
    
def new_zillow_data():
    '''
    This function reads the zillow data from the Codeup db into a df,
    writes it to a csv file, and returns the df.
    '''

    # Create SQL query.
    sql_query = """
            SELECT 	prop.*, 
                ac.airconditioningdesc,
                txn.transactiondate, 
                pred.logerror, 
                ast.architecturalstyledesc,
                bc.buildingclassdesc,
                hs.heatingorsystemdesc,
                plu.propertylandusedesc,
                st.storydesc,
                tc.typeconstructiondesc
            FROM properties_2017 prop
            JOIN (
                SELECT parcelid, max(transactiondate) as transactiondate
                FROM predictions_2017
                GROUP BY parcelid
                ) AS txn ON prop.parcelid = txn.parcelid
            JOIN predictions_2017 AS pred  
            ON prop.parcelid = pred.parcelid 
                AND pred.transactiondate = txn.transactiondate
            LEFT JOIN airconditioningtype AS ac
            USING(airconditioningtypeid)
            LEFT JOIN architecturalstyletype AS ast
            USING (architecturalstyletypeid)
            LEFT JOIN buildingclasstype AS bc
            USING (buildingclasstypeid)
            LEFT JOIN heatingorsystemtype AS hs
            USING (heatingorsystemtypeid)
            LEFT JOIN propertylandusetype AS plu
            USING (propertylandusetypeid)
            LEFT JOIN storytype AS st
            USING (storytypeid)
            LEFT JOIN typeconstructiontype AS tc
            USING (typeconstructiontypeid)
            WHERE COALESCE(prop.longitude, prop.latitude) IS NOT NULL
                AND propertylandusetypeid IN ('261', '262', '263', '264', '265', '266', '268', '271', '273', '274', '275', '276', '279'); 
            """
    # Read in DataFrame from Codeup's SQL db.
    df = pd.read_sql(sql_query, get_connection('zillow'))
    
    return df


################### Acquire existing csv file ###################

def get_zillow_data():
    '''
    This function reads in zillow data from Codeup database, writes data to
    a csv file if a local file does not exist, and returns a df.
    '''
    if os.path.isfile('zillow.csv'):
        
        # If csv file exists, read in data from csv file.
        df = pd.read_csv('zillow.csv', index_col=0)
        
    else:
        
        # Read fresh data from db into a DataFrame.
        df = new_zillow_data()
        
        # Write DataFrame to a csv file.
        df.to_csv('zillow.csv')
        
    return df


def summarize_stats(df):
    print("YOU CAN'T HANDLE THE STATS!!!!!!")
    print('|------------------------------------------------------|')
    print('|------------------------------------------------------|')
    print(f'Shape: {df.shape}')
    print('|------------------------------------------------------|')
    print(df.info())
    print('|------------------------------------------------------|')
    print('|------------------------------------------------------|')
    for col in df.columns:
        print(f'|-------{col}-------|')
        print()
        print(f'dtpye: {df[col].dtype}')
        print()
        print(f'Null count: {df[col].isnull().sum()}')
        print()
        print(df[col].describe())
        print()
        print(df[col].value_counts())
        print()
        print(df[col].unique())
        print('|------------------------------------------------------|')
        print('|------------------------------------------------------|')