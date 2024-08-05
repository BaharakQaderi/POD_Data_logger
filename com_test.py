import logging
from pymodbus.client import ModbusSerialClient
from pymodbus.exceptions import ModbusIOException
from datetime import datetime
import struct
import time

# Enable detailed debugging
# logging.basicConfig(level=logging.DEBUG)
# log = logging.getLogger()

# Configuration
PORT = '/dev/serial0'  # Adjust based on your setup
BAUDRATE = 9600
SLAVE_ID = 3
LOGFILE = 'modbus_data.log' #x46KsXEJrrgc2YPTkhK6a249


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

            for i in range(10):

                # #reading the weight value
                result_adc = client.read_holding_registers(address=61, count=1, slave=SLAVE_ID)
                print("ADC VALUE:", result_adc)
                if not result_adc.isError():
                    adc_registers = result_adc.registers
                    if len(adc_registers) == 1:
                        adc_value = adc_registers[0]  # Directly use the 16-bit value
                        print("ADC VALUE:", adc_value)
                    else:
                        print("Error: Unexpected number of registers for ADC value")

                # Reading the weight value (32-bit float)
                result_weight = client.read_holding_registers(address=63, count=2, slave=SLAVE_ID)
                if not result_weight.isError():
                    weight_registers = result_weight.registers
                    if len(weight_registers) == 2:
                        # Calculate the 32-bit NetWeight value according to the provided formula
                        net_weight = (weight_registers[0] << 16) + weight_registers[1]
                        # Convert the calculated NetWeight to a floating-point number
                        net_weight_bytes = struct.pack('>I', net_weight)
                        net_weight_float = struct.unpack('>f', net_weight_bytes)[0]
                        print("NET WEIGHT Float Calculation:", net_weight_float, "RAW value:", weight_registers)
                    else:
                        print("Error: Unexpected number of registers for weight value")
        except ModbusIOException as ex:
            print(f"Modbus IO Exception: {ex}")
        finally:
            client.close()
    else:
        print("Failed to establish Modbus connection.")

if __name__ == "__main__":
    main()