"""
ETL script for Home.LLC Data Engineer Assessment.
Reads property CSV and config, normalizes data, and loads into MySQL.
"""


import pandas as pd
import mysql.connector
from datetime import datetime


# 1. Read the raw file
df = pd.read_csv('sql/fake_data.csv')

# 2. Normalize addresses
# Normalize addresses and rename to match DB schema
df_addresses = df[['Street_Address', 'City', 'State', 'Zip']].drop_duplicates().reset_index(drop=True)
df_addresses['country'] = 'USA'
df_addresses['address_id'] = df_addresses.index + 1
df_addresses = df_addresses.rename(columns={
    'Street_Address': 'street',
    'City': 'city',
    'State': 'state',
    'Zip': 'zip'
})[['address_id', 'street', 'city', 'state', 'zip', 'country']]

print("Sample addresses:")
print(df_addresses.head())

# 3. Normalize financials

df_financials = df[['List_Price', 'Taxes', 'Net_Yield', 'IRR']].drop_duplicates().reset_index(drop=True)
df_financials['financial_id'] = df_financials.index + 1
df_financials = df_financials.rename(columns={
    'List_Price': 'list_price',
    'Taxes': 'taxes',
    'Net_Yield': 'net_yield',
    'IRR': 'irr'
})[['financial_id', 'list_price', 'taxes', 'net_yield', 'irr']]


print("Sample financials:")
print(df_financials.head())


# 4. Merge address_id and financial_id back into main dataframe
merged = df.merge(df_addresses, left_on=['Street_Address', 'City', 'State', 'Zip'],
                                right_on=['street', 'city', 'state', 'zip'])
merged = merged.merge(df_financials, left_on=['List_Price', 'Taxes', 'Net_Yield', 'IRR'],
                                    right_on=['list_price', 'taxes', 'net_yield', 'irr'])





# 5. Build properties table
df_properties = merged[['Property_Title', 'address_id', 'financial_id']].copy()
df_properties['purchase_date'] = datetime.today().strftime('%Y-%m-%d')
df_properties['property_id'] = df_properties.index + 1

print("Sample properties:")
print(df_properties.head())



# 6. Create features table
df_features = merged[['Bed', 'Bath', 'SQFT_Total', 'BasementYesNo']].copy()
df_features['property_id'] = df_properties['property_id']

# Optional: turn 'Yes'/'No' into binary
df_features['has_basement'] = df_features['BasementYesNo'].map({'Yes': 1, 'No': 0}).fillna(0).astype(int)

df_features = df_features.rename(columns={
    'Bed': 'bedrooms',
    'Bath': 'bathrooms',
    'SQFT_Total': 'sqft'
})[['property_id', 'bedrooms', 'bathrooms', 'sqft', 'has_basement']]

df_features['feature_id'] = df_features.index + 1

print("Sample features:")
print(df_features.head())



# 7. Connect to MySQL
db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': '6equj5_root',
    'database': 'home_db'
}

conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()

# Clear previous data before re-insert (dev safe)
cursor.execute("DELETE FROM features")
cursor.execute("DELETE FROM properties")
cursor.execute("DELETE FROM financials")
cursor.execute("DELETE FROM addresses")
conn.commit()


def insert_df(df, table_name, columns):
    placeholders = ', '.join(['%s'] * len(columns))
    col_names = ', '.join(columns)
    sql = f"INSERT INTO {table_name} ({col_names}) VALUES ({placeholders})"
    for row in df[columns].itertuples(index=False, name=None):
        cursor.execute(sql, row)
    conn.commit()


# 8. Load tables in correct dependency order
insert_df(df_addresses, 'addresses', ['address_id', 'street', 'city', 'state', 'zip', 'country'])
insert_df(df_financials, 'financials', ['financial_id', 'list_price', 'taxes', 'net_yield', 'irr'])
insert_df(df_properties, 'properties', ['property_id', 'address_id', 'financial_id', 'Property_Title', 'purchase_date'])
insert_df(df_features, 'features', ['feature_id', 'property_id', 'bedrooms', 'bathrooms', 'sqft', 'has_basement'])


cursor.close()
conn.close()
print("✅ ETL completed and data loaded into MySQL.")
