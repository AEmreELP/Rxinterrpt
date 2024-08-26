import serial
import select


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
                # data=print(f"{int.from_bytes(data, 'big'):02X}")
                print(f"{int.from_bytes(data)} /t {data.hex()}")
                # data = int.from_bytes(data)
                if (data.hex() == hex(0x0a)):
                    print(data)
                # data = int(data.hex(), 16)
                # print(paketNum)

                my_list.append(data)
                if data:
                    # print(data)
                    # print(f'Initial list: {my_list}')
                    paketNum = paketNum + 1

                    # my_list = my_list.append(paketNum)
                    if (paketNum > 12):
                        paketNum = 0
                        for i in range(len(my_list)):
                            ser.write(my_list[i])
                        my_list = []
                        # ser.flushOutput()
                        # ser.write(my_list)
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()


if __name__ == '__main__':
    main()
