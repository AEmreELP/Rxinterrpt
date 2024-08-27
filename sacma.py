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
            ser.timeout = 0.1  # 0.1 saniye timeout
            new_data = ser.read_all()
            data += new_data

            # Yeni veri gelmediyse
            if not new_data:
                break
                while select.select([ser], [], [], 0)[0]:
                    # Use select to wait for data to be available

                    # Read data from serial port
                    data = ser.read_all()
                    if data:
                        # Print the integer and its hexadecimal representation
                        # Add the hexadecimal representation to the list
                        my_list.append(data.hex())
                        # print(f'Initial list: {my_list}')
                        paketNum = paketNum + 1

                        if paketNum > 11:
                            # print("Buraya girdi")
                            paketNum = 0
                            for item in my_list:
                                # print("En iÃ§te")
                                # Send each item as bytes (decode from hex to bytes)
                                ser.write(bytes.fromhex(item))
                            my_list = []
                            # interpretation()
                            # Flush the output if needed
                            # ser.flushOutput()





    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()
