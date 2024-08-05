import serial

# Configuration
PORT = '/dev/ttyS0'  # Adjust based on your RS-485 adapter configuration
BAUDRATE = 9600
TIMEOUT = 1  # 1 second timeout

def test_serial_connection():
    try:
        # Open serial port
        ser = serial.Serial(
            port=PORT,
            baudrate=BAUDRATE,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=TIMEOUT
        )

        if ser.is_open:
            print(f"Serial port {PORT} opened successfully.")

            # Send a test message
            test_message = b'Hello, RS-485!'
            ser.write(test_message)
            print(f"Sent: {test_message}")

            # Wait for a response (you may need to loop this if waiting for an external response)
            response = ser.read(len(test_message))
            print(f"Received: {response}")

            ser.close()
        else:
            print(f"Failed to open serial port {PORT}.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_serial_connection()