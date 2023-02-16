# -*- coding: utf-8 -*-
"""better.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Bk-ZYXG0Da3cLbWawhu0K8gjnfKxNdB4
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import math 

from google.colab import drive
drive.mount('/content/drive/')

cd 'drive/My Drive/Colab Notebooks'

#Describe
mortality = pd.read_csv('FINAL_DATASET.csv')
X = mortality
#X = mortality.drop(columns = ['DateModified', 'Adult mortality rate', 'Unnamed: 0'], axis = 1)
y = mortality['Adult mortality rate']
y = y.values
y = np.around(y)
y = y.astype(int)
y = pd.DataFrame(y, columns = ['Adult mortality rate'])

pl = X[['ParentLocation', 'Adult mortality rate']]
l = X[['Location', 'Adult mortality rate']]
s = X[['Location','Sex', 'Adult mortality rate']]
l.groupby(['Location']).mean().sort_values('Adult mortality rate')
pl.groupby(['ParentLocation']).mean().sort_values('Adult mortality rate')
s.groupby(['Location','Sex']).mean().sort_values('Adult mortality rate')

mortality

#Describe
X['ParentLocation'].unique()
newloc = X['Location'].unique()
newloc.sort()

#Dictionary for mapping of Parent Location
Ploc = {
    'Eastern Mediterranean' : 0,
    'Africa' : 1,
    'Europe': 2, 
    'Western Pacific' : 3,
    'Americas' : 4, 
    'South-East Asia' : 5
}

#Mapping Parent Location
X['ParentLocation'] = X['ParentLocation'].map(Ploc)

# Mapping for Sex 
SexM = {
    'Male': 0,
    'Female': 1
}
X['Sex'] = X['Sex'].map(SexM)

X['Location'].unique()

#Describe
#Get the sorted Location for Mapping 
pd.options.mode.chained_assignment = None 
bX= X.sort_values(['Location']) #Sorted Location Ascending 

#Dictionary for Location but has brackets 
trial = dict()
for i in range(len(bX['Location'].unique())):
    # here define what key is, for example,
    key = bX['Location'].unique()[i]
    # check if key is already present in dict
    if key not in trial:
        trial[key] = []
    # append some value 
    trial[key].append(i)
  
X['Location'] = bX['Location'].map(trial) #Mapping Location

newest = [i[0] for i in X['Location']]#removes brackets from location
X['Location'] = newest
trial



# MAKES THE Y AS HIGH OR LOW 
# changing elements of array
# def amr_category(num):
#   if(num > 306):
#     num = "HIGH"
#     return num
#   elif(num <= 306 and num >= 194):
#     num = "MODERATE"
#     return num
#   elif(num < 194):
#     num = "LOW"
#     return num

# y = y.apply(lambda x: amr_category(x))

X

y

# main = pd.concat([X,y],axis=1)
# main.head()



X

#Calculation
def get_prev_mean(x,df):
  year = int(x['Period'])-1
  location = x['Location']
  #print(year,location,df.query(f"Period == '{year}' and Location == '{location}'").shape)
  prev_mean = df.query(f"Period == {year} and Location == {location}")['Adult mortality rate'].mean()
  if str(prev_mean) != 'nan':
    return prev_mean
  else:
    prev_mean = df.query(f"Location == {location}")['Adult mortality rate'].mean()
    return 0
    #return prev_mean

X['prev_mean'] = X.apply(lambda x: get_prev_mean(x,X),axis=1)
X.head(6000)

X

import pandas as pd
from scipy.stats import pearsonr

corr1, _ = pearsonr(X['ParentLocation'], X['Adult mortality rate'])
corr2, _ = pearsonr(X['Location'], X['Adult mortality rate'])
corr3, _ = pearsonr(X['Period'], X['Adult mortality rate'])
corr4, _ = pearsonr(X['Sex'], X['Adult mortality rate'])
#corr5, _ = pearsonr(X['prev_mean'], X['Adult mortality rate'])
print('Parent Location Pearsons correlation: %.3f' % corr1)
print('Location Pearsons correlation: %.3f' % corr2)
print('Period Pearsons correlation: %.3f' % corr3)
print('Sex Pearsons correlation: %.3f' % corr4)
#print('prev_mean Pearsons correlation: %.3f' % corr5)

X.head(6000)

#OPTIONAL
#Calculation
def get_ls_mean(x,df):
  location = x['Location']
  sex = x['Sex']
  ls_mean = df.query(f"Location == {location} and Sex == {sex}")['Adult mortality rate'].mean()
  if str(ls_mean) != 'nan':
    return ls_mean
  else:
    ls_mean = df.query(f"ParentLocation == {location} and Sex == {sex}")['Adult mortality rate'].mean()
    return 0

#X['ls_mean'] = X.apply(lambda x: get_ls_mean(x,X),axis=1)

#X.groupby(['Location'])['prev_mean'].mean()

#x_mean = X.groupby(['Location'])['prev_mean'].mean()
#X['prev_mean'] = X['prev_mean'].fillna(x_mean)

#X['prev_mean'] = X['prev_mean'].replace(np.nan, X.groupby(['Location'])['prev_mean'].mean().values)

X.head(6000)

#Calculation
#Splits by Period 

train = X.query("Period < 2010")
test = X.query("Period >= 2010 and Period < 2014")
validation = X.query("Period >= 2014")
train['Period'].unique()
X.shape
print(train.shape)
print(test.shape)
print(validation.shape)

#Calculation
X = X.drop(columns = ['Period', 'Adult mortality rate'], axis = 1)


x_train = train.drop(columns = ['Period', 'DateModified', 'Adult mortality rate', 'Unnamed: 0'])
y_train = train['Adult mortality rate']

x_test = test.drop(columns = ['Period', 'DateModified', 'Adult mortality rate', 'Unnamed: 0'])
y_test = test['Adult mortality rate']

x_val = validation.drop(columns = ['Period', 'DateModified', 'Adult mortality rate', 'Unnamed: 0'])
y_val = validation['Adult mortality rate']

x_train

# #Create a function with many machine learning models
# def models(X_train, Y_train):
  
#   from sklearn.linear_model import LogisticRegression
#   log = LogisticRegression(random_state =0)
#   log = LogisticRegression(solver='lbfgs', max_iter=100) # 
#   log.fit(X_train, Y_train)

#   #Use Neighbors
#   from sklearn.neighbors import KNeighborsClassifier
#   knn = KNeighborsClassifier(n_neighbors =5, metric = 'minkowski', p=2)
#   knn.fit(X_train, Y_train)

#   #Use SVC (linear kernel)
#   from sklearn.svm import SVC
#   svc_lin = SVC(kernel ='linear', random_state =0)
#   svc_lin.fit(X_train, Y_train)

#   #Use SVC (RBF kernel)
#   from sklearn.svm import SVC
#   svc_rbf = SVC(kernel ='rbf', random_state =0)
#   svc_rbf.fit(X_train, Y_train)

#   #Use GaussianNB
#   from sklearn.naive_bayes import GaussianNB
#   gauss = GaussianNB()
#   gauss.fit(X_train, Y_train)

#   #Use Desicion Tree
#   from sklearn.tree import DecisionTreeClassifier
#   tree = DecisionTreeClassifier(criterion ='entropy', random_state=0)
#   tree.fit(X_train, Y_train)

#   #Use RandomForest Classifier
#   from sklearn.ensemble import RandomForestClassifier
#   forest = RandomForestClassifier(n_estimators =10, criterion = 'entropy', random_state =0)
#   forest.fit(X_train, Y_train)

#   #Print the training accuracy for each model
#   print("[0]Logistic Regression Training Accuracy: ", log.score(X_train, Y_train))
#   print("[1]K Neighbors Training Accuracy: ", knn.score(X_train, Y_train))
#   print("[2]SVC Linear Training Accuracy: ", svc_lin.score(X_train, Y_train))
#   print("[3]SVC RBF Training Accuracy: ", svc_rbf.score(X_train, Y_train))
#   print("[4]Gaussian NB Training Accuracy: ", gauss.score(X_train, Y_train))
#   print("[5]Decision Tree Training Accuracy: ", tree.score(X_train, Y_train))
#   print("[6]Random Forest Training Accuracy: ", forest.score(X_train, Y_train))

#   #return log, knn, svc_lin, svc_rbf, gauss, tree, forest
#   return knn, svc_lin, svc_rbf, gauss, tree, forest

#CALCULATION
#Create a function with many machine learning models
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

import math

def models(X_train, Y_train, X_test, Y_test, X_val, Y_val):
  
  from sklearn.linear_model import LinearRegression
  lr = LinearRegression()
  lr.fit(X_train, Y_train)
  #Print the training accuracy for each model

  y_test_pred = lr.predict(X_test)
  lr_rmse_test = math.sqrt(mean_squared_error(Y_test, y_test_pred))
  
  y_val_pred = lr.predict(X_val)
  lr_val_rmse_test = math.sqrt(mean_squared_error(Y_val, y_val_pred))
  lr_test_score = r2_score(Y_test, y_test_pred)
  lr_val_score = r2_score(Y_val, y_val_pred)


  from sklearn.ensemble import RandomForestRegressor
  from sklearn.datasets import make_regression
  regr = RandomForestRegressor(max_depth=6, random_state=0, min_samples_leaf = 2)
  print(X_train.shape)
  regr.fit(X_train, Y_train)

  fr_y_pred = regr.predict(X_test)
  fr_test_rmse_test = math.sqrt(mean_squared_error(Y_test, fr_y_pred))


  fr_y_val = regr.predict(X_val)
  fr_val_rmse_test = math.sqrt(mean_squared_error(Y_val, fr_y_val))
  val_score = regr.score(X_val, Y_val)

  val_score = r2_score(Y_val,fr_y_val)
  test_score = r2_score(Y_test,fr_y_pred)

  #Linear Regression
  print("Linear Regression")
  print("Model Prediction: ",lr_rmse_test, lr_test_score)
  print("Validation: ",lr_val_rmse_test, lr_val_score)

  print("Random Forest")
  print("Model Prediction: ",fr_test_rmse_test, test_score)
  print("Validation: ",fr_val_rmse_test,val_score)

  #Generalized Linear Regression

  #return log, knn, svc_lin, svc_rbf, gauss, tree, forest
  #return lr

train

x_train

#Calculation
model = models(x_train, y_train, x_test, y_test, x_val, y_val)



#CALCULATION
#Show the confusion matrix and accury for all models
from sklearn.metrics import confusion_matrix

for i in range (len(model)):
  cm = confusion_matrix(Y_test, model[i].predict(X_test))

  #Extract TN, FP, FN, TP
  TN, FP, FN, TP = cm.ravel()
  test_score = (TP + TN) / (TP + TN + FN + FP)
  print(cm)
  print('Model[{}] Testing Accuracy = "{}"'.format(i, test_score ))
  print()

z = mortality.drop(columns = ['DateModified', 'Unnamed: 0'], axis = 1)

africa2016 = z[['ParentLocation','Period', 'Sex', ['Adult mortality rate'].mean()]][((z["ParentLocation"] == 'Africa') ]]