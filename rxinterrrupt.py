import serial
import select

def main():
    # Set up serial connection (adjust parameters as needed)
    ser = serial.Serial(
        port='/dev/ttyUSB0',  # Update with your serial port
        baudrate=115200,
        timeout=1  # Non-blocking read
    )

    try:
        while True:
            # Use select to wait for data to be available
            if select.select([ser], [], [], 1)[0]:
                # Read data from serial port
                data = ser.readline()
                if data:
                    print(f"Received: {data.decode('utf-8').strip()}")
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
