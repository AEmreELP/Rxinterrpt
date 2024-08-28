import serial
import select
import time

testList = []
crc = 0
indexTrack = -1
dn = 0


def interpretation(byte):
    global testList
    global dataLenght
    global crc
    global indexTrack
    global dn

    # print(f" Header is:{data[0]}")

    if str(byte) > "7F":
        print(f"Our Header is : {byte}")
        y = int(byte) & 7
        indexTrack = 0
        testList.append(byte)
    elif indexTrack > 2:
        if (indexTrack > int(dataLenght, 16) + 2):
            crc = byte
            print(f"Our CRC is : {byte}")
            print("Data Geldi")
            dn = 0
            indexTrack = -1
        else:
            testList.append(byte)
            indexTrack = indexTrack + 1
            dn = dn + 1
            print(f"Our {dn}.data is : {byte}")

    elif indexTrack == 2:
        print(f"Our Data Lenght is : {byte}")
        dataLenght = byte
        testList.append(byte)
        indexTrack = 3

    elif indexTrack == 1:
        print(f"Our command is : {byte}")
        komut = byte
        testList.append(byte)
        indexTrack = 2

    elif indexTrack == 0:
        print(f"Our K is : {byte}")
        k = byte
        n = ((0 * 128) + int(k, 16))
        indexTrack = 1
        testList.append(byte)


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
                # print(len(my_list))

                for item in my_list:
                    # print("En iÃ§te")
                    # Send each item as bytes (decode from hex to bytes)
                    # ser.write(bytes.fromhex(item))
                    interpretation(item)
                    my_list = []

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
