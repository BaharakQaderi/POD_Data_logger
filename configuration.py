import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from datetime import datetime
import struct
import time

# Enable detailed debugging
logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

# Configuration
PORT = '/dev/serial0'  # Adjust based on your setup
BAUDRATE = 9600
SLAVE_ID = 3



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

    if client.connect():
        print("Modbus connection established successfully.")
        try:

            #Start to configuring the whole thing #MS 43, LS 44, MS 45, LS 46
            client.write_register(address=43, value=0x4000, slave=SLAVE_ID)
            client.write_register(address=44, value=0x0000, slave=SLAVE_ID)
            client.write_register(address=45, value=0x4348, slave=SLAVE_ID)
            client.write_register(address=46, value=0x0000, slave=SLAVE_ID)
            client.write_register(address=67, value=0xc2fa, slave=SLAVE_ID)
            client.write_register(address=67, value=0xabac, slave=SLAVE_ID)
            # client.write_register(address=43, value=0x4000, slave=3) 
            # client.write_register(address=44, value=0x0000, slave=3)
            # client.write_register(address=45, value=0x0000, slave=3)
            # client.write_register(address=46, value=0x4348, slave=3)
            # client.write_register(address=67, value=0xc2fa, slave=3)
            # client.write_register(address=67, value=0xabac, slave=3)
            
            print("-----------------------Configuration done!---------------------------------")
        except ModbusIOException as ex:
            print(f"Modbus IO Exception: {ex}")
        finally:
            client.close()
    else:
        print("Failed to establish Modbus connection.")

if __name__ == "__main__":
    main()