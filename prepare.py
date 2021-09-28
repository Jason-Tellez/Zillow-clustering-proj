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
import sklearn.preprocessing


################### Cleans the data ###################

def clean_data(df, outlier_cols, k):
    """
    Function takes in dataframe, columns to drop outliers from, and a scalar to compute IQR.
    Drops columns missing more than 50% of values 
    Drops rows missing more than 50% of values
    Fills remaining columns with either median or mode values
    Creates new transaction month column
    Converts yearbuilt to age column
    Drops duplicated rows
    Converts datatypes
    Removes outliers according to inputted k value
    Returns a cleaned dataframe.
    """
    df = df.dropna(axis=0, thresh=df.shape[1]*.50).dropna(axis=1, thresh=df.shape[0]*.50)
    df = df.drop(columns=['id', 'parcelid', 'assessmentyear', 'roomcnt', 'unitcnt', 'censustractandblock',
                          'rawcensustractandblock', 'propertylandusetypeid', 'heatingorsystemtypeid', 'calculatedbathnbr'])
    mode_cols = ['buildingqualitytypeid', 'fullbathcnt', 'propertyzoningdesc', 'regionidcity', 'regionidzip', 'yearbuilt',
                 'heatingorsystemdesc']

    # For discrete/categorical variables, i will impute the mode
    for col in mode_cols:
        df[col].fillna(value=df[col].mode()[0], inplace=True)
    # For continuous variables, i will impute the median
    median_cols = ['calculatedfinishedsquarefeet', 'finishedsquarefeet12', 'lotsizesquarefeet',
                   'structuretaxvaluedollarcnt', 'taxamount']
    for col in median_cols:
        df[col].fillna(value=df[col].median(), inplace=True)

    # Create columns for investigation
    # transaction month
    x=[]
    for value in df.transactiondate:
        x.append(value[5:7])
    df['transaction_month'] = x
    df.drop(columns='transactiondate', inplace=True)
    df.transaction_month = df.transaction_month.replace('0', '').astype(int)
    # convert yearbuilt to age column
    y=[]
    for value in df.yearbuilt.astype(int):
        y.append(2021-value)
    df.yearbuilt = y
    # tax_rate column
    df['tax_rate'] = df.taxvaluedollarcnt / df.taxamount    
        
    # Drop duplicate rows
    df.drop_duplicates(inplace=True)

    # Convert datatypes
    df.bedroomcnt = df.bedroomcnt.astype(int)
    df.buildingqualitytypeid = df.buildingqualitytypeid.astype(int)
    df.fips = df.fips.astype(int)
    df.fullbathcnt = df.fullbathcnt.astype(int)
    df.regionidcounty = df.regionidcounty.astype(int)
    
    # handle outliers
    for col in outlier_cols:
        q1, q3 = df[col].quantile([0.25, 0.75])
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        upper_bound =  q3 + k * iqr
        lower_bound =  q1 - k * iqr
        df = df[(df[col] < upper_bound) & (df[col] > lower_bound)]
    
    # Renames columns
    df.rename(columns={"bathroomcnt": "bath",
        "bedroomcnt": "bed",
        "buildingqualitytypeid": "quality_id",
        "calculatedfinishedsquarefeet": "sqft",
        "finishedsquarefeet12": "living_sqft", 
        #fips
        "fullbathcnt": "full_bath",
        #latitude
        #longitude
        "lotsizesquarefeet": "lot_sqft",
        "propertycountylandusecode": "landusecode",
        "propertyzoningdesc": "zone"  ,           
        #regionidcity
        #regionidcounty
        #regionidzip
        "yearbuilt": "age",
        "structuretaxvaluedollarcnt": "structure_tax",
        "taxvaluedollarcnt": "taxvalue",
        "landtaxvaluedollarcnt": "landtax",
        #taxamount
        #logerror
        "heatingorsystemdesc": "heating",
        "propertylandusedesc": "landusedesc"
        }, inplace=True)
    # Convert objects to numeric using enumerate
    for count, value in enumerate(df.landusecode.unique()):
        df.replace({'landusecode': {value: count}}, inplace=True)
    for count, value in enumerate(df.zone.unique()):
        df.replace({'zone': {value: count}}, inplace=True)
    for count, value in enumerate(df.landusedesc.unique()):
        df.replace({'landusedesc': {value: count}}, inplace=True)
    # Convert heating for easier testing    
    df.replace({'heating': {'Central': 0,
                    'Floor/Wall': 1,
                    'Forced air': 3,
                    'Yes': 3,
                    'Solar': 3,
                    'None': 3,
                    'Baseboard': 3,
                    'Radiant': 3,
                    'Gravity': 3,
                    'Heat Pump': 3
                   }}, inplace=True)
    
    # Price per livable sqft
    # Since lot sqft must be greater than or equal to livable sqft, I will drop any rows where this isnt the case.
    
    return df

################### Split the data ###################

def train_validate_test_split(df):
    train_and_validate, test = train_test_split(df, train_size=0.8, random_state=123)
    train, validate = train_test_split(train_and_validate, train_size=0.75, random_state=123)
    return train, validate, test





################### Min-max Scaling ###################

def minmax_scaler(X_train, X_validate, X_test, quants):
    """
    Takes in split data and individually scales each features to a value within the range of 0 and 1.
    Uses min-max scaler method from sklearn.
    Returns datasets with new, scaled columns to the added.
    """
    # Scale the data
    scaler = sklearn.preprocessing.MinMaxScaler()

    # Fit the scaler
    scaler.fit(X_train[quants])

    # Use the scaler to transform train, validate, test
    X_train_scaled = scaler.transform(X_train[quants])
    X_validate_scaled = scaler.transform(X_validate[quants])
    X_test_scaled = scaler.transform(X_test[quants])


    # Turn everything into a dataframe
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train[quants].columns)
    X_validate_scaled = pd.DataFrame(X_validate_scaled, columns=X_train[quants].columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_train[quants].columns)
    
    return X_train_scaled, X_validate_scaled, X_test_scaled

                                                           
################### X, y split Funciton ###################

def X_y_split(train, validate, test, target):
    """
    Functions that takes in trainm validate, test, and target var and split to X and y datasets
    """
    # Setup X and y
    X_train = train.drop(columns=target)
    y_train = train[target]

    X_validate = validate.drop(columns=target)
    y_validate = validate[target]

    X_test = test.drop(columns=target)
    y_test = test[target]
    return X_train, y_train, X_validate, y_validate, X_test, y_test

def prep_zillow(df, outlier_cols, k, target):
    """
    Function takes in dataframe, columns to analyze for outliers, and scaler to calculate IQR.
    Calls clean_data function and returns df
    Calls train_validate_test_split and returns train, test, and validate dataframes
    Calls X_y_split and returns appropriate dataframes.
    """
    df = clean_data(df, outlier_cols, k)
    train, validate, test = train_validate_test_split(df)
    X_train, y_train, X_validate, y_validate, X_test, y_test = X_y_split(train, validate, test, target)
    
    return df, X_train, y_train, X_validate, y_validate, X_test, y_test, train, validate, test
    