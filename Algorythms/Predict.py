from sklearn.pipeline import Pipeline
import pickle
from sklearn.naive_bayes import GaussianNB
from sklearn import cross_validation
import xgboost
from sklearn.cross_validation import train_test_split
import numpy as np
import pandas as pd
from sklearn import datasets
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.linear_model import Lasso, RidgeCV, LassoCV
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from os import getcwd
from sys import platform

def prediction(pickle_path, data):
    Predictor = None
    with open(pickle_path, 'rb') as f:
        Predictor = pickle.load(f)
    data_ready = data.drop(['Company'], axis = 1).values
    # scaler
    y_pred = Predictor.predict(data_ready)
    return y_pred