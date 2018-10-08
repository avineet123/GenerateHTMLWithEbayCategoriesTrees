import sqlite3
import os
import requests
import xml.etree.ElementTree as ET

def delete_database():
    filelist = [ f for f in os.listdir(".") if f == 'categories_ht.db' ]
    for f in filelist:
        os.remove(f)

def create_database():
    conn = sqlite3.connect('categories_ht.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE categories
                 (id integer primary key, categoryName text, categoryLevel integer, bestOfferEnabled integer,
                  categoryParentID integer)''')

    conn.commit()
    conn.close()

def get_categories():
    request_headers = {
        'X-EBAY-API-CALL-NAME': 'GetCategories',
        'X-EBAY-API-APP-NAME': 'EchoBay62-5538-466c-b43b-662768d6841',
        'X-EBAY-API-CERT-NAME': '00dd08ab-2082-4e3c-9518-5f4298f296db',
        'X-EBAY-API-DEV-NAME': '16a26b1b-26cf-442d-906d-597b60c41c19',
        'X-EBAY-API-SITEID': '0',
        'X-EBAY-API-COMPATIBILITY-LEVEL': '861'
    }
    data_xml = '''<?xml version="1.0" encoding="utf-8"?>
                <GetCategoriesRequest xmlns="urn:ebay:apis:eBLBaseComponents">
                  <CategorySiteID>0</CategorySiteID>
                  <ViewAllNodes>True</ViewAllNodes>
                  <DetailLevel>ReturnAll</DetailLevel>
                  <RequesterCredentials>
                    <eBayAuthToken>AgAAAA**AQAAAA**aAAAAA**y6rfVg**nY+sHZ2PrBmdj6wVnY+sEZ2PrA2dj6wFk4GhAJeHqQydj6x9nY+seQ**PbwDAA**AAMAAA**8OlM6fqJvNyuqK22AdBhw6/Ef9NR5TFA4TbCh2Kj5aZa+cRwuCmml6OFQ9bPWMiCn6fRqiKYjZW4SnihoRtnJhcq9UQL7sgWd7S7rV6k2LMAvUdPWbIadFnxroUnbDpAfCxx+MKKVo4Ez6ENlhtYFVhuVXYRWZ644UVGuTz3JMFdS97ZvTQiZI6oKkRPJM7uYs3+t2VvTzuaI63zMrtIZtsHO2H+qxrqChDL4eGr1K6ugJ1tSYztrmhf2vdtd01QID2CbVrEI/NJOypCs8nTXKEcvMtEsaUmU6ZdlmhTWnfHa45UAWHlEC/sG86r7Y/g72DEhl1SOrRLnng9CnTTT0274q9aJDwgoxK1u6TyP1qoKsa8FrCzIFdevT3FZ2d59PCk6jdKgKEyYiP8EmeNOK82QDOLverS7AhUrJB/fhMMurYy9mQpl0wyz5P8SVbtRb5r8ae3VXM2Sy2+7iSXwjwTyYDkS/ZeBMAEjXslMptIVMUi7pKqUMZofp2nClqrYOJ7k9SHCO3tCG6eckKznOdznSlcizf8/gHNg8AX9i4Dxx6s+L7HebrYptYM565446z7W3hD6fwuzXMONL0q0jffaJvF+buKFVTN/pPXhO/idD310Im5z1NGmb8/suCD6h0jOEGbSl8VRcQ/vNil2ddojHRmKTZr425Rc1JZhAfka4Yem8PmJrVE64C+4PbGXpusrEMK0z5fDpxcAfBw1B+zug42MZuFlO/1xvKEkwopwHlBq4S02sHuiZpfte23</eBayAuthToken>
                  </RequesterCredentials>
                </GetCategoriesRequest>'''

    r =requests.post('https://api.sandbox.ebay.com/ws/api.dll', headers=request_headers, data=data_xml)


    root = ET.fromstring(r.text.encode('utf-8'))
    categories = root.find('{urn:ebay:apis:eBLBaseComponents}CategoryArray')

    conn = sqlite3.connect('categories_ht.db')
    c = conn.cursor()
    categories_array_sql = []
    for child in categories:
        id = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryID').text)
        categoryName = child.find('{urn:ebay:apis:eBLBaseComponents}CategoryName').text
        categoryLevel = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryLevel').text)

        bestOfferEnabled = 0
        try:
            if child.find('{urn:ebay:apis:eBLBaseComponents}BestOfferEnabled').text == 'true':
                bestOfferEnabled = 1
        except Exception as e:
            pass

        categoryParentID = int(child.find('{urn:ebay:apis:eBLBaseComponents}CategoryParentID').text)
        if categoryParentID == id:
            categoryParentID = -1

        category = (id, categoryName, categoryLevel, bestOfferEnabled, categoryParentID)
        categories_array_sql.append(category)

    c.executemany('INSERT INTO categories(id, categoryName, categoryLevel, bestOfferEnabled, categoryParentID) VALUES (?,?,?,?,?)', categories_array_sql)

    conn.commit()
    conn.close()
try:
    delete_database()
    create_database()
    get_categories()
except Exception as e:
    print(e)
    #delete_database()
    print ('Error creating the db or getting the data')

