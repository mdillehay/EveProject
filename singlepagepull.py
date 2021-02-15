import requests
import json
import sqlite3
import single_item_pull as sip
from tqdm import tqdm

id_list = []
id_name = []
error_list = []


for i in tqdm(range(40)):
	esi_request = ('https://esi.evetech.net/latest/universe/types/?datasource=tranquility&page=' + str(i+1))
	response = requests.get(esi_request)
	data = json.loads(response.content)

	for item in data:
    		id_list.append(item)



#print(id_list)


for item in tqdm(id_list):
    esi_request = ('https://esi.evetech.net/latest/universe/types/' + str(item) + '/?datasource=tranquility&language=en-us')
    response = requests.get(esi_request)
    try:
        data = json.loads(response.content)
    except Exception:
        error_list.append(item)
        pass

    try:
        i_name = data['name']
        id_name.append((item, str(i_name)))
    except Exception:
        pass

conn = sqlite3.connect("EveNames2.db")
conn.execute("CREATE TABLE IF NOT EXISTS ItemNames(TypeID, ItemName)")
conn.executemany("INSERT into ItemNames(TypeID, ItemName) values (?, ?)", id_name)
conn.commit()

if not error_list:
    pass
else: 
    for item in error_list:
        try:
            sip.updateSingleItemInfo(item)
            error_list.pop()
        except Exception:
            pass

print(error_list)

