# -*- coding: utf-8 -*-
"""K-Means_Clustering 2nd Example

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/18D_A0-8U_u8gepy437roiQy6y-DmgffN
"""

from google.colab import drive
drive.mount('/content/drive/')

cd 'drive/My Drive/Colab Notebooks'

# Commented out IPython magic to ensure Python compatibility.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

dataset =pd.read_csv('Mall-Customer-Segmentation-Dataset.csv')

dataset.head()

dataset.rename(columns ={'Annual Income (k$)' : 'A_Income', 'Spending Score (1-100)' : 'Spending_Score'}, inplace =True)

dataset.head()

dataset.describe()

sns.pairplot(dataset[['Age','A_Income','Spending_Score']])

import sklearn.cluster as cluster
kmeans =cluster.KMeans(n_clusters =5, init ="k-means++")
kmeans =kmeans.fit(dataset[['Spending_Score', 'A_Income']])

kmeans.cluster_centers_

dataset['Clusters']= kmeans.labels_
dataset.head()

dataset['Clusters'].value_counts()

sns.scatterplot(x ='Spending_Score', y ='A_Income', hue ='Clusters', data =dataset )