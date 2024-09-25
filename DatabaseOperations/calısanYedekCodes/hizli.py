import serial
import select
import time
import datetime
import threading
import queue
from pymongo import MongoClient, UpdateOne
from pymongo.server_api import ServerApi
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# Setup MongoDB Client URI
uri = "mongodb+srv://ASSAN:sifre@batterymanagementcluste.wyc4v.mongodb.net/?retryWrites=true&w=majority&appName=BatteryManagementCluster"

# Thread-gÃ¼venli veri kuyruÄŸu
data_queue = queue.Queue()

# Global deÄŸiÅŸkenler
testList, resultList = [], []
crc, indexTrack, dn, sum = 0, -1, 0, 0


def insert_to_db(database, collection, data, max_retries=3):
    client = None
    for attempt in range(max_retries):
        try:
            client = MongoClient(uri, server_api=ServerApi('1'), serverSelectionTimeoutMS=10000)
            db = client[database]
            coll = db[collection]

            if isinstance(data, list):
                print("it is updated:", data)
                coll.bulk_write([UpdateOne({'_id': item['time']}, {'$set': item}, upsert=True) for item in data])
            else:
                coll.update_one({'_id': data['time']}, {'$set': data}, upsert=True)

            print("Veri baÅŸarÄ±yla eklendi.")
            return
        except (ConnectionFailure, ServerSelectionTimeoutError) as e:
            print(f"BaÄŸlantÄ± hatasÄ±: {e}. Yeniden deneniyor... ({attempt + 1}/{max_retries})")
            time.sleep(2)
        except Exception as e:
            print(f"Beklenmeyen hata: {e}")
            return
        finally:
            if client:
                client.close()
    print("Maksimum yeniden deneme sayÄ±sÄ±na ulaÅŸÄ±ldÄ±. Veri eklenemedi.")


def interpretation(byte):
    global testList, dataLenght, crc, indexTrack, dn, sum, resultList

    byte_int = int(byte, 16)

    if byte_int > 0x7F:
        indexTrack = 0
        testList = [byte]
        resultList = [byte]
        sum = byte_int
    elif indexTrack > 2:
        if indexTrack > int(dataLenght, 16) + 2:
            crc = byte
            dn = 0
            indexTrack = -1
            resultList.append(byte)
            if sum % 9 == byte_int:
                sum = 0
                return resultList
            else:
                insert_to_db("BatteryManagement", "logs",
                             {"data": resultList, "Code": 200, "time": time.strftime("%d.%m.%Y")})
                sum = 0
                resultList = []
        else:
            testList.append(byte)
            resultList.append(byte)
            indexTrack += 1
            dn += 1
            sum += byte_int
    elif indexTrack == 2:
        dataLenght = byte
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 3
        sum += byte_int
    elif indexTrack == 1:
        testList.append(byte)
        resultList.append(byte)
        indexTrack = 2
        sum += byte_int
    elif indexTrack == 0:
        indexTrack = 1
        testList.append(byte)
        resultList.append(byte)
        sum += byte_int


def read_serial(ser):
    buffer = bytearray()
    while True:
        if select.select([ser], [], [], 0)[0]:
            buffer.extend(ser.read(ser.in_waiting))
            while buffer:
                interpreted_data = interpretation(f"{buffer[0]:02x}")
                if interpreted_data is not None:
                    data_queue.put(interpreted_data)
                buffer = buffer[1:]


def db_worker():
    batch = []
    last_insert = time.time()
    while True:
        try:
            data = data_queue.get(timeout=1)
            if data is None:
                break

            saltData = int(data[4], 16) * 100 + int(data[5], 16) * 10 + int(data[6], 16) + int(data[7], 16) * 0.1 + int(
                            data[8], 16) * 0.01 + int(data[9], 16) * 0.001
            salt_data = round(saltData, 4)

            record = {
                "header": int(data[0], 16),
                "k": int(data[1], 16),
                "Dtype": int(data[2], 16),
                "length": int(data[3], 16),
                "data": salt_data,
                "crc": int(data[-1], 16),
                "time": time.strftime("%d.%m.%Y, %H:%M:%S")
            }

            print("batche eklenen veri", record)
            batch.append(record)


            if len(batch) >= 100 or (time.time() - last_insert) > 5:
                insert_to_db("BatteryManagement", "clusters", {"data":batch})
                insert_to_db("BatteryManagement", "logs",
                             {"data": batch, "Code": 200, "time": time.strftime("%d.%m.%Y, %H:%M:%S")})
                batch = []
                last_insert = time.time()

            data_queue.task_done()
        except queue.Empty:
            if batch:
                insert_to_db("BatteryManagement", "clusters",{"data":batch})
                insert_to_db("BatteryManagement", "logs",
                             {"data": batch, "Code": 200, "time": time.strftime("%d.%m.%Y, %H:%M:%S")})
                batch = []
                last_insert = time.time()


def main():
    ser = serial.Serial(port="/dev/serial0", baudrate=115200, timeout=0)

    threading.Thread(target=read_serial, args=(ser,), daemon=True).start()
    db_thread = threading.Thread(target=db_worker, daemon=True)
    db_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program sonlandÄ±rÄ±lÄ±yor.")
    finally:
        ser.close()
        data_queue.put(None)
        db_thread.join()


if __name__ == '__main__':
    main()
