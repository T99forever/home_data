import numpy as np
import pandas as pd
from plotnine import *

df = pd.read_csv("data\\home_data_trans.csv",
                 sep = ";")
print(df.head(n = 10), "\n", df.info(verbose = True, show_counts = True))
df_original = df.copy()

### TRANSFORMATION ###

df["zipcode_9800"] = df["zipcode"].astype(str).str[0:4] + "X"
df["zipcode_980"] = df["zipcode"].astype(str).str[0:3] + "XX"

df = df.set_index(["zipcode", "lat", "long"])
df = df.sort_index(na_position = "last")

print(df.head(n = 10), "\n", df.info(verbose = True, show_counts = True))

### VISUALIZATION ###
## SQFT (SCATTER) ##

df_sqft = df.copy()
df_sqft = df_sqft.query("sqft_lot < 300000 and sqft_living < 10000")

sqft_scat = ggplot(df_sqft,
                   aes(x = "sqft_lot", 
                       y = "sqft_living",
                       color = "zipcode_980")
                   ) + geom_point(
                   ) + labs (title = "Scatterplot, lot size and living room size",
                             subtitle = "Lot size and living room size by zipcodes (980XXX and 981XXX)",
                             caption = "Outliers removed for x > 300,000 and y > 10,000",
                             x = "Lot size in square feet",
                             y = "Living room size in square feet",
                             color = "Zipcode group")
print(sqft_scat)

sqft_scat2 = ggplot(df_sqft,
                    aes(x = "sqft_lot", 
                        y = "sqft_living",
                        color = "zipcode_9800")
                        ) + geom_point(
                        ) + labs(title = "Scatterplot, lot size and living room size",
                                 subtitle = "Lot size and living room size by zipcodes (9800XX through 9819XX)",
                                 caption = "Outliers removed for x >= 300,000 and y >= 10,000",
                                 x = "Lot size in square feet",
                                 y = "Living room size in square feet",
                                 color = "Zipcode group")
print(sqft_scat2)

## PRICE (BAR) ##

df_bedrooms = df.groupby(by = "bedrooms").aggregate(func = "mean", numeric_only = True)
df_bedrooms = df_bedrooms.reset_index()
df_bedrooms = df_bedrooms.sort_values(by = "price", ascending = True)
print(df_bedrooms)

bedrooms_price_bar = ggplot(df_bedrooms,
                           aes(x = "reorder(bedrooms, price)",
                               y = "price")
                               ) + geom_col(
                                   color = "red", 
                                   fill = "pink"
                                   ) + labs(
                                       title = "Average house price for amount of bedrooms",
                                       caption = "House price represents price house was sold for",
                                       x = "Number of bedrooms",
                                       y = "Average house price (in dollars)")
print(bedrooms_price_bar)

df_bathrooms = df.groupby(by = "bathrooms").aggregate(func = "mean", numeric_only = True)
df_bathrooms = df_bathrooms.reset_index()
df_bathrooms = df_bathrooms.sort_values(by = "price", ascending = True)
print(df_bathrooms)

bathrooms_price_bar = ggplot(df_bathrooms,
                           aes(x = "reorder(bathrooms, price)",
                               y = "price")
                               ) + geom_col(
                                   color = "red", 
                                   fill = "pink"
                                   ) + labs(
                                       title = "Average house price for amount of bathrooms",
                                       caption = "House price represents price house was sold for",
                                       x = "Number of bathrooms",
                                       y = "Average house price (in dollars)")
print(bathrooms_price_bar)

df_floors = df.groupby(by = "floors").aggregate(func = "mean", numeric_only = True)
df_floors = df_floors.reset_index()
df_floors = df_floors.sort_values(by = "price", ascending = True)
print(df_floors)

floors_price_bar = ggplot(df_floors,
                           aes(x = "reorder(floors, price)",
                               y = "price")
                               ) + geom_col(
                                   color = "red", 
                                   fill = "pink"
                                   ) + labs(
                                       title = "Average house price for amount of floors",
                                       caption = "House price represents price house was sold for",
                                       x = "Number of floors",
                                       y = "Average house price (in USD)")
print(floors_price_bar)

## PRICE (LINE) ##

df_date = df.groupby(by = ["zipcode_980", "month"]).aggregate(func = "mean", numeric_only = True)
df_date = df_date.reset_index()
df_date = df_date.sort_values(by = ["zipcode_980", "month"], ascending = True)
print(df_date)

date_price_col = ggplot(df_date,
                         aes(x = "month",
                             y = "price",
                             group = "zipcode_980",
                             color = "zipcode_980",
                             fill = "zipcode_980")
                             ) + geom_col(
                             ) + labs(title = "Average house price, by zipcode",
                                      subtitle = "For 2014 and 2015",
                                      caption = "House price represents price house was sold for",
                                      x = "Month",
                                      y = "Average house price (in USD; zipcodes combined for total)",
                                      color = "Zipcode group",
                                      fill = "Zipcode group")
print(date_price_col)

date_price_line = ggplot(df_date,
                         aes(x = "factor(month)",
                             y = "price",
                             group = "zipcode_980",
                             color = "zipcode_980")
                             ) + geom_line(
                             ) + labs(title = "Average house price, over 2014 and 2015",
                                      subtitle = "Grouped by zipcode",
                                      caption = "House price represents price house was sold for",
                                      x = "Month",
                                      y = "Average house price (in USD; zipcodes combined for total)",
                                      color = "Zipcode group")
print(date_price_line)

## PRICE (BOX) ##

df_price = df.copy()
df_price = df_price.query("price < 1000000")

date_price_box = ggplot(df_price,
                         aes(x = "factor(month)",
                             y = "price")
                             ) + geom_boxplot( 
                                 color = "red", 
                                 fill = "pink"
                             ) + labs(title = "Average house price by month, boxplot",
                                 caption = "Outliers removed for y >= 1,000,000; House price represents price house was sold for",
                                 y = "Average house price (in USD)"
                                 ) + scale_x_discrete(
                                name = "Month"
                                )
print(date_price_box)