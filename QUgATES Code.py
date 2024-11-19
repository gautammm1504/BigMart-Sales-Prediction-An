# -*- coding: utf-8 -*-
"""Another copy of BIG MART SALES PREDICTION

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Zl_2zKKvla1fTw2d5KvmGzsDZzixY1mC

Importing the libraries
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn import metrics

"""DATA COLLECTION AND ANALYSIS"""

#LOADING THE DATASET
bmd=pd.read_csv('/content/Train.csv')
bmd.head(5) #first 5 rows

bmd.shape #number od datapoints and features

bmd.info()

"""Categorical features


*   Item_Identifier
*   Item_Fat_Content
*   Item_Type
*   Outlet_Identifier
*   Outlet_Size
*   Outlet_Location_type
*   Outlet_Type













"""

#missing values
bmd.isnull().sum()

"""Handling missing value

Imputation (mean) ---> Item_Weight column as it is numeric

mode ---> Outlet_size as it is categorical
"""

#mean value for Item_Weight column
bmd['Item_Weight'].mean()

plt.figure(figsize=(2,2))
bmd.boxplot('Item_Weight')

#filling the missing values in "Item_Weight" column with mean values
bmd['Item_Weight'].fillna(bmd['Item_Weight'].mean(),inplace=True)

#filling the missing values in "Outlet_Size" with mode value

mode_of_os=bmd.pivot_table(values='Outlet_Size',columns='Outlet_Type',aggfunc=(lambda x:x.mode()[0]))
print(mode_of_os)
print(mode_of_os['Grocery Store'].Outlet_Size)

#mode_func=df.pivot_table(values='CrimeGroup_Name',columns='Beat_Name',aggfunc=(lambda x:x.mode()[0]))

a=dict(mode_of_os)

b=list(a.values())
for i in range(len(a)):
  print(b[i][0])

missing_values=bmd['Outlet_Size'].isnull()
print(missing_values)

#loc[row,coulumn]
bmd.loc[missing_values,'Outlet_Size'] = bmd.loc[missing_values,'Outlet_Type'].apply(lambda x: mode_of_os[x].Outlet_Size)

bmd['Outlet_Size']

#all null values are removed
bmd.isnull().sum()

bmd.duplicated().sum()

"""Data Analysis"""

bmd.describe()

plt.figure(figsize=(1,2))
sns.pairplot(bmd)

"""Numerical Features"""

sns.set()

#Item_Weight distribution
plt.figure(figsize=(2,2))
sns.distplot(bmd['Item_Weight'])
plt.title('Item_Weight distribution')
plt.show()

#Item_Visibility distribution
plt.figure(figsize=(2,2))
sns.distplot(bmd['Item_Visibility'])
plt.title('Item_Visibility distribution')
plt.show()

"""there is a skewness in item visibility unlike item weight"""

#Item_MRP distribution
plt.figure(figsize=(2,2))
sns.histplot(bmd['Item_MRP'])
plt.title('Item_MRP distribution')
plt.show()

#Item_Outlet_Sales distribution
plt.figure(figsize=(2,2))
sns.distplot(bmd['Item_Outlet_Sales'])
plt.title('Item_Outlet_Sales distribution ')
plt.show()

#Outlet_Establishment_Year

plt.figure(figsize=(6,2))
sns.countplot(x='Outlet_Establishment_Year',data=bmd)
plt.show()

"""Check for Categorical features

Item_Identifier(no need)

Item_Fat_Content

Item_Type

Outlet_Identifier(no need)

Outlet_Size

Outlet_Location_Type

Outlet_Type
"""

#Item_Fat_Content
plt.figure(figsize=(6,2))
sns.countplot(x='Item_Fat_Content',data=bmd)
plt.title('Item_Fat_Content')
plt.show()

"""LF--->low fat

reg--->Regular

Will be changed in preprocessing  
"""

#Item_Type
plt.figure(figsize=(7,2))
sns.countplot(x='Item_Type',data=bmd)
plt.title('Item_Type')
plt.show()

#Outlet_Size
plt.figure(figsize=(7,2))
sns.countplot(x='Outlet_Size',data=bmd)
plt.title('Outlet_Size')
plt.show()

#Outlet_Location_type
plt.figure(figsize=(6,2))
sns.countplot(x='Outlet_Location_Type',data=bmd)
plt.title('Outlet_Location_type')
plt.show()

#Outlet_Type
plt.figure(figsize=(7,2))
sns.countplot(x='Outlet_Type',data=bmd)
plt.title('Outlet_Type')
plt.show()

plt.figure(figsize=(3,3))
sns.heatmap(bmd.corr())

sns.heatmap(bmd.isnull())

"""DATA PREPROCESSING"""

bmd.head()

#cleaning the Item_Fat_Content
bmd['Item_Fat_Content'].value_counts()

bmd.replace({'Item_Fat_Content':{'low fat':'Low Fat','LF':'Low Fat','reg':'Regular'}},inplace=True)

bmd['Item_Fat_Content'].value_counts()

"""Label encoding ---> convert all the categorical values to numerical values

