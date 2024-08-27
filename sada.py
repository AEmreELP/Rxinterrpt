import serial
import select

data=['0A','80' ,'07' ,'0A' ,'06' ,'0B' ,'0B' ,'0B' ,'0B' ,'0B' ,'0B','02']
data1 = ['0a', '10', '82', '08', '04', '02', '01', '02', '02', '02', '03', '09', '00', '0a', '10', '08', '04', '02',
        '01']

def command(cod):
    if (cod == "0a" or cod == "0A" ):
        return "Gerilim"
    elif (cod == "0b" or cod == "0B"):
        return "Akim"
    elif (cod == "0c" or cod == "0C"):
        return "Sicaklik"
    else:
        return "Wrong Code"
def typeOfMessage(messageType):
    if (messageType == "10"):
        return "Hex"
    elif (messageType == "20"):
        return "Decimal"
    elif (messageType == "30"):
        return "Binary"
    else:
        return "Wrong Code"
def lenghtOfData(data):
    myList = []
    for i in data[3:-2]:
        myList.append(i)

    return len(myList)
def sum_hex_values_and_modulo(hex_list):
    # Convert each hexadecimal string to an integer and sum them up
    total_sum = sum(int(x, 16) for x in hex_list[:-1])
    # Calculate the modulo by 9
    result = total_sum % 9
    return result
def sepFunc(data):
    indices = [index for index, value in enumerate(data) if int(value, 16) > 0x80]
    return indices
def slice_hex_list(data, indexes):
    sliced_parts = []
    for i in range(len(indexes)):
        start = indexes[i]
        if i + 1 < len(indexes):
            end = indexes[i + 1]
        else:
            end = len(data)
        sliced_parts.append(data[start:end])
    return sliced_parts


indexTrack = 0
y = 0
n = 0
dn = 0
myList = []
crc = 0
def interpretation(data, indexTrack, y, n, dn, myList, crc):
    print("Data is here")
    print(data)

    # print(f" Header is:{data[0]}")
    for i in range(len(data)):

        if str(data[i]) > "7F":
            header = data[i]
            y = int(data[i]) & 7
            indexTrack = 0
        elif indexTrack > 2:
            if (indexTrack > int(dataLenght,16) + 2):
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
    return print(f" Our header is      :{header}\n"
                 f" Our K is           :{k}\n"
                 f" Our Comand is      :{command(komut)}\n"
                 f" Our Data Lenght is :{dataLenght}\n"
                 f" Our Our Data is    :{myList}\n"
                 f" Our CRC is         :{crc}\n");

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
            # Use select to wait for data to be available
            if select.select([ser], [], [], 1)[0]:
                # Read data from serial port
                data = ser.readline()
                if data:
                    # Print the integer and its hexadecimal representation
                    # Add the hexadecimal representation to the list
                    my_list.append(data.hex())
                    print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

                    if paketNum > 38:
                        paketNum = 0
                        for item in my_list:
                            # Send each item as bytes (decode from hex to bytes)
                            ser.write(bytes.fromhex(item))
                        my_list = []
                        interpretation(slice_hex_list(data, sepFunc(my_list)))
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
    print(interpretation(data, indexTrack, y, n, dn, myList, crc))
    #main()
