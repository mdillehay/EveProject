import requests
import json
import sqlite3

id_list = []
id_name = []

for page in range(1,2):
    esi_request = ('https://esi.evetech.net/latest/universe/types/?datasource=tranquility&page=' + str(page))
    response = requests.get(esi_request)
    data = json.loads(response.content)

    for item in data:
        id_list.append(item)

    if page == 2:
        print('TypeID page pull complete.')


for item in id_list:
    esi_request = ('https://esi.evetech.net/latest/universe/types/' + str(item) + '/?datasource=tranquility&language=en-us')
    response = requests.get(esi_request)
    data = json.loads(response.content)
    
    try:
        i_name = data['name']
        id_name.append((item, str(i_name)))
    except Exception:
        pass



conn = sqlite3.connect("EveNames.db")

conn.execute("CREATE table ItemNames(TypeID, ItemName)")
conn.executemany("INSERT into ItemNames(TypeID, ItemName) values (?, ?)", id_name)


