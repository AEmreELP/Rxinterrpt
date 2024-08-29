import serial
import select
import time
from pymongo import MongoClient
from pymongo.server_api import ServerApi

testList = []
crc = 0
indexTrack = -1
dn = 0
sum = 0
resultList = []


def insertToDB(database, collection, data):
    uri = "mongodb+srv://ASSAN:sifre!!!!!@batterymanagementcluste.wyc4v.mongodb.net/?retryWrites=true&w=majority&appName=BatteryManagementCluster"
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

    # print(f" Header is:{data[0]}")

    if str(byte) > "7F":
        #print(f"Our Header is : {byte}")
        y = int(byte, 16) & 7
        indexTrack = 0
        testList.append(byte)
        resultList.append(byte)
        sum = sum + int(byte, 16)

    elif indexTrack > 2:
        if (indexTrack > int(dataLenght, 16) + 2):
            crc = byte
            #print(f"Our CRC is : {byte}")
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
                    resultList=[]
            else:
                print("Data False")
                sum = 0
                resultList = []
        else:
            testList.append(byte)
            resultList.append(byte)
            indexTrack = indexTrack + 1
            dn = dn + 1
            #print(f"Our {dn}.data is : {byte}")
            sum = sum + int(byte, 16)

    elif indexTrack == 2:
        #print(f"Our Data Lenght is : {byte}")
        dataLenght = byte
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 3
        sum = sum + int(byte, 16)

    elif indexTrack == 1:
        #print(f"Our command is : {byte}")
        komut = byte
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 2
        sum = sum + int(byte, 16)

    elif indexTrack == 0:
        #print(f"Our K is : {byte}")
        k = byte
        n = ((0 * 128) + int(k, 16))
        indexTrack = 1
        testList.append(byte)
        resultList.append(byte)
        sum = sum + int(byte, 16)


def resultListSetEmpty():
    global resultList
    resultList = []


def summation(byte):
    global indexTrack
    global sum
    global dn
    if (indexTrack > -1):
        sum = sum + int(byte, 16)

    if dn > 0:
        sum = sum % 9

    return sum


def main():
    paketNum = 0
    my_list = []
    # Set up serial connection (adjust parameters as needed)
    ser = serial.Serial(
        port="/dev/serial0",  # Update with your serial port
        baudrate=56000,
        timeout=0  # Non-blocking read
    )
    try:
        while True:

            if select.select([ser], [], [], 0)[0]:
                # Use select to wait for data to be available
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')


            if (len(my_list) > 0):

                for item in my_list:
                    # Send each item as bytes (decode from hex to bytes)
                    # ser.write(bytes.fromhex(item))
                    a = interpretation(item)
                    print("interpretation dan gelen A")
                    print(a)
                    my_list = []
                    b = {"name": "John", "age": 30, "city": "New York"}
                    if (a != None):
                        print(a[0])

                        saltData = int(a[4], 16) * 100 + int(a[5], 16) * 10 + int(a[6], 16) + int(a[7], 16) * 0.1 + int(
                            a[8], 16) * 0.10 + int(a[9], 16) * 0.001

                        insertToDB("Yasin", "Emre",
                                   {"header": a[0], "K constant": a[1], "Command": a[2], "Data Lenght": a[3],
                                    "Data": saltData, "CRC": a[10]})
                        a=[]
                        print(a)

                # a=summation(item)
                # print(a)

                # Flush the output if needed
                # ser.flushOutput()






    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()


if __name__ == '__main__':
    indexTrack = -1
    y = 0
    n = 0
    dn = 0
    myList = []
    crc = 0
    main()
