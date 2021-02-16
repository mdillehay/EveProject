import requests
import json
import sqlite3
import single_item_pull as sip
from tqdm import tqdm

id_list = []
id_name = []
error_list = []

# tqdm is a lightweight very simple progress bar feature. 
# this  FOR LOOP pulls 'TypeID' data from the ESI API and builds a list that can be iterated over.
for i in tqdm(range(40)):
	esi_request = ('https://esi.evetech.net/latest/universe/types/?datasource=tranquility&page=' + str(i+1))
	response = requests.get(esi_request)
	data = json.loads(response.content)

	for item in data:
    		id_list.append(item)



#print(id_list)

# this FOR LOOP pulls 'Item Name' data from ESI API using the list of 'TypeID's built in above LOOP. It then builds
# another LIST of  (TypeID, ItemName) sets for every TypeID in the above LIST. 
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


# Add info to a SQLITE DB
conn = sqlite3.connect("EveNames2.db")
conn.execute("CREATE TABLE IF NOT EXISTS ItemNames(TypeID, ItemName)")
conn.executemany("INSERT into ItemNames(TypeID, ItemName) values (?, ?)", id_name)
conn.commit()


# Checks the 'error_list' for logged errors, if found, it attempts to pull that info from ESI again using the
# 'updateSingleItem' Method from 'single_item_pull.py'. Then removes that item from list.
if not error_list:
    pass
else: 
    for item in error_list:
        try:
            sip.updateSingleItemInfo(item)
            error_list.pop(len(error_list) - (len(error_list)-1))
        except Exception:
            pass

print(error_list)

