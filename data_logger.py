import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from datetime import datetime
import struct
import time
import csv
import os

# Configuration
PORT = '/dev/serial0'
BAUDRATE = 9600
SLAVE_ID = 3
LOGFILE = 'modbus_data.csv'
BUFFER_SIZE = 10  # Number of readings before flushing to disk

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
        if not os.path.exists(LOGFILE) or os.stat(LOGFILE).st_size == 0:
            mode = 'w'
        else:
            mode = 'a'

        with open(LOGFILE, mode, newline='') as file:
            csv_writer = csv.writer(file)
            if mode == 'w':
                csv_writer.writerow(['Timestamp', 'Net Weight'])

            try:
                while True:
                    if os.path.exists("stop.txt"):
                        print("STOPPING...")
                        break
                    result_weight = client.read_holding_registers(address=63, count=2, slave=SLAVE_ID)
                    if not result_weight.isError():
                        weight_registers = result_weight.registers
                        if len(weight_registers) == 2:
                            net_weight = (weight_registers[0] << 16) + weight_registers[1]
                            net_weight_bytes = struct.pack('>I', net_weight)
                            net_weight_float = struct.unpack('>f', net_weight_bytes)[0]
                            data_buffer.append([datetime.now(), net_weight_float])
                            print(f"Logged NET WEIGHT: {datetime.now(), net_weight_float}")

                            if len(data_buffer) >= BUFFER_SIZE:
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
                # Ensure any remaining data is written to the file
                if data_buffer:
                    csv_writer.writerows(data_buffer)
                    file.flush()
                    os.fsync(file.fileno())
                client.close()
    else:
        print("Failed to establish Modbus connection.")

if __name__ == "__main__":
    main()