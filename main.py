import serial
import select
import time
import datetime
import threading
import queue
from pymongo import MongoClient
from pymongo.server_api import ServerApi

# Setup MongoDB Client URI
uri = "mongodb+srv://ASSAN:sifre@batterymanagementcluste.wyc4v.mongodb.net/?retryWrites=true&w=majority&appName=BatteryManagementCluster"

# Thread-safe queue to hold data
data_queue = queue.Queue()
testList = []
crc = 0
indexTrack = -1
dn = 0
sum = 0
resultList = []


# MongoDB insert function
def insertToDB(database, collection, data):
    client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=60000)
    db = client[database]
    coll = db[collection]
    coll.insert_one(data)
    # client.close()    #When I run this code After a minute connection is closing and its not inster data to DB


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


# Function to read data from the serial port in a separate thread
def read_serial(ser):
    paketNum = 0
    my_list = []

    while True:
        if select.select([ser], [], [], 0)[0]:
            # Use select to wait for data to be available
            data = ser.read_all()
            if data:
                my_list.append(data.hex())
                paketNum += 1

        if my_list:
            paketNum = 0
            for item in my_list:
                interpreted_data = interpretation(item)
                if interpreted_data is not None:
                    # Add interpreted data to the thread-safe queue
                    data_queue.put(interpreted_data)
            my_list = []


# Function to insert data into the database in a separate thread
def db_worker():
    while True:
        # Get data from the queue and insert into the database
        data = data_queue.get()
        if data is None:
            break  # Sentinel for exit
        saltData = int(data[4], 16) * 100 + int(data[5], 16) * 10 + int(data[6], 16) + int(data[7], 16) * 0.1 + int(
            data[8], 16) * 0.01 + int(data[9], 16) * 0.001
        saltData = round(saltData, 4)
        insertToDB("BatteryManagement", "clusters",
                   {"header": int(data[0], 16), "k": int(data[1], 16), "type": int(data[2], 16),
                    "lenght": int(data[3], 16), "data": saltData, "crc": int(data[-1], 16)})
        data_queue.task_done()
        print("Data inserted into DB:", data)
        print("Success Code : 200")


def main():
    # Set up serial connection (adjust parameters as needed)
    ser = serial.Serial(
        port="/dev/serial0",  # Update with your serial port
        baudrate=56000,
        timeout=0  # Non-blocking read
    )

    # Create and start threads
    threading.Thread(target=read_serial, args=(ser,), daemon=True).start()
    db_thread = threading.Thread(target=db_worker, daemon=True)
    db_thread.start()

    try:
        # Main thread can perform other tasks or just wait for threads to finish
        while True:
            time.sleep(1)  # Simulate some work (e.g., logging, monitoring)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        # Clean up
        ser.close()
        # Insert 'None' as a sentinel to shut down db_worker thread
        data_queue.put(None)
        db_thread.join()


if __name__ == '__main__':
    main()
