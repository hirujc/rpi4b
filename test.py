import time
import RPi.GPIO as GPIO
from RPLCD.i2c import CharLCD

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Define the GPIO pins for rows and columns (adjust based on your wiring)
ROW_PINS = [26, 5, 16, 17]  # GPIO pins for the rows
COL_PINS = [6, 27, 22, 23]  # GPIO pins for the columns

# Set up the row pins as output and column pins as input
for row in ROW_PINS:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)  # Set rows to HIGH initially

for col in COL_PINS:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set columns to input with pull-up

# Define the keypad layout (the matrix of buttons)
keypad_layout = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Initialize the LCD using I2C address 0x27
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1)

# Function to scan the keypad
def scan_keypad():
    for row_index, row in enumerate(ROW_PINS):
        # Set the current row LOW and the others HIGH
        GPIO.output(row, GPIO.LOW)
        
        for col_index, col in enumerate(COL_PINS):
            if GPIO.input(col) == GPIO.LOW:  # If the button is pressed
                # Return the corresponding key from the keypad layout
                return keypad_layout[row_index][col_index]
        
        GPIO.output(row, GPIO.HIGH)  # Reset the row to HIGH
    
    return None  # Return None if no key is pressed

# Main loop to read the keypad and print the pressed keys on the LCD
try:
    while True:
        key = scan_keypad()
        if key:
            lcd.clear()  # Clear the LCD before displaying the new key
            lcd.write_string(f"Key pressed: {key}")
            print(f"Key pressed: {key}")
        time.sleep(0.1)  # Small delay to debounce the button press

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit
