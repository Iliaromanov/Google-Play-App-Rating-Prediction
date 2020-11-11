import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder

app_data = pd.read_csv('googleplaystore.csv')


def missing_values(df):
    total = df.isnull().sum().sort_values(ascending=False)
    percent_1 = df.isnull().sum()/df.isnull().count()*100
    percent_2 = (round(percent_1, 1)).sort_values(ascending=False)
    missing_data = pd.concat([total, percent_2], axis=1, keys=['Total', '%'])
    return missing_data.head((missing_data['Total'] > 0).sum())


# Display the amount of missing values per column
# and what percentage of the column contains missing values
missing_values(app_data)


# Removing rows with missing rating 
# I don't think I did anything with this line -Ilia
app_data = app_data[app_data.Rating.notnull()]


# Count unique values in App and see that there are duplicates
unique_apps = app_data["App"].nunique()
all_apps = app_data["App"].size

f"total app count: {all_apps}, unique app count: {unique_apps}"


# Removing duplicate apps
app_data = app_data.drop_duplicates(subset = "App")

new_all_apps = app_data["App"].size
f"total app count after dropping duplicates: {new_all_apps}"


# Create df for Rating
# the y df
app_data_y = app_data["Rating"]

# Create df for the Rest of the features
# the x df
columns_drop = ["Rating", "App"]
app_data_x = app_data.drop(columns_drop, axis = 1)

#See all unique values in the Android version column
app_data_x["Android Ver"].unique()
# Note that most are num and up. Hence, we can split the column into 3 by space

#Take the first part of the android version
app_data_x["Android Ver"] = app_data["Android Ver"].str.split(expand = True)

# There are 3 values in type column: free, paid and nan. There is only 1 nan so I looked at it and
# since the price is set to 0, I will put free for that cell
app_data_x["Type"][9148] = "Free"

# Change price column to free = 0 and paid = 1
paid_types = app_data_x["Type"].unique()

# creating instance of labelencoder
labelencoder = LabelEncoder()
app_data_x['Type'] = labelencoder.fit_transform(app_data_x['Type'])

