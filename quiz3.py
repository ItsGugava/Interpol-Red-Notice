import requests
import json
import sqlite3

url = "https://ws-public.interpol.int/notices/v1/red/"

# 1
r = requests.get(url)
res = r.json()

# content = json.dumps(res, indent=4)
# print(content)
# print(r.headers)
# print(r.content)
# print(r.status_code)

# 2
with open("interpol_wanted.json", "w") as file:
    json.dump(res, file, indent=4)

# 3 - 4

wanted_id_list = []
all_wanted = res["_embedded"]["notices"]


for each in all_wanted:
    wanted_id_list.append(each["entity_id"].replace("/", "-"))

conn = sqlite3.connect("interpol_wanted.sqlite")
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS WANTED(
               id INTEGER PRIMARY KEY AUTOINCREMENT, 
               name VARCHAR(50),
               sex VARCHAR(6),
               nationality VARCHAR(20))""")

for id in wanted_id_list:
    r = requests.get(f"https://ws-public.interpol.int/notices/v1/red/{id}")
    res = r.json()
    print(f"Interpol is searching for criminal with name: {res['forename']}, sex: {res['sex_id']}, nationality: {res['country_of_birth_id']}")
    cursor.execute(f'''INSERT INTO WANTED(name, sex, nationality) VALUES("{res['forename']}", "{res['sex_id']}", "{res['country_of_birth_id']}")''')

conn.commit()
conn.close()