"""

encoder=LabelEncoder()

bmd['Item_Identifier']=encoder.fit_transform(bmd['Item_Fat_Content'])
bmd['Item_Fat_Content']=encoder.fit_transform(bmd['Item_Fat_Content'])
bmd['Item_Type']=encoder.fit_transform(bmd['Item_Type'])
bmd['Outlet_Identifier']=encoder.fit_transform(bmd['Outlet_Identifier'])
bmd['Outlet_Size']=encoder.fit_transform(bmd['Outlet_Size'])
bmd['Outlet_Location_Type']=encoder.fit_transform(bmd['Outlet_Location_Type'])
bmd['Outlet_Type']=encoder.fit_transform(bmd['Outlet_Type'])



bmd.head(5)

"""Splitting features and target"""

X=bmd.drop(columns='Item_Outlet_Sales',axis=1)
Y=bmd['Item_Outlet_Sales']

from sklearn.linear_model import LinearRegression
from sklearn.feature_selection import RFE #eliminate
LR=LinearRegression()                 # [ _,_,_,_ ] ---- [_,_]  eliminatte
                                      # [ ] -----[_,_]            [_,_,_,_]  selection
rfe=RFE(LR,n_features_to_select=8)

rfe.fit(X,Y)

selected_features=X.columns[rfe.support_]

print(selected_features)

X=bmd.drop(["Item_Weight", "Item_Identifier","Item_Type",'Item_Outlet_Sales'],axis=1)
X

"""Splitting the data into training and testing data

"""

X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=2)

print(X.shape,X_train.shape,X_test.shape)

"""Machine learning model training

**XGBOOST REGRESSOR**

ensemble
- bagging   -- 5 --- 5 models ---cumulative
- boosting  -- 5 --- 5 models , wt distribution --- 3 model performnace -- high pri

- stacking  ---
"""

regressor=XGBRegressor()

regressor.fit(X_train,Y_train) #finds the pattern bwt them

"""EVALUATION"""

#PREDICTION ON TRAINING DATA
training_data_prediction=regressor.predict(X_train)

#R squared value

r2_train=metrics.r2_score(Y_train,training_data_prediction)
print(r2_train)

#PREDICTION ON TEST DATA

test_data_prediction=regressor.predict(X_test)

r2_test=metrics.r2_score(Y_test,test_data_prediction)  # overfitting
print(r2_test)

from sklearn.metrics import mean_squared_error
rms = np.sqrt(mean_squared_error(Y_test, test_data_prediction))
print(f'Root Mean Squared Error (RMSE): {rms}')

"""**LInear REGRESSION**"""

from sklearn.linear_model import LinearRegression

regressor2=LinearRegression()

regressor2.fit(X_train,Y_train)

training_data_prediction2=regressor2.predict(X_train)

R2_train=metrics.r2_score(Y_train,training_data_prediction2)
print(R2_train)

test_data_prediction2=regressor2.predict(X_test)

R2_test=metrics.r2_score(Y_test,test_data_prediction2)
print(R2_test)

from sklearn.metrics import mean_squared_error
rms = np.sqrt(mean_squared_error(Y_test, test_data_prediction2))
print(f'Root Mean Squared Error (RMSE): {rms}')

from sklearn.ensemble import RandomForestRegressor
rf_model = RandomForestRegressor()
rf_model.fit(X_train, Y_train)

tdp=rf_model.predict(X_train)

R2_train=metrics.r2_score(Y_train,tdp)
print(R2_train)

tedp=rf_model.predict(X_test)
R2_train=metrics.r2_score(Y_test,tedp)
print(R2_train)

param_grid={'max_depth' : [100,110],
           'max_features':[2,3],
           'min_samples_leaf':[3,4,5],
           'min_samples_split':[8,10,12],
           'n_estimators':[200,300]}

RF_HY=RandomForestRegressor()

from sklearn.model_selection import GridSearchCV
grid_search=GridSearchCV(estimator=RF_HY,cv=3,param_grid=param_grid)
grid_search.fit(X_train,Y_train)

grid_search.best_params_

RF_HYP=RandomForestRegressor(max_depth= 110,
 max_features= 2,
 min_samples_leaf= 5,
 min_samples_split= 12,
 n_estimators= 200)
RF_HYP.fit(X_train,Y_train)
RF_HYP.score(X_test,Y_test)

y_pred_RF_HYP=RF_HYP.predict(X_test)

from sklearn.metrics import r2_score

print("MSE:",mean_squared_error(Y_test,y_pred_RF_HYP))
print("r squared value:",r2_score(Y_test,y_pred_RF_HYP))



import pickle
filename='trained_model.sav'
pickle.dump(rf_model,open(filename,'wb'))

loaded_model=pickle.load(open('/content/trained_model.sav','rb'))

y_pred=loaded_model.predict(X_train)
print(y_pred)