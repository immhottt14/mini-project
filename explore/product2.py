import snowflake.connector
import requests
from bs4 import BeautifulSoup
import pandas as pd

#page-url = https://www.scrapingcourse.com/ecommerce/page/12/

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
    products = soup.find("ul", class_="products columns-4")
    items = soup.find_all("li", class_="product")

    if not items:
        print(f"Data not found or data no more data {page}")
        break

    for item in items:
        name = item.find("h2", class_="woocommerce-loop-product__title").text.strip()
        price = item.find("span", class_="woocommerce-Price-amount").text.strip()
        link = item.find("a")["href"]

        data.append({"Nama Produk": name, "Harga": price, "Link": link})

        page +=1

# Simpan ke DataFrame
df = pd.DataFrame(data)
print(df)