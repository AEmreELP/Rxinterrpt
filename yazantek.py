import serial
import select
import time


def interpretation(data, indexTrack, y, n, dn, myList, crc):
    print("Data is here")
    print(data)

    # print(f" Header is:{data[0]}")
    for i in range(len(data)):

        if str(data[i]) > "7F":
            y = int(data[i]) & 7
            indexTrack = 0
        elif indexTrack > 2:
            if (indexTrack > int(dataLenght, 16) + 2):
                crc = data[i]
                print("Data Geldi")
                break
            else:
                myList.append(data[i])
                indexTrack = indexTrack + 1
                dn = dn + 1

        # elif indexTrack == 3:
        #     k = data[i]
        #     indexTrack = 4

        elif indexTrack == 2:
            dataLenght = data[i]
            indexTrack = 3

        elif indexTrack == 1:
            komut = data[i]
            indexTrack = 2

        elif indexTrack == 0:
            k = data[i]
            n = ((y * 128) + int(k, 16))
            indexTrack = 1
    return myList;


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

                # Read data from serial port
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

                    if (len(data) > 0):
                        # print("Buraya girdi")
                        paketNum = 0
                        print(my_list)
                        for item in my_list:
                            # print("En iÃ§te")
                            # Send each item as bytes (decode from hex to bytes)
                            ser.write(bytes.fromhex(item))

                        # interpretation()
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

"""Version 2 """
import serial
import select
import time


def interpretation(data, indexTrack, y, n, dn, myList, crc):
    print("Data is here")
    print(data)

    # print(f" Header is:{data[0]}")
    for i in range(len(data)):

        if str(data[i]) > "7F":
            y = int(data[i]) & 7
            indexTrack = 0
        elif indexTrack > 2:
            if (indexTrack > int(dataLenght, 16) + 2):
                crc = data[i]
                print("Data Geldi")
                break
            else:
                myList.append(data[i])
                indexTrack = indexTrack + 1
                dn = dn + 1

        # elif indexTrack == 3:
        #     k = data[i]
        #     indexTrack = 4

        elif indexTrack == 2:
            dataLenght = data[i]
            indexTrack = 3

        elif indexTrack == 1:
            komut = data[i]
            indexTrack = 2

        elif indexTrack == 0:
            k = data[i]
            n = ((y * 128) + int(k, 16))
            indexTrack = 1
    return myList;


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

                # Read data from serial port
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

            if (len(my_list) > 0):
                # print("Buraya girdi")
                paketNum = 0
                print(my_list)
                for item in my_list:
                    # print("En iÃ§te")
                    # Send each item as bytes (decode from hex to bytes)
                    ser.write(bytes.fromhex(item))

                    # interpretation()
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

"""Version 3"""
import serial
import select
import time


def interpretation(data, indexTrack, y, n, dn, myList, crc):
    print("Data is here")
    print(data)

    # print(f" Header is:{data[0]}")
    for i in range(len(data)):
        if str(data[i]) > "7F":
            y = int(data[i]) & 7
            indexTrack = 0
        elif indexTrack > 2:
            if (indexTrack > int(dataLenght, 16) + 2):
                crc = data[i]
                print("Data Geldi")
                break
            else:
                myList.append(data[i])
                indexTrack = indexTrack + 1
                dn = dn + 1

        # elif indexTrack == 3:
        #     k = data[i]
        #     indexTrack = 4

        elif indexTrack == 2:
            dataLenght = data[i]
            indexTrack = 3

        elif indexTrack == 1:
            komut = data[i]
            indexTrack = 2

        elif indexTrack == 0:
            k = data[i]
            n = ((y * 128) + int(k, 16))
            indexTrack = 1
    return myList;


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

                # Read data from serial port
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

            if (len(my_list) > 0):
                # print("Buraya girdi")
                paketNum = 0
                print(my_list)
                print(len(my_list))
                time.sleep(1)
                # ser.write(bytes.fromhex(my_list))
                # for item in my_list:
                # print("En iÃ§te")
                # Send each item as bytes (decode from hex to bytes)
                #    ser.write(bytes.fromhex(item))

                # interpretation()
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


"""Verison 4"""
import serial
import select
import time


def interpretation(byte, indexTrack, y, n, dn, myList, crc):
    print("Data is here")
    print(byte)

    # print(f" Header is:{data[0]}")
    for i in range(len(byte)):

        if str(byte) > "7F":
            y = int(byte) & 7
            indexTrack = 0
        elif indexTrack > 2:
            if (indexTrack > int(dataLenght, 16) + 2):
                crc = byte
                print("Data Geldi")
                break
            else:
                myList.append(byte)
                indexTrack = indexTrack + 1
                dn = dn + 1

        # elif indexTrack == 3:
        #     k = data[i]
        #     indexTrack = 4

        elif indexTrack == 2:
            dataLenght = byte
            indexTrack = 3

        elif indexTrack == 1:
            komut = byte
            indexTrack = 2

        elif indexTrack == 0:
            k = byte
            n = ((y * 128) + int(k, 16))
            indexTrack = 1
    return myList;


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

                # Read data from serial port
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

            if (len(my_list) > 0):
                # print("Buraya girdi")
                paketNum = 0
                # print(my_list)
                print(len(my_list))

                for item in my_list:
                    # print("En iÃ§te")
                    # Send each item as bytes (decode from hex to bytes)
                    ser.write(bytes.fromhex(item))
                    print(item)
                    my_list = []
                    # interpretation()
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

"""""Version 5 saplamaca"""

import serial
import select
import time

testList=[]
crc=0
indexTrack=-1
dn=0

def interpretation(byte, indexTrack=None, dataLenght=None, dn=None):
    print("Data is here")
    print(byte)

    # print(f" Header is:{data[0]}")

    if str(byte) > "7F":
        y = int(byte) & 7
        indexTrack = 0
        testList.append(byte)
    elif indexTrack > 2:
        if (indexTrack > int(dataLenght, 16) + 2):
            crc = byte
            print("Data Geldi")
        else:
            myList.append(byte)
            indexTrack = indexTrack + 1
            dn = dn + 1

    elif indexTrack == 2:
        dataLenght = byte
        testList.append(byte)
        indexTrack = 3

    elif indexTrack == 1:
        komut = byte
        testList.append(byte)
        indexTrack = 2

    elif indexTrack == 0:
        k = byte
        n = ((y * 128) + int(k, 16))
        indexTrack = 1
        testList.append(byte)




    return myList;


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

                # Read data from serial port
                data = ser.read_all()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

            if (len(my_list) > 0):
                # print("Buraya girdi")
                paketNum = 0
                # print(my_list)
                print(len(my_list))

                for item in my_list:
                    # print("En iÃ§te")
                    # Send each item as bytes (decode from hex to bytes)
                    ser.write(bytes.fromhex(item))
                    print(item)
                    my_list = []
                    # interpretation()
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

