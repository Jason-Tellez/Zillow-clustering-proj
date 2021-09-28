import os
from env import host, user, password
import numpy as np
import pandas as pd

import seaborn as sns
import matplotlib.pyplot as plt

# ignore warnings
import warnings
warnings.filterwarnings("ignore")

from sklearn.metrics import median_absolute_error as mae
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler, PolynomialFeatures
from sklearn.cluster import KMeans
import sklearn.preprocessing
from sklearn.linear_model import LinearRegression, LassoLars
from sklearn.preprocessing import PolynomialFeatures
from sklearn.metrics import mean_squared_error, r2_score, explained_variance_score
from sklearn.feature_selection import SelectKBest, f_regression, RFE
from sklearn.neighbors import KNeighborsRegressor

from scipy import stats

import acquire as a
import prepare as p

pd.set_option('display.float_format', lambda x: '%.5f' % x)


def regression_errors(df, y, yhat):
    residual = df[yhat] - df[y]
    residual_sq = residual**2
    SSE = residual_sq.sum()
    ESS = ((df[yhat] - df[y].mean())**2).sum()
    TSS = SSE + ESS
    MSE = SSE/len(df[y])
    RMSE = MSE**0.5
    return SSE, ESS, TSS, MSE, RMSE


def select_feats(scaled_df, k, target):
    # kbest
    kbest = SelectKBest(f_regression, k=k)
    kbest.fit(scaled_df, target)
    X_kbest = scaled_df.columns[kbest.get_support()]

    # recursive feature elimination
    rfe = RFE(estimator=LinearRegression(), n_features_to_select=k)
    rfe.fit(scaled_df, target)
    X_rfe = scaled_df.columns[rfe.get_support()]
    return X_kbest, X_rfe