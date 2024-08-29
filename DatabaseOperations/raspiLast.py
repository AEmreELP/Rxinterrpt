import serial
import select
import time
import datetime
import threading
from pymongo import MongoClient
from pymongo.server_api import ServerApi

testList = []
crc = 0
indexTrack = -1
dn = 0
sum = 0
resultList = []
storeData = []
def insertToDB(database, collection, data):
    uri = "mongodb+srv://ASSAN:sifre@batterymanagementcluste.wyc4v.mongodb.net/?retryWrites=true&w=majority&appName=BatteryManagementCluster"
    client = MongoClient(uri, server_api=ServerApi('1'))

    db = client[f'{database}']
    collection = db[f"{collection}"]

    document = data
    insert_doc = collection.insert_one(document)
    client.close()

def interpretation(byte):
    global testList
    global dataLenght
    global crc
    global indexTrack
    global dn
    global sum
    global resultList

    if str(byte) > "7F":
        y = int(byte, 16) & 7
        indexTrack = 0
        testList.append(byte)
        resultList.append(byte)
        sum = sum + int(byte, 16)

    elif indexTrack > 2:
        if (indexTrack > int(dataLenght, 16) + 2):
            crc = byte
            print("Data Geldi")
            dn = 0
            indexTrack = -1
            resultList.append(byte)
            if (sum % 9 == int(byte, 16)):
                print("Data True")
                sum = 0
                try:
                    return resultList
                except:
                    print("interpretation Error")
                finally:
                    resultList = []
            else:
                print("Data False")
                sum = 0
                resultList = []
        else:
            testList.append(byte)
            resultList.append(byte)
            indexTrack = indexTrack + 1
            dn = dn + 1
            sum = sum + int(byte, 16)

    elif indexTrack == 2:
        dataLenght = byte
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 3
        sum = sum + int(byte, 16)

    elif indexTrack == 1:
        komut = byte
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 2
        sum = sum + int(byte, 16)

    elif indexTrack == 0:
        k = byte
        n = ((0 * 128) + int(k, 16))
        indexTrack = 1
        testList.append(byte)
        resultList.append(byte)
        sum = sum + int(byte, 16)

def storeOurDatas(data):
    global storeData
    storeData.append(data)


def main():
    paketNum = 0
    my_list = []
    ser = serial.Serial(
        port="/dev/serial0",
        baudrate=56000,
        timeout=0
    )
    try:
        while True:
            if select.select([ser], [], [], 0)[0]:
                data = ser.read_all()
                if data:
                    my_list.append(data.hex())

            if (len(my_list) > 0):
                for item in my_list:
                    a = interpretation(item)
                    my_list = []
                    if (a != None):
                        print(a[0])
                        now = time.localtime(time.time())
                        start = time.time()
                        a.append(time.strftime("%y/%m/%d %H:%M", now))
                        saltData = int(a[4], 16) * 100 + int(a[5], 16) * 10 + int(a[6], 16) + int(a[7], 16) * 0.1 + int(a[8], 16) * 0.10 + int(a[9], 16) * 0.001
                        storeOurDatas(a)
                        print(storeData)
                        insertToDB("Yasin", "Emre",
                                   {"header": a[0], "K constant": a[1], "Command": a[2], "Data Length": a[3],
                                    "Data": saltData, "CRC": a[10], "Time Now": a[11]})
                        print(a)
                        a = []
                        print(a)
                        end = time.time()
                        print(end-start)
                        print(threading.active_count())
                        print(threading.enumerate())
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
