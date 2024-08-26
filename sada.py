import serial
import select
def command(cod):
    if (cod == "0a"):
        return "Gerilim"
    elif (cod == "0b"):
        return "Akim"
    elif (cod == "0c"):
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


def interpretation(data):
    print("Data is here")
    print(data)
    if str(data[0]) > "80":
        # print(f" Header is:{data[0]}")
        for i in range(len(data)):
            print(data[i])
            komut = command(data[i][1])
            tip = typeOfMessage(data[i][2])
            uzunluk = lenghtOfData(data[i])
            CRC = sum_hex_values_and_modulo(data[i])
            print(f"Header  :{data[i][0]}\n"
                  f"Komut   :{komut}\n"
                  f"Tip     :{tip}\n"
                  f"Uzunluk :{uzunluk}\n"
                  f"Degerler:{data[i][4:4 + uzunluk]}\n"
                  f"CRC     :{CRC}\n")


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
            if select.select([ser], [], [], 0)[0]:
                # Read data from serial port
                data = ser.readline()
                if data:
                    # Print the integer and its hexadecimal representation
                    print(f"{int.from_bytes(data, 'big')} \t {data.hex()}")
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
    main()

