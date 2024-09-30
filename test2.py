import serial
import time

try:
    with serial.Serial('/dev/serial0', 115200, timeout=1) as ser:
        print('Serial port opened successfully.')
        while True:
            data = ser.read(10)
            if data:
                print(f'Received: {data.decode().strip()}')
            else:
                print('No data received.')
            time.sleep(1)
except serial.SerialException as e:
    print(f"Error: {e}")


    #pip install xsensdeviceapi-2022.0.0-cp310-none-linux_x86_64.whl
    #pip install ./python/xsensdeviceapi-2022.0.0-cp310-none-linux_x86_64.whl

    #/usr/bin/python3.11