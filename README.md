# Drivers of Zestimate Error
By: Jason Tellez
Date: September 28, 2021

The goal of this report is to find the main drivers of error between Zestimates and prices of the listed properties. Specifically, we will be looking at single-unit/single-family properties which had transactions in the year 2017. From here, we proceed through the usual stages of the DS pipeline and hopefully find the what drives the error. I will incorporate clustering in my analysis and modeling to possibly better predict the Zestimate error.


## Table of contents

- [Table of contents](#table-of-contents)
- [Project Summary](#project-summary)
- [Executive Summary](#executive-summary)
- [Dictionary](#dictionary)
- [Pipeline](#pipeline)

    -[Acquire](#acquire)
    
    -[Prepare](#prepare)
    
    -[Explore](#explore)
    
    -[Model](#model)
    
    -[Evaluate](#evaluate)
    
    -[Conclusions](#conclusions)
    
- [Recreate these results](#recreate-these-results)


## Project Summary
[(Back to top)](#drivers-of-zestimate-error)

#### Goal
The goal of this report is to find the main drivers of error between Zestimates and prices of the listed properties. Specifically, we will be looking at single-unit/single-family properties which had transactions in the year 2017. From here, we proceed through the usual stages of the DS pipeline and hopefully find the what drives the error. I will incorporate clustering in my analysis and modeling to possibly better predict the Zestimate error.

#### Deliverables
1. A final notebook. This notebook will be presented and should contains markdown documentation and cleaned up code.
2. A README that explains what the project is, how to reproduce the work, and any notes from project planning.
3. A Python module or modules that automate the data acquisistion and preparation process. These modules will be imported and used in the final notebook.


## Executive Summary 
[(Back to top)](#table-of-contents)
### Conclusions & Next Steps
- I found that when properties are separated by bedroom count, specifically those with more than 3 bedrooms versus those the 3 or less bedrooms, the average log error is significantly different between the two subgroups.
- I found that there was no linear relationship between tax value of property and logerror.
- Using square feet and age of property, I found that when I created 5 clusters, the mean logerror was equal across all clusters
- Using latitude, longitude and heating/airconditioning type, I found that when i created 6 clusters, the mean logerror was different across all clusters.
- Using bathroom count, tax rate, and county, I found that when i created 5 clusters, the mean logerror was equal across all 6 clusters.
- I found that my models are not adequete predictors of logerror.
- If i had more time, I would like to investigate any non-linear relationships the features might have. Most notably, the relationship between tax value and log error.


## Data Dictionary
[(Back to top)](#table-of-contents)

**Types of units I aqcuired (propertylandusedesc)**
- 261: Single Family Residential
- 262: Rural Residence
- 263: Mobile Home
- 264: Townhouse
- 265: Cluster home
- 266: Condominium
- 268: Row House
- 271: Timeshare
- 273: Bungalow
- 274: Zero Lot Line
- 275: Manufactured, Modular, Prefabricated Home
- 276: Patio Home
- 279: Inferred Single Family Residential

key|old_key|description
|:------------------|:------------------------|:-------------|                   
age                     |yearbuilt                   |Age of property|
fips                    |fips                        |Federal Information Processing Standard code |
sqft                    |calculatedfinishedsquarefeet|Calculated total finished living area of the home |
lot_sqft                |lotsizesquarefeet           |Area of the lot in square feet |
quality_id              |buildingqualitytypeid       |Quality of build of property |
bath                    |bathroomcnt                 |Number of bathrooms in home including fractional bathrooms |
bed                     |bedroomcnt                  |Number of bedrooms in home |
taxamount               |taxamount                   |The total property tax assessed for that assessment year |
taxvalue                |taxvaluedollarcnt           |The total tax assessed value of the parcel |
living_sqft             |finishedsquarefeet12        |Area of livable sqft of unit  |
full_bath               |fullbathcnt                 |Number of full baths |
latitude                |latitude                    |Coordinate of unit |
longitude               |longitude                   |Coordinate of unit |
landusecode             |propertycountylandusecode   |Code that indicates zone which unit is located |
zone                    |propertyzoningdesc          |Description of zone which property is located |
regionidcity            |regionidcity                |ID of city which property is located |
regionidcounty          |regionidcounty              |ID of county which property is located |
regionidzip             |regionidzip                 |ID of zipcode which property is located |
structure_tax           |structuretaxvaluedollarcnt  |Tax value of structure which unit is located in |
landtax                 |landtaxvaluedollarcnt       |Tax value of parcel which unit is located |
logerror                |logerror                    |Error of Zestimate vs actual price of unit |
heating                 |heatingorsystemdesc         |Type of heating or cooling system the unit has |
landusedesc             |propertylandusedesc         |Type of unit |
transaction_month       |*New column*                |Month where the transaction of unit took place |
tax_rate                |*New column*                |Tax rate of unit (taxvalue / taxamount) |
 
 
## Pipeline
[(Back to top)](#table-of-contents)

### Plan
- Build the README and [Trello board](https://trello.com/b/tuXcQdYs/zillow-clustering-project)
- Gather previously used data from regression project to speed up process
- Plan stages of the pipeline
- Create hypotheses to test

### Acquire
- Create SQL qeury that gathers relevant data from SQL database
- Use code to convert data to CSV file and to pandas dataframe
- Understand the data to prepare for the next phase

### Prepare
- Adress null values
    - Drop columns and rowsmissing too much data
- Impute remaining null values with best method (median, mode) 
- Convert datatypes
- Create new columns
- Rename columns
- Drop outliers
- Split the data
- Scale the data (MinMax)

### Explore
- Test hypotheses
    1. Create null and alternative hypothses
    2. Visualize
    3. Create clusters (if necessary)
    4. Test distribution (if necessary)
    5. Use statistical tests to find answers to original hypothesis
-  At least 3 combinations of features for clustering should be tried

### Model
- Create baseline model to compare future models
- At least 4 different models are created and their performance is compared
- Calculate metrics for each model aid comparison
- Choose best model to evaluate with test dataset (Out-of-sample)

### Conclusions
- Draw conclusions from previous stages
- Determine whether any of the models are useful in finding drivers of error
- Be sad that your model is bad and feel bad


# Recreate these results
[(Back to top)](#drivers-of-zestimate-error)

1. Download this [README](https://github.com/Jason-Tellez/Zillow-clustering-proj/blob/main/README.md)
2. Download the [acquire](https://github.com/Jason-Tellez/Zillow-clustering-proj/blob/main/acquire.py), [prepare](https://github.com/Jason-Tellez/Zillow-clustering-proj/blob/main/prepare.py), and [model](https://github.com/Jason-Tellez/Zillow-clustering-proj/blob/main/model.py) modules
3. Acquire credentials (env) to database
4. Download [the final jupyter notebook](https://github.com/Jason-Tellez/Zillow-clustering-proj/blob/main/zillow_clustering_report.ipynb) and run all cells
