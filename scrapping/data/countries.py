import requests
import snowflake.connector  
from bs4 import BeautifulSoup
import pandas as pd

#raw_results
url = 'https://www.geonames.org/countries/'

## get_results
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Scrape data
table = soup.find('table', class_="stats-table") 
#{'id': 'countries'})
#print(f"Number of table = {len(table)}")

rows = table.find_all('tr')
#print(f"Number of rows = {len(rows)}")

data = []
for row in rows:
    cols = row.find_all(['th', 'td'])
    cols = [ele.text.strip() for ele in cols]
    if cols: # Pastikan baris tidak kosong
        data.append(cols)

# Buat DataFrame (Baris pertama biasanya header)
df = pd.DataFrame(data[1:], columns=data[0])

# print(df.head(10))

# Connector snowflake
conn = snowflake.connector.connect(
    user="ibnumaulana",
    password="Ibp!2345Ibp!2345",             
    account="OZGOQZU-EF24647",  
    warehouse="COMPUTE_WH",
    database="PROJECTDB",
    schema="BRONZE",
    role="ACCOUNTADMIN",
    authenticator="snowflake"         
)

cur = conn.cursor()

world_countries = """
CREATE OR REPLACE TABLE world_countries (
    iso_alpha2 STRING,
    iso_alpha3 STRING,
    iso_numeric STRING,
    fips STRING,
    country STRING,
    capital STRING,
    area_km2 STRING,
    population STRING,
    continent STRING
);
"""

cur.execute(world_countries)

# Step 4: Insert data ke Snowflake
records = df.to_records(index=False)
data = df.values.tolist()

insert_sql = """
INSERT INTO world_countries (
    iso_alpha2, iso_alpha3, iso_numeric, fips,
    country, capital, area_km2, population, continent
) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""
cur.executemany(insert_sql, data)

conn.commit()
cur.close()
conn.close()

print("✅ Data berhasil diinsert ke Snowflake!")