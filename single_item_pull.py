import requests
import json
import sqlite3

def updateSingleItemInfo(TypeID):
    esi_request = ('https://esi.evetech.net/latest/universe/types/' + str(TypeID) + '/?datasource=tranquility&language=en-us')
    response = requests.get(esi_request)
    try:
        data = json.loads(response.content)
    except Exception:
        print('It still did not work')
        pass

    item_name = data['name']

    conn = sqlite3.connect("EveNames2.db")
    #conn.execute("INSERT INTO ItemNames (TypeID, ItemName) VALUES (?, ?)", (TypeID, item_name))
    conn.execute("UPDATE ItemNames SET ItemName=(?) WHERE TypeID=(?)", (item_name, TypeID))
    conn.commit()

if __name__ == '__main__':
    pass
