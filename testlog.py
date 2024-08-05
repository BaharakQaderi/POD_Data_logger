import csv
from datetime import datetime
import struct
import time
from pymodbus.client import ModbusSerialClient as ModbusClient
from pymodbus.exceptions import ModbusException

# Configuration
PORT = '/dev/serial0' # Adjust based on your setup
BAUDRATE = 9600
SLAVE_ID = 1
LOGFILE = 'weight_log.csv'
DURATION = 600  # Duration in seconds (e.g., 10 minutes)

def read_weight(client):
    """Reads weight from a Modbus device and returns it as a float."""
    try:
        # Assuming weight is stored in registers 63 & 64 (adjust as needed)
        result = client.read_holding_registers(63, 2, unit=SLAVE_ID)
        if not result.isError():
            # Combine the two registers and convert to float
            weight_raw = (result.registers[0] << 16) + result.registers[1]
            weight_bytes = struct.pack('>I', weight_raw)
            weight_float = struct.unpack('>f', weight_bytes)[0]
            return weight_float
        else:
            print("Error reading weight")
            return None
    except ModbusException as e:
        print(f"Modbus error: {e}")
        return None

def main():
    client = ModbusClient(method='rtu', port=PORT, baudrate=BAUDRATE, timeout=1)
    client.connect()

    start_time = time.time()
    with open(LOGFILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        csvwriter.writerow(['Timestamp', 'Weight'])

        while time.time() - start_time < DURATION:
            weight = read_weight(client)
            if weight is not None:
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                csvwriter.writerow([timestamp, weight])
                print(f"{timestamp}, {weight}")
            time.sleep(1)  # Delay between readings

    client.close()

if __name__ == "__main__":
    main()