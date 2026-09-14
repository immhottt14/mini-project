import requests
import snowflake.connector  
from bs4 import BeautifulSoup
import pandas as pd

#raw_results

url = 'https://www.scrapethissite.com/pages/simple/'

## get_results
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

country_blocks = soup.find_all("div", class_="col-md-4 country")
print(f"Number of countries = {len(country_blocks)}")

## get loop results
results = []
for block in country_blocks:
    name = block.find("h3", class_="country-name").text.strip()
    capital = block.find("span", class_="country-capital").text.strip()
    population = block.find("span", class_="country-population").text.strip()
    area = block.find("span", class_="country-area").text.strip()
    results.append({"name" : name, "capital" : capital, "population" : population, "area" : area}) 

# Simpan ke resultsFrame
df = pd.DataFrame(results)
print(df)

# Connector snowflake
conn = snowflake.connector.connect(
    user="LAMHOTPT",
    password="P@ssvv0rdP@ssvv0rd!!",             
    account="FCHSPXS-RP17491",  
    warehouse="COMPUTE_WH",
    database="DATAWAREHOUSE",
    schema="RAW",
    role="ACCOUNTADMIN",
    authenticator="snowflake"         
)

cur = conn.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS raw_countries (
    uid STRING DEFAULT UUID_STRING(),
    name VARCHAR(50),
    capital VARCHAR(50),
    population VARCHAR(50),
    area VARCHAR(50)
    )
""")


for block in results:
    cur.execute("INSERT INTO raw_countries (name, capital, population, area) VALUES (%s, %s, %s, %s)",
        (block["name"], block["capital"], block["population"], block["area"])
    )

conn.commit()
cur.close()
conn.close()

