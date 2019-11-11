#!/usr/bin/env python
# coding: utf-8

# # Assignment 2
# 
# ## Objective of this assignment
# The objective of this assignment is to get an understanding of the many ways data can be visualized. Upon completing this exercise you should be familiar with histograms, boxplots and scatter plots.
# 
# 
# ## ** Important: ** When handing in your homework:
# + Hand in the notebook **and nothing else** named as follows: StudentName1_snumber_StudentName2_snumber.ipynb
# + **From this week on, we will deduct a point if you zip/tar/archive the notebook, especially if you include the data folder!** 
# + Provide clear and complete answers to the questions below under a separate header (not hidden somewhere in your source code), and make sure to explain your answers / motivate your choices. Add Markdown cells where necessary.
# + Source code, output graphs, derivations, etc., should be included in the notebook.
# + Hand-in: upload to Brightspace.
# + Include name, student number, assignment (especially in filenames)!
# + When working in pairs only one of you should upload the assignment, and report the name of your partner in your filename.
# + Use the Brightspace discussion board or email the student assistants for questions on how to complete the exercises.
# + If you find mistakes/have suggestions/would like to complain about the assigment material itself, please email me [Lisa] at `l.tostrams@science.ru.nl`
# 
# 
# ## Advised Reading and Exercise Material
# **The following reading material is recommended:**
# 
# - Pang-Ning Tan, Michael Steinbach, and Vipin Kumar, *Introduction to Data Mining*, section 3.3
# - Jonathon Shlens, *A tutorial on Principal Component Analysis* , https://arxiv.org/abs/1404.1100
# 
# 
# ## 2.1 Visualizing wine data (4.5 points)
# 
# In this part of the exercise we will consider two data sets related to red and white variants of the Portuguese "Vinho Verde" wine[1]. The data has been downloaded from http://archive.ics.uci.edu/ml/datasets/Wine+Quality. Only physicochemical and sensory attributes are available, i.e., there is no data about grape types, wine brand, wine selling price, etc. The data has the following attributes:
# 
# | #   |  Attribute      | Unit |
# | --- |:--------------- |:---- |
# | 1   | Fixed acidity (tartaric) | g/dm3 |
# | 2   | Volatile acidity (acetic) | g/dm3 |
# | 3   | Citric acid | g/dm3 |
# | 4   | Residual sugar | g/dm3 |
# | 5   | Chlorides | g/dm3 |
# | 6   | Free sulfur dioxide | mg/dm3 |
# | 7   | Total sulfur dioxide | mg/dm3 |
# | 8   | Density | g/cm3 |
# | 9   | pH | pH |
# | 10  | Sulphates | g/dm3 |
# | 11  | Alcohol | % vol. |
# | 12  | Quality score | 0-10 |
# 
# Attributes 1-11 are based on physicochemical tests and attribute 12 on human judging. The data set has many observations that can be considered outliers and in order to carry out analyses it is important to remove the corrupt observations.
# 
# The aim of this exercise is to use visualization to identify outliers and remove these outliers from the data. It might be necessary to remove some outliers before other outlying observations become visible. Thus, the process of finding and removing outliers is often iterative. The wine data is stored in a MATLAB file, `Data/wine.mat`
# 
# *This exercise is based upon material kindly provided by the Cognitive System Section, DTU Compute,
# http://cogsys.compute.dtu.dk. Any sale or commercial distribution is strictly forbidden.*
# 
# > 2.1.1a) (3pts)
# 1. Load the data into Python using the `scipy.io.loadmat()` function. 
# 2. This data set contains many observations that can be considered outliers. Plot a box plot and a histogram for each attribute to visualize the outliers in the data set. Use subplotting to nicely visualize these plots.
# 3. From prior knowledge we expect volatile acidity to be around 0-2 g/dm3, density to be close to 1 g/cm3, and alcohol percentage to be somewhere between 5-20% vol. We can safely identify the outliers for these attributes, searching for the values, which are a factor of 10 greater than the largest we expect. Identify outliers for volatile acidity, density and alcohol percentage, and remove them from the data set. This means that you should remove the entire sample from the dataset, not just for that attribute!
# 4. Plot new box plots and histograms for these attributes and compare them with initial ones.
# 
# > 
#  + *You can use the `scipy.stats.zscore()` to standardize your data before you plot a boxplot.*
#  + *You can use logical indexing to easily make a new dataset (for example $X\_filtered$, where the outliers are removed. This is much easier, and faster than methods like dropping, or selecting using a for loop or list comprehension. For more information, see: https://docs.scipy.org/doc/numpy-1.13.0/user/basics.indexing.html Take a look at the -Boolean or "mask" index arrays- section.*
#  + *You can use the function `matplotlib.pyplot.subplots()` to plot several plots in one figure. A simple example an be found at: https://matplotlib.org/2.0.2/examples/pylab_examples/subplots_demo.html, take a look at the 2D subplot specifically. There is also an example of a subplot in the first assignment. If you're handy, you can devise a for loop which fills up the subplot area!* 
#  + *The object in wine.mat is a dictionary. The attributes are stored in matrix $X$. Attribute names and class names are stored in the attributeNames object, which contain arrays, of which the first element contains the names*
# 
# **Make sure to take a look at the documentation of functions before you try and use them!**
# 

