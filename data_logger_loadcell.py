import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from datetime import datetime
import struct
import time
import csv  # Import the csv module
import os
import RPi.GPIO as GPIO

# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger()

# Configuration
PORT = '/dev/serial0'  # Adjust based on your setup
BAUDRATE = 9600     
SLAVE_ID = 3
LOGFILE = 'modbus_data.csv'
BUFFER_SIZE = 10
GPIO_PIN = 4  # Set this to your GPIO pin number
GPIO.setmode(GPIO.BCM)  # Use Broadcom pin numbering
GPIO.setup(GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Set the pin as an input


def main():
    client = ModbusSerialClient(
        method='rtu',
        port=PORT,
        baudrate=BAUDRATE,
        timeout=1,
        parity='N',
        stopbits=1,
        bytesize=8
    )
    data_buffer = []  # Initialize the buffer
    if client.connect():
        print("Modbus connection established successfully.")
        # Check if the file exists and has content
        if not os.path.exists(LOGFILE) or os.stat(LOGFILE).st_size == 0:
            mode = 'w'  # Write mode, for creating a new file or clearing an existing one
        else:
            mode = 'a'  # Append mode, for adding to an existing file

        with open(LOGFILE, mode, newline='') as file:
            csv_writer = csv.writer(file)
            if mode == 'w':
                # Write the CSV headers only if the file is new or empty
                csv_writer.writerow(['Timestamp', 'Net Weight', 'GPIO Value'])
            try:
                while True:  # Change this condition to stop based on your requirement
                    if os.path.exists("stop.txt") :
                        print("STOPING...")
                        break
                    # Reading the weight value (32-bit float)
                    result_weight = client.read_holding_registers(address=63, count=2, slave=SLAVE_ID)
                    if not result_weight.isError():
                        weight_registers = result_weight.registers
                        if len(weight_registers) == 2:
                            # Calculate and convert the NetWeight
                            net_weight = (weight_registers[0] << 16) + weight_registers[1]
                            net_weight_bytes = struct.pack('>I', net_weight)
                            net_weight_float = struct.unpack('>f', net_weight_bytes)[0]
                            # data_buffer.append([datetime.now(), net_weight_float])
                            gpio_value = GPIO.input(GPIO_PIN)  # Read the value of the GPIO pin
                            data_buffer.append([datetime.utcnow(), net_weight_float, gpio_value])  # Append the GPIO value to the data buffer
                            print(f"Logged NET WEIGHT: {datetime.utcnow(), net_weight_float, gpio_value}")  
                            # Write the timestamp and weight to the CSV file
                            # csv_writer.writerow([datetime.now(), net_weight_float])

                            # print(f"Logged NET WEIGHT: {datetime.now(), net_weight_float}")
                            if len(data_buffer) >= BUFFER_SIZE:
                                # Write the buffer to the CSV file
                                csv_writer.writerows(data_buffer)
                                file.flush()
                                os.fsync(file.fileno())
                                data_buffer.clear()
                        else:
                            print("Error: Unexpected number of registers for weight value")
                    time.sleep(0.2)  # Adjust the sleep time as needed
            except ModbusIOException as ex:
                print(f"Modbus IO Exception: {ex}")
            finally:
                if data_buffer:
                    # Ensure any remaining data is written to the file
                    csv_writer.writerows(data_buffer)
                    file.flush()
                    os.fsync(file.fileno())
                client.close()
                pass
    else:
        print("Failed to establish Modbus connection.")

if __name__ == "__main__":
    main()