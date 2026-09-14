import requests
from bs4 import BeautifulSoup
import snowflake.connector

# url website

url = 'https://books.toscrape.com/index.html'

#ambil data dari website
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

#cari books
products = soup.find_all("article", class_="product_pod")

data = []
for product in products:
    name = product.find("h3", class_="woocommerce-loop-product__title").text.strip()
    price = product.find("span", class_="woocommerce-Price-amount").text.strip()
    link = product.find("a")["href"]
    data.append({"Nama Produk": name, "Harga": price, "Link": link})
