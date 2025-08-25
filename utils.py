from loader import loader
import json
import pandas as pd

df = loader.load_json('./data/Retail_Clean_Data.json')

monthly_revenue = df.groupby("Month")['Revenue'].sum().sort_index() # Level 1 Variabels
country_revenue = df.groupby('Country')['Revenue'].sum().sort_values(ascending=False).head(10) # Level 2 measures
monthly_quantity = df.groupby('Month')['Quantity'].sum().sort_index() # level2
df_quantity = df[(df['Quantity']>0) & (df['Quantity'] < 100)] #level 2
top_countries_by_revenue = df.groupby('Country')['Revenue'].sum().sort_values().head(5)  # level 3

# group bar chart level 3
top_countries = df['Country'].value_counts().head(5).index.tolist()
df_top = df[df['Country'].isin(top_countries)].copy()
grouped = df_top.groupby(['Country','Month'])['Revenue'].sum().reset_index()
grouped['Month'] = pd.to_datetime(grouped['Month'])
grouped = grouped.sort_values('Month')
grouped['Month'] = grouped['Month'].dt.strftime('%Y-%m')

# heatmap level 3
labels = ['Quantity', 'Price', 'Revenue']
corr_matrix = df[labels].corr()



with open("./data/data.json",'r') as file:
            data = json.load(file)