# In[161]:


#Joost Verhaert
#Student number == S1047220
#from os.path import dirname, join as pjoin
import scipy.io
import matplotlib.pyplot as plt
import numpy as np

#load the data into Python
data = scipy.io.loadmat('C:/Users/Joost/Documents/Radboud/Data Mining/Assignment_2/Assignment_2/data/wine.mat')
print(data)
X = data['X']
#print(type(data_values))
#print(data_values)
#fig, axs = plt.subplots(3, 4, figsize=(20,20))
attribute = data['attributeNames'][0]

Volatile_acidity = X[:,1] <20
Density = X[:,7] < 10 
Alcohol = X[:,10] <200

fig, axes = plt.subplots(3,4, figsize=(20,20))
axes = axes.flatten()
for i in range(12):
    axes[i].boxplot(X[:,i])
    axes[i].set_title(attribute[i][0])
    
fig, axes = plt.subplots(3,4, figsize=(20,20))
axes = axes.flatten()
for i in range(12):
    axes[i].hist(X[:,i])
    axes[i].set_title(attributes[i][0])

fixed_data = X[Volatile_acidity & Density & Alcohol]

fig, axes = plt.subplots(3,4, figsize=(20,20))
axes = axes.flatten()
for i in range(12):
    axes[i].boxplot(fixed_data[:,i])
    axes[i].set_title(attribute[i][0])
    
fig, axes = plt.subplots(3,4, figsize=(20,20))
axes = axes.flatten()
for i in range(12):
    axes[i].hist(fixed_data[:,i])
    axes[i].set_title(attributes[i][0])

plt.show()
#filtered = X[volatile_acidity & density & alcohol_volume]
#x = 0
#for i in range(len(data_values[1])):
#    if i%4 == 0:
#        x = 0
#    axs[int(i/4), x].boxplot(X[i+1],0, 'gD')
#    axs[int(i/4), x].set_title(attribute[i][0])
#    x += 1

#x = 0
#for i in range(len(data_values[1])):
#    if i%4 == 0:
#        x = 0
#    axs[int(i/4), x].hist(X[i+1],0)
#    axs[int(i/4), x].set_title(attribute[i][0])
#    x += 1
    


# ----
# 
# 
# ----

# > 2.1.1b (0.5pts)
# Why do we need to standardize the data after removing the outliers? Give the -statistical- reason, not just the practical reason. 

# ----
# The calculated information including the outliers can diverse strongly with respect to the "real" data. When the outliers are removed the calculated information beforehand is not relevant to the real data. For instance, the mean and standard deviation can be very different from what it was before.
# 
# ----

