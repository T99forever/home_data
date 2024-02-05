import numpy as np
import pandas as pd

df = pd.read_csv("data\\home_data.csv",
                 sep = ",")

print(df.head(n = 10), "\n", df.info(verbose = True, show_counts = True))

df_trans = df.copy()

df_trans.drop(axis = 1, columns = "id", inplace = True)

df_trans["date_clean"] = df_trans["date"].str.rstrip("0T")
df_trans["day"] = df_trans["date_clean"].astype(str).str[6:8]
df_trans["month"] = df_trans["date_clean"].astype(str).str[4:6]
df_trans["year"] = df_trans["date_clean"].astype(str).str[0:4]
df_trans["date_new"] = df_trans["year"].astype(str) + "-" + df_trans["month"].astype(str)

print(df_trans.head(n = 10), "\n", df_trans.info(verbose = True, show_counts = True))

df_trans_bedrooms = df_trans.groupby(by = "bedrooms").aggregate(["min", "max"])
df_trans_bathrooms = df_trans.groupby(by = "bathrooms").aggregate(["min", "max"])
df_trans_floors = df_trans.groupby(by = "floors").aggregate(["min", "max"])
print(df_trans_bedrooms, df_trans_bathrooms, df_trans_floors)

df_trans.loc[df_trans["bedrooms"] == 0, "bedrooms"] = -999
df_trans.loc[df_trans["bathrooms"] == 0, "bathrooms"] = -999
df_trans.replace(-999, np.nan, 
                 inplace = True)

print(df_trans.head(n = 10), "\n", df_trans.info(verbose = True, show_counts = True))

bedrooms_new_list = []
for value in df_trans["bedrooms"]:
    if value == 1:
        bedrooms_new_list.append("One")
    elif value == 2:
        bedrooms_new_list.append("Two")
    elif value == 3:
        bedrooms_new_list.append("Three")
    elif value == 4:
        bedrooms_new_list.append("Four")
    elif value == 5:
        bedrooms_new_list.append("Five or more")
    else:
        bedrooms_new_list.append(np.nan)
df_trans["bedrooms_new"] = bedrooms_new_list

bathrooms_new_list = []
for value in df_trans["bathrooms"]:
    if value < 1.5:
        bathrooms_new_list.append("One")
    elif value >= 1.5 and value < 2.5:
        bathrooms_new_list.append("Two")
    elif value >= 2.5 and value < 3.5:
        bathrooms_new_list.append("Three")
    elif value >= 3.5 and value < 4.5:
        bathrooms_new_list.append("Four")
    elif value >= 4.5:
        bathrooms_new_list.append("Five or more")
    else:
        bathrooms_new_list.append(np.nan)
df_trans["bathrooms_new"] = bathrooms_new_list

renovated_bool_list = []
for value in df_trans["yr_renovated"]:
    if value == 0:
        renovated_bool_list.append(False)
    else:
        renovated_bool_list.append(True)
df_trans["renovated_bool"] = renovated_bool_list

basement_bool_list = []
for value in df_trans["sqft_basement"]:
    if value == 0:
        basement_bool_list.append(False)
    else:
        basement_bool_list.append(True)
df_trans["basement_bool"] = basement_bool_list

df_trans.loc[df_trans["yr_renovated"] == 0, "yr_renovated"] = -999
df_trans.loc[df_trans["sqft_basement"] == 0, "sqft_basement"] = -999
df_trans.replace(-999, np.nan, 
                 inplace = True)

print(df_trans["waterfront"].unique())

df_trans.loc[df_trans["waterfront"] == 0, "waterfront"] = False
df_trans.loc[df_trans["waterfront"] == 1, "waterfront"] = True

print(df_trans.head(n = 10), "\n", df_trans.info(verbose = True, show_counts = True), "\n", df_trans.columns)

df_final = df_trans[["zipcode", "lat", "long", "date_new", "price", "floors", "bedrooms_new", "bathrooms_new", "sqft_lot", "sqft_living", "basement_bool", "sqft_basement", "sqft_above", "yr_built", "renovated_bool", "yr_renovated", "condition", "view", "waterfront", "grade"]]

df_final.columns = ["zipcode", "lat", "long", "month", "price", "floors", "bedrooms", "bathrooms", "sqft_lot", "sqft_living", "basement", "sqft_basement", "sqft_above", "yr_built", "renovated", "yr_renovated", "condition", "view", "waterfront", "grade"]

df_final.set_index(["zipcode", "lat", "long"], inplace = True)
df_final.sort_index(na_position = "last", inplace = True)

print(df_final.head(n = 10), "\n", df_final.info(verbose = True, show_counts = True), "\n", df_final.columns)

df_final.to_csv("data\\home_data_trans.csv",
                sep = ";")