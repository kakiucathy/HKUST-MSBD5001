# -*- coding: utf-8 -*-
"""Copy of MSBD5001_new

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1HP351vX08tyr0tgVG_vB_pKdDaUAwfSb
"""

import numpy as np
import pandas as pd
from math import log
from sklearn import model_selection
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import accuracy_score as accuracy
import xgboost as xgb

dataframe_training = pd.read_csv("train.csv")
y_train=dataframe_training['playtime_forever']
train_categories=dataframe_training['categories']
train_dummies_categories= train_categories.str.get_dummies(",")
train_genres=dataframe_training['genres']
train_dummies_genres= train_genres.str.get_dummies(",")
dataframe_training=dataframe_training.filter(items=['price','date_difference','total_positive_reviews','total_negative_reviews'])
x_train=pd.concat([dataframe_training,train_dummies_genres,train_dummies_categories], axis=1, sort=False)

import statsmodels.api as sm
X_1 = sm.add_constant(x_train)
model_1= sm.OLS(y_train,X_1).fit()
model_1.pvalues

cols = list(x_train.columns)
pmax = 1
while (len(cols)>0):
    p= []
    X_1 = x_train[cols]
    X_1 = sm.add_constant(X_1)
    model = sm.OLS(y_train,X_1).fit()
    p = pd.Series(model.pvalues.values[1:],index = cols)      
    pmax = max(p)
    feature_with_p_max = p.idxmax()
    if(pmax>0.05):
        cols.remove(feature_with_p_max)
    else:
        break
selected_features_BE = cols
print(selected_features_BE)

x_train=x_train.filter(items=['date_difference', 'total_positive_reviews', 'total_negative_reviews', 'Adventure', 'RPG', 'Full controller support', 'Steam Workshop', 'price'])
x_train['reviews']=x_train['total_positive_reviews']+x_train['total_negative_reviews']
x_train=x_train.filter(items=['date_difference', 'reviews', 'Adventure', 'RPG', 'Full controller support', 'Steam Workshop', 'price'])

Xtrain, Xtest, Ytrain, Ytest = split(x_train,y_train, test_size=0.25, random_state=7)

from sklearn.ensemble import *
AllRegressorModel = [BaggingRegressor]

def Model_Selection_By_Cross_Valid():
        ThisRound_SelectedModel = None
        ThisRound_SelectedModel_Name = None
        ThisRound_SelectedModel_Score = None
        for temp_select_model_name in AllRegressorModel:
            kfold = model_selection.KFold(n_splits=10, random_state=7)
            print (kfold)
            temp_model= temp_select_model_name()
            print(temp_model)
            temp_model.fit(Xtrain, Ytrain)
            results = model_selection.cross_val_score(temp_model, Xtrain, Ytrain, cv=kfold, scoring='neg_mean_squared_error')
        print(temp_select_model_name,results.mean())
        if (ThisRound_SelectedModel == None) or (abs(results.mean()) < ThisRound_SelectedModel_Score):
            ThisRound_SelectedModel = temp_model
            ThisRound_SelectedModel_Name = temp_select_model_name
            ThisRound_SelectedModel_Score = abs(results.mean())
        print ("This round Model Name: ", temp_model,"MSE Score: ",abs(results.mean()))
        print ("This Model Feature Importance",temp_model.feature_importances_)
        print("This Model Do No Have Feature Importance......")
        print ("<----------------------------------->")
        print ("Selected Model Name:", ThisRound_SelectedModel, "MSE Score:",ThisRound_SelectedModel_Score)
        return {"ModelName": ThisRound_SelectedModel_Name,"Model": ThisRound_SelectedModel}

SelectedModel = Model_Selection_By_Cross_Valid()

predictmodel_new=BaggingRegressor(base_estimator=None, bootstrap=True, bootstrap_features=False,
                 max_features=1.0, max_samples=1.0, n_estimators=10,
                 n_jobs=None, oob_score=False, random_state=7, verbose=0,
                 warm_start=False)

predictmodel_new.fit(x_train,y_train)

y_train_predict=predictmodel_new.predict(x_train)

from sklearn.metrics import r2_score
r2_score(y_train, y_train_predict)

from sklearn.metrics import mean_absolute_error
mean_absolute_error(y_train, y_train_predict)

from sklearn.metrics import mean_squared_error
mean_squared_error(y_train, y_train_predict)

dataframe_testing = pd.read_csv("test.csv")
test_categories=dataframe_testing['categories']
test_dummies_categories= test_categories.str.get_dummies(",")
test_genres=dataframe_testing['genres']
test_dummies_genres= test_genres.str.get_dummies(",")
dataframe_testing=dataframe_testing.filter(items=['price','date_difference','total_positive_reviews','total_negative_reviews'])
x_test=pd.concat([dataframe_testing,test_dummies_genres,test_dummies_categories], axis=1, sort=False)

x_test=x_test.filter(items=['date_difference', 'total_positive_reviews', 'total_negative_reviews', 'Adventure', 'RPG', 'Full controller support', 'Steam Workshop', 'price'])
x_test['reviews']=x_test['total_positive_reviews']+x_test['total_negative_reviews']
x_test=x_test.filter(items=['date_difference', 'reviews', 'Adventure', 'RPG', 'Full controller support', 'Steam Workshop', 'price'])

x_test=x_test.filter(items=['date_difference','total_positive_reviews', 'total_negative_reviews','Adventure','RPG','Co-op ','Full controller support','Includes level editor ','Steam Workshop','price'])
x_test

x_test

Predicted = predictmodel_new.predict(x_test)

Predicted=pd.DataFrame(Predicted)

from google.colab import files
Predicted.to_csv('Submission_88675.csv') 
files.download('Submission_88675.csv')