# > 2.1.2 (1pt) Make scatter plots between attributes and wine quality as rated by human judges. Can you manually identify any clear relationship between the attributes of the wine and wine quality? Which values of these attributes are associated with high quality wine? Use the correlation coefficients to substantiate your answers. Make sure to use the data where the outliers are removed 
# + *You can calculate the correlation coefficient using the `scipy.stats.pearsonr()` function to measure the strength of association.*

# In[207]:


#print(X)
#print(attribute)
#print(X[:,1])
import scipy.stats
from scipy.stats import pearsonr

fig, axes = plt.subplots(3,4, figsize=(20,20))
axes = axes.flatten()
list_correlation = []
for i in range(11):
    axes[i].scatter(fixed_data[:,i],fixed_data[:,11])
    axes[i].set_title(attribute[i][0])
    list_correlation.append(scipy.stats.pearsonr(fixed_data[:,i],fixed_data[:,11]))
    print(attribute[i][0], scipy.stats.pearsonr(fixed_data[:,i],fixed_data[:,11]))
list_max = []
list_min = []
for k in list_correlation:
    list_max.append(k[0])
    list_min.append(k[0])
print(max(list_max))
print(min(list_min))


# ----
# Looking at these scatter plots and the values of the correlation and p-value. You are able to see that the correlation is very small with the density regard the wine score. On the other hand, alcohol has a strong correlation. The variable Chlorides is has strong influences with the amount getting higher. The lower the value the higher the wine will be rated positively.
# 
# ----

# ## 2.2 Visualizing the handwritten digits (4 points)
# 
# In this part of the exercise we will analyse the famous *mnist* handwritten digit dataset from: http://yann.lecun.com/exdb/mnist/.
# 
# > 2.2.1 (4pts)
# 1. Load zipdata.mat by using the loadmat function. There are two data sets containing handwritten digits: *testdata* and *traindata*. Here, we will only use *traindata*. The first column in the matrix *traindata* contains the digit (class) and the last 256 columns contain the pixel values.
# 2. Create the data matrix *X* and the class index vector *y* from the data. Remove
# the digits with the class index 2-9 from the data, so only digits belonging to
# the class 0 and 1 are analyzed. (remember logical indexing!) 
# 3. Visualize the first 10 digits as images. (take a look at the example code)
# Next, compute the principal components (PCA) of the data matrix. Now, using the PCA model, create a new data matrix $Z$ by projecting $X$ onto the space spanned by the loadings $V$. The new data matrix should have 4 attributes corresponding to PC1-PC4.  Use subplotting to show the digits and their reconstructed counterparts in an orderly manner.
# 4. Reconstruct the initial data using PC1-PC4 into a new matrix called $W$. Visualize the first 10 digits as images for the reconstructed data and compare them with images for the original data.
# 5. Make a 4-by-4 subplot of scatter plots of each possible combination projection onto PC1 to PC4 (contained in $Z$) against each other. You can leave the diagonal blank.  Plot elements belonging to different classes in different colors. Add a legend to clarify which digit is shown in which color.
# 6. Make a 3-dimensional scatter plot of the projections onto the first three principal components PC1-PC3 (contained in $Z$). Plot elements belonging to different classes in different colors. Add a legend to clarify which digit is shown in which color.
# 7. What can you conclude from the various scatterplots about the PCs and the way they separate the data?
# 
# > **Hints:**
# + *The below example code can help you visualize digits as images.*
# + *See Assignment 1 if you can not recall how to compute a PCA.*
# + *Keep in mind that numpy.linalg.svd() returns the transposed **V<sup>T</sup>** matrix as output.*
# + *You can use **Z** = **Y** $*$ **V**[:,:4] to project the data onto the first four PCs. Don't forget that the $*$ operator does not perform matrix multiplication for numpy arrays!*
# + *To reconstruct the data from projection you can use the following formula: **W** = **Z**&ast;**V**[:,:4]<sup>T</sup> + **μ**. *
# + *You can take a look at the example_figure.ipynb notebook to see how you can easily plot multiple classes and color them correspondingly.* 
# + *It is advisable to make a for-loop to generate the 2D scatter plots, this saves a lot of time. It is an important skill to master if you want to easily modify your work later on, for example when correcting mistakes, or when you want to modify each plot in the same manner.* 
# 

# In[308]:


## Example code:
#------------------------------------------------
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from scipy.io import loadmat
from numpy import reshape

# Index of the digit to display
i = 0

# Load Matlab data file to python dict structure
mat_data = loadmat('C:/Users/Joost/Documents/Radboud/Data Mining/Assignment_2/Assignment_2/Data/zipdata.mat')

# Extract variables of interest
testdata = mat_data['testdata']
traindata = mat_data['traindata']
X = traindata[:,1:]
y = traindata[:,0]
values = traindata[:,0] <2
fixed_data = X[values]
X = X[values]
fig = plt.figure(figsize=(10,10))
for i in range(10):
    plt.subplot(5,2,i+1);
    I = reshape(fixed_data[i,0:],(16,16)) #y[i,:]
    plt.imshow(I, extent=(0,16,0,16), cmap=cm.gray_r);
plt.title('Digit as an image');
plt.show()

mu = fixed_data.mean(axis=1)

fixed_data_transposed = np.transpose(np.transpose(fixed_data) - mu)
print(fixed_data_transposed, fixed_data_transposed.shape)

U, S, Vt= np.linalg.svd(fixed_data_transposed)
V = np.transpose(Vt)
print(U.shape)
print(S.shape)
print(Vt.shape)
print(V.shape)
#print(Y.shape)

Z = np.dot(fixed_data,V[:,:4])
#Z.shape

fig = plt.figure(figsize=(10, 10))
for i in range(10):
    plt.subplot(5,2,i+1);
    I = reshape(Z[i,0:],(2,2)) #y[i,:]
    plt.imshow(I, extent=(0,16,0,16), cmap=cm.gray_r);

W_2 = np.transpose(np.dot(Z, V[:,:4].transpose()))
W = np.transpose(W_2+mu)

fig = plt.figure(figsize=(10, 10))
for i in range(10):
    plt.subplot(5,2,i+1);
    I = reshape(W[i,0:],(16,16)) #y[i,:]
    plt.imshow(I, extent=(0,16,0,16), cmap=cm.gray_r);
print(Z)
print(len(Z))

Traindata = np.array(mat_data['traindata'])
SelectZerosOnes = Traindata[:,0] < 2
y = Traindata[SelectZerosOnes, 0]

fig, axes = plt.subplots(4,4, figsize=(20,20))
#plt.scatter(Z[:,0],Z[:,3], c=y)
#colormap = np.array(['r', 'g'])
colors = itertools.cycle(["r", "b"])
#plt.style.use('seaborn-whitegrid')
for i in range(4):
    for k in range(4):
        axes[i,k].scatter(Z[:,i],Z[:,k], c = y)
        

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
#colormap = np.array(['r', 'g'])

ax = Axes3D(fig, rect=[0, 0, .75, .75], elev=45, azim=135)
plt.scatter(Z[:,0],Z[:,1], Z[:,2], y)

ax.set_xlabel('PC1')
ax.set_ylabel('PC2')
ax.set_zlabel('PC3')
plt.show()

#I WAS NOT ABLE TO FIX THE COLORS TO REAL COLORS AS RED AND GREEN. I REALLY WOULD LIKE TO KNOW HOW TO DO THIS. 

# Visualize the i'th digit as an image
#plt.subplot(1,1,1);

#fig, axes = plt.subplots(5,2, figsize=(10,10))
#axes = axes.flatten()
#for i in range(12):
#    axes[i].boxplot(X[:,i])
#    axes[i].set_title(attribute[i][0])
    
#for k in range(10):
#    I = reshape(fixed_data[k,:],(16,16))
#    plt.imshow(I, extent=(0,16,0,16), cmap=cm.gray_r);
#plt.title('Digit as an image');
#plt.show()
#------------------------------------------------


# ----
# The PC1 and the PC2 are on a diagonal line. PC3 is divided strongly with regard to the other PC's (PC1 & PC2).
# PC3 is therefore indepedent and PC1 & PC2 are dependent on each other.
# 
# ----
# 
# 

# ## 2.3 Probability and Statistics (1.5 points)
# The aim of this exercise is to learn how to calculate basic statistics in python.
# > 2.3.1 (0.3pts) A study of a very limited population of Aliens reveals the following number of body appendages (limbs):
# <center>2,3,6,8,11,18</center>
# i. Find the mean $m$ and the standard deviation $\sigma$ of this population.
# + *You can use the methods numpy.ndarray.mean() and numpy.ndarray.std() to calculate the mean and standard deviation.*

# In[181]:


import statistics
import numpy as np
list_variabels = [2,3,6,8,11,18]
print("The mean using python statistics is: ", statistics.mean(list_variabels))
print("The mean using numpy is: ", np.mean(list_variabels))
print("The standarddeviation is: ", np.std(list_variabels))


# > ii. (0.3pts) List all possible samples of two aliens without replacement, and find each mean. Do the same with samples of four aliens.
# + *You can use the method itertools.combinations(v,n) to find all possible samples of a vector v taking n elements at a time.*

# In[201]:


import itertools
#lijst = ['a','b','c','d']
#import itertools.combinations
sample1 = list(itertools.combinations(list_variabels,2))
sample2 = list(itertools.combinations(list_variabels,4))
sample1_means = []
sample2_means = []
for i in range(len(sample1)):
    print(sample1[i])
    sample1_means.append(np.mean(sample1[i]))
    #print(np.mean(sample1[i]))
#print(list(itertools.combinations(list_variabels,2)))
for i in range(len(sample2)):
    print(sample2[i])
    sample2_means.append(np.mean(sample2[i]))
    #print(np.mean(sample2[i]))
#print(list(itertools.combinations(list_variabels,4)))
print("means of two aliens: ", sample1_means)
print("means of four aliens: ", sample2_means)


# > iii. (0.3pts) Each of the means above is called a sample mean. Find the mean of all the sample means (denoted by $m_x$) and the standard
# deviation of all the sample means (denoted by $\sigma_x$) for both
# the *N=2* and *N=4* samples.

# In[205]:


print("Mean of the sample means with two alien: ", np.mean(sample1_means))
print("The standard deviation of the sample means with two alien: ", np.std(sample1_means))
print("Mean of the sample means with four alien: ", np.mean(sample2_means))
print("The standard deviation of the sample means with fout alien: ", np.std(sample2_means))


# > iv. Verify the Central Limit Theorem: (i) (0.1pts) compare the population
# mean with the mean of both sample means; (ii) (0.2pts) compare the population
# standard deviation divided by the square root of the sample size
# with the standard deviation of both sample means (i.e., does
# $\sigma_x \approx \sigma/\sqrt{N}$). BTW, a better approximation for
# small population sizes is $\sigma_x = \sigma / \sqrt{N} \times
# \sqrt{(M-N)/(M-1)}$ with *M = 6* the size of the original

# ----
# 
# 
# ----

# > v. (0.3pts) Plot the distribution of the population and the distributions of both sample means using histograms. What happens to the shape of the sample means distribution as the sample size (N*) increases?

# In[224]:


import seaborn as sns
sns.distplot(list_variabels)
lijst = [sample1_means, sample2_means]
lijst2 = ["sample1_means", "sample2_means"]
fig, axes = plt.subplots(1,1, figsize=(5,5))
sns.distplot(lijst[0])
fig, axes = plt.subplots(1,1, figsize=(5,5))
sns.distplot(lijst[1])
print("When the N size increases the mean grows")


# ----
# 
# 
# ----
