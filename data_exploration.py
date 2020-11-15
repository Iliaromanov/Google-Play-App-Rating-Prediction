import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

def missing_values(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent_1 = df.isnull().sum()/df.isnull().count()*100
    percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
    missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
    return missing_data.head((missing_data['Total'] > 0).sum())

train = pd.read_csv("googleplaystore.csv")
# The weird column with missed data
mixed = train.loc[10472]
train = train.drop(10472, axis = 0)

#Create x and y dfs
train_y = train["Rating"]
columns_drop = ["Rating", "App"]


train_x = train.drop(columns_drop, axis = 1)

#Count unique values in App and see that there are duplicates
unique_apps = train["App"].nunique()
all_apps = train["App"].size

#Check missing values
missing_values(train)

#convert Installs to numeric
train_x["Installs"] =  pd.to_numeric((train_x["Installs"].str.replace("+", "")).str.replace(",", ""))

#See all unique values in the Android version column
train_x["Android Ver"].unique()
# Note that most are num and up. Hence, we can split the column into 3 by space

#Take the first part of the android version
train_x["Android Ver"] = train["Android Ver"].str.split(expand = True)

# There are 3 values in type column: free, paid and nan. There is only 1 nan so I looked at it and
# since the price is set to 0, I will put free for that cell
train_x["Type"][9148] = "Free"

# Change price column to free = 0 and paid = 1
paid_types = train_x["Type"].unique()

# creating instance of labelencoder
labelencoder = LabelEncoder()
train_x['Type'] = labelencoder.fit_transform(train_x['Type'])

# Select numeric columns that can be converted as is
num_cols = ["Reviews"]

train_x["Type"] = train_x[num_cols].astype(float)




