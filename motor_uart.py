# Import necessary modules
from picozero import DigitalOutputDevice, PWMOutputDevice
import bluetooth
from ble_simple_peripheral import BLESimplePeripheral

# Create a Bluetooth Low Energy (BLE) object
ble = bluetooth.BLE()

# Create an instance of the BLESimplePeripheral class with the BLE object
sp = BLESimplePeripheral(ble)

# Motor pins
pin1 = DigitalOutputDevice(0)
pin2 = DigitalOutputDevice(1)
en1 = PWMOutputDevice(2)

# Initialize motor state pins to zero for the pins that require it
motor_state = 0

# Define a callback function to handle received data
def on_rx(data):
    print("Data received: ", data)  # Print the received data
    global motor_state # Access the global variable led_state
    if data == b'forward\r\n':  # Check if the received data is "forward"
        pin1.value = not motor_state
        pin2.value = 0
        motor_state = 1 - motor_state
    if data == b'backward\r\n':
        pin1.value = 0
        pin2.value = not motor_state
        motor_state = 1 - motor_state
    if data == b'half\r\n':
        en1.value = 0.5
    if data == b'full\r\n':
        en1.value = 1

# Start an infinite loop
while True:
    if sp.is_connected():  # Check if a BLE connection is established
        sp.on_write(on_rx)  
