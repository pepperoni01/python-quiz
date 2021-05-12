import requests
import json
import sqlite3

r = requests.get('https://whiskyhunter.net/api/auctions_data/')
print(r.status_code)  # ვბეჭდავ სტატუს კოდს. 200 არის OK
print(r.url)  # ვბეჭდავ რექვესთის ლინკს
print(r.cookies)  # ვბეჭდავ რექვესთის cookieებს

r_json = r.json()
r_loads = json.loads(r.text)

# ვქმნი json ფაილს და ვინახავ რექვესთით წამოღებულ ინფორმაციას json ფორმატში
with open('whisky.json', 'w') as f:
    json.dump(r_loads, f, indent=4)

conn = sqlite3.connect('whisky.sqlite')
c = conn.cursor()

# ბაზაში შევქმენი ახალი TABLE დასახელებით - "whisky"
c.execute("""CREATE TABLE if not exists whisky (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date VARCHAR(20),
                name VARCHAR(20),
                trading_volume FLOAT)""")
conn.commit()

for each in r_loads:
    date = each['dt']
    auction_name = each['auction_name']
    auction_trading_volume = each['auction_trading_volume']
    # კონსოლზე ვბეჭდავ სასურველ ინფორმაციას
    print("აუქციონის თარიღი: ", date, "სახელი: ", auction_name, "აუქციონის გაყიდვების დონე: ", auction_trading_volume)

    # ბაზაში ვინახავ დაბეჭდილს ინფორმაციას
    c.execute("INSERT INTO whisky (date, name, trading_volume) VALUES (?, ?, ?)",(date, auction_name, auction_trading_volume))
    conn.commit()

conn.close()