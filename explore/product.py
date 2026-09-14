import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL target
url = "https://scrapingcourse.com/ecommerce/"

# Ambil HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Cari semua produk
products = soup.find_all("li", class_="product")

data = []
for product in products:
    name = product.find("h2", class_="woocommerce-loop-product__title").text.strip()
    price = product.find("span", class_="woocommerce-Price-amount").text.strip()
    link = product.find("a")["href"]
    data.append({"Nama Produk": name, "Harga": price, "Link": link})

# Simpan ke DataFrame
df = pd.DataFrame(data)
print(df)

# # Export ke CSV
# df.to_csv("produk_scraped.csv", index=False)