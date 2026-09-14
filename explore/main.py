import snowflake.connector
import requests
from bs4 import BeautifulSoup


# get data countries
response = requests.get('https://www.scrapethissite.com/pages/simple/') # get data scrap website
soup = BeautifulSoup(response.text, "html.parser")

country_blocks = soup.find_all("div", class_="col-md-4 country")
print(f"Number of countries = {len(country_blocks)}")

result = []
for block in country_blocks:
    name_element = block.find("h3", class_="country-name")
    country_name = name_element.get_text(strip=True)

    name_element = block.find("span", class_="country-capital")
    capital_name = name_element.get_text(strip=True)

    name_element = block.find("span", class_="country-population")
    population_name = name_element.get_text(strip=True)

    result.append({"country_name" : country_name, "capital_name" : capital_name, "population" : population_name})

#  get data products

base_url =  'https://www.scrapingcourse.com/ecommerce/page/{}/'
page = 1
data = []

while True:
    # url = f"{base_url}?page={page}"
    url = base_url.format(page)
    print(f"Fetching Page {url}...")

    response = requests.get(url)
    if response.status_code !=200:
        print(f"Failed to retrieve page {page}")
        break

    soup = BeautifulSoup(response.text, "html.parser")
    # products = soup.find_all("ul", class_="products columns-4")
    items = soup.find_all("li", class_="product")

    if not items:
        print(f"Data not found or data no more data {page}")
        break

    for item in items:
        name = item.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = item.find("span", class_="woocommerce-Price-amount").text.strip()
        link = item.find("a")["href"]

        data.append({"product_name": name, "price": price, "link": link})

        page +=1

# Connector snowflake
conn = snowflake.connector.connect(
    user="LAMHOTPT",
    password="P@ssvv0rdP@ssvv0rd!!",              # kalau pakai username/password
    account="FCHSPXS-RP17491",  # tanpa .snowflakecomputing.com
    warehouse="COMPUTE_WH",
    database="PROJECTDB",
    schema="BRONZE",
    role="ACCOUNTADMIN",
    authenticator="snowflake"         # pakai username/password
    # kalau akunmu memang SSO, ganti jadi: authenticator="externalbrowser"
)

cur = conn.cursor()

cur.execute("""
    CREATE OR REPLACE TABLE countries (
    uid STRING DEFAULT UUID_STRING(),
    country_name VARCHAR,
    capital_name VARCHAR,
    population INT
    )
""")

cur.execute("""
    CREATE OR REPLACE TABLE products (
    uid STRING DEFAULT UUID_STRING(),
    product_name VARCHAR,
    price VARCHAR,
    link VARCHAR
    )
""")

for item in result:
    cur.execute("INSERT INTO countries (country_name, capital_name, population) VALUES (%s, %s, %s)",
        (item["country_name"], item["capital_name"], item["population"])
    )

conn.commit()

for item in data:
    cur.execute("INSERT INTO products (product_name, price, link) VALUES (%s, %s, %s)",
        (item["product_name"], item["price"], item["link"])
    )


conn.commit()
cur.close()
conn.close()
    # print(f"Country: {item['country_name']} - Capital: {item['capital_name']} - Population: {item['population']}")

      