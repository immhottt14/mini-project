import requests
import snowflake.connector

conn = snowflake.connector.connect(
    user="LAMHOTPT",
    password="P@ssvv0rdP@ssvv0rd!!",              # kalau pakai username/password
    account="FCHSPXS-RP17491",  # tanpa .snowflakecomputing.com
    warehouse="COMPUTE_WH",
    database="PROJECTDB",
    schema="PUBLIC",
    role="ACCOUNTADMIN",
    authenticator="snowflake"         # pakai username/password
    # kalau akunmu memang SSO, ganti jadi: authenticator="externalbrowser"
)

cur = conn.cursor()

# Buat tabel
cur.execute("""
    CREATE OR REPLACE TABLE posts (
        id INT,
        title STRING,
        body STRING
    )
""")

# Ambil data API
url = "https://jsonplaceholder.typicode.com/posts"
response = requests.get(url)
data = response.json()

# Insert ke Snowflake
for row in data[:10]:
    cur.execute(
        "INSERT INTO posts (id, title, body) VALUES (%s, %s, %s)",
        (row["id"], row["title"], row["body"])
    )

conn.commit()
cur.close()
conn.close()