
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def insertToDB(database,collection,data):

    uri = "mongodb+srv://ASSAN:sifre!!!@batterymanagementcluste.wyc4v.mongodb.net/?retryWrites=true&w=majority&appName=BatteryManagementCluster"
    client = MongoClient(uri, server_api=ServerApi('1'))


    db = client[f'{database}']
    collection = db[f"{collection}"]

    document = {f'{data}'}
    insert_doc = collection.insert_one(document)
    client.close()
