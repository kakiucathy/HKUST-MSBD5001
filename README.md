# MSBD5001
#I used Python and ran the code in google colab.

#The code can be reproduced using google colag.

#Import Library
import numpy as np
import pandas as pd
from sklearn import model_selection
from sklearn.model_selection import train_test_split as split
from sklearn.metrics import accuracy_score as accuracy
import statsmodels.api as sm
from sklearn.ensemble import *
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import mean_squared_error

I first imported the required packages and libraries. Then I manipulated train data set and test data set using excel. 
I used excel to calculate difference between release date and purchase data. 
If one of the dates are 0, I calculated the mean between the date we have(the non zero date) and the latest date of zero zero date and considered it as the date difference.
Then imported train data set and manipulated string to dummy variables.
After handling the data, performed backward elimination to drop features in order to prevent overfitting.
Dropped features that are not important and combined review data.
Built model using Bagging Regressor.
Evaluated model performance using R^2 and MSE. R^2 in 2 submission are >0.86.

Imported test data and manipulated data using the same way in train data.
Predicted result and export file for Submission.
