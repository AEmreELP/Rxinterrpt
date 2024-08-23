import serial
import select

def main():
    # Set up serial connection (adjust parameters as needed)
    ser = serial.Serial(
        port="/dev/serial0",  # Update with your serial port
        baudrate=115200,
        timeout=0  # Non-blocking read
    )

    try:
        while True:
            # Use select to wait for data to be available
            if select.select([ser], [], [], 0.1)[0]:
                # Read data from serial port
                data = ser.readline()
                if data:
                    ser.flushOutput()
                    ser.write(data.encode())
    except KeyboardInterrupt:
        print("Exiting program.")
    finally:
        ser.close()

if __name__ == '__main__':
    main()
