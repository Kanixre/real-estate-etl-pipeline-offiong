# import requests

# url = "https://api.rentcast.io/v1/properties"

# params = {
#     "address": "1600 Pennsylvania Ave NW",
#     "city": "Washington",
#     "state": "DC"
# }

# headers = {
#     "X-Api-Key": "2fde9f39494c48a58d93d812821c61bc"
# }

# response = requests.get(url, params=params, headers=headers)
# print(response.json())


import requests
import pandas as pd
import json
import os

# LOADS DATA FROM RENTCAST API USING UNIQUE API KEY
url = "https://api.rentcast.io/v1/properties/random?limit=100"

headers = {
    "accept": "application/json",
    "X-Api-Key": "2fde9f39494c48a58d93d812821c61bc"
}

response = requests.get(url, headers=headers)

# print(response.text)

property_data = response.json()

# CONVERT DATA FROM JSON TO DATA FRAME FOR BETTER VIEWING
df = pd.DataFrame(property_data)

df["ingested_at"] = pd.Timestamp.utcnow()

SOURCE_API = "rentcast_properties_v1"
df["source_api"] = SOURCE_API

# CONFIGURE PANDAS TO SHOW ALL ROWS & COLUMNS
pd.set_option('display.max_rows', None)      
pd.set_option('display.max_columns', None)   
pd.set_option('display.width', None)         
pd.set_option('display.max_colwidth', None)  

# CREATES AND CLEANS PRIMARY KEY??

# REMOVES DUPLICATES WITH THE PRIMARY KEY - 'id'
df = df.drop_duplicates(subset=["id"])


# DROP ROWS WITH CRITACAL MISSING DATA
df = df.dropna(subset=['id', 'formattedAddress', 'city', 'squareFootage', 'lastSalePrice'])
print(f"After drop: {len(df)} rows")


df["formattedAddress"] = df["formattedAddress"].replace(
    ["", " ", "N/A", "null", "None"],
    pd.NA
)


# DATA TYPE ENFORCEEMENT - Convert types SAFELY
df['lastSalePrice'] = pd.to_numeric(df['lastSaleDate'], errors='coerce').astype('Int64')
df['squareFootage'] = pd.to_numeric(df['squareFootage'], errors='coerce').astype('Int64')
# df['bathrooms'] = pd.to_numeric(df['bathrooms'], errors='coerce').astype('Int64')
df['bedrooms'] = pd.to_numeric(df['bedrooms'], errors='coerce').astype('Int64')
df['lotSize'] = pd.to_numeric(df['lotSize'], errors='coerce').astype('Int64')

# Parse date
df['lastSaleDate'] = pd.to_datetime(df['lastSaleDate'], errors='coerce')

# # Check missing required columns -  requires a dict of EXPECTED SCHEMA
# missing_cols = set(EXPECTED_SCHEMA) - set(df.columns)
# if missing_cols:
#     raise ValueError(f"Missing columns: {missing_cols}")



df = df[['id', 'formattedAddress', 'county', 'city', 'state', 'zipCode', 
         'propertyType', 'bedrooms', 'bathrooms', 'squareFootage', 
 'lotSize', 'yearBuilt', 'lastSaleDate', 'lastSalePrice', 'source_api', 'ingested_at']]


# df = df[['id', 'formattedAddress', 'addressLine1', 'addressLine2', 'city', 'state', 
#  'county', 'zipCode', 'propertyType', 'bedrooms', 'bathrooms', 'squareFootage', 
#  'lotSize', 'yearBuilt', 'legalDescription', 'features', 
#  'taxAssessments', 'propertyTaxes', 'ownerOccupied', 'lastSaleDate', 
#  'history', 'lastSalePrice', 'hoa']]


# 'features', 'owner', 'history'?, 'zoning'? - might be needed later on


# SHOW FULL DATA
print("="*80)
print("     FULL PROPERTY LISTINGS")
print("="*80)
print(df.to_string(index=False))  # Displays all rows properly
print("="*80)
print(f"\nTotal Listings: {len(df)}")
# print(f"Columns: {list(df.columns)}")



# print(df.duplicated().any())
# print(df[df["id"].duplicated()])

# print(df)

# OUTPUT = r"C:\Users\Owner\Documents\Amdari Projects\data\RentCastAPI_properties.csv"
# os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
# df.to_csv(OUTPUT, index=False)
# print(f"\nClean data saved → {OUTPUT}")

# id	formattedAddress	addressLine1	addressLine2	city	state	stateFips	zipCode	county	countyFips	latitude	longitude	propertyType	bedrooms	bathrooms	squareFootage	lotSize	yearBuilt	assessorID	legalDescription	zoning	lastSaleDate	lastSalePrice	features	taxAssessments	history	owner	ownerOccupied	propertyTaxes	subdivision	hoa
