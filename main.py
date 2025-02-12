import RPi.GPIO as GPIO
import time
import smbus
from time import sleep

# I2C Setup
I2C_ADDR = 0x27  # I2C address of the LCD
bus = smbus.SMBus(1)  # I2C bus

# Define row and column pins for the keypad
COL_PINS = [17, 16, 5, 19]  # GPIO pins for rows
ROW_PINS = [23, 22, 27, 6]  # GPIO pins for columns

# Define keypad layout
KEYPAD = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']  # 'D' represents division
]

# LCD initialization
def lcd_write(cmd, mode=0):
    """Write a command or data to the LCD."""
    bus.write_byte_data(I2C_ADDR, mode, cmd)

def lcd_clear():
    """Clear the LCD screen."""
    lcd_write(0x01, 0)  # Clear display

def lcd_init():
    """Initialize the LCD."""
    lcd_write(0x33, 0)
    lcd_write(0x32, 0)
    lcd_write(0x06, 0)
    lcd_write(0x0C, 0)
    lcd_write(0x28, 0)
    lcd_clear()

def lcd_display(text):
    """Display text on the LCD."""
    for i in range(len(text)):
        lcd_write(ord(text[i]), 1)  # Write each character to the LCD

# Set up GPIO mode
GPIO.setmode(GPIO.BCM)
for pin in ROW_PINS:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Rows as inputs (with pull-up resistors)
for pin in COL_PINS:
    GPIO.setup(pin, GPIO.OUT)  # Columns as outputs

# Function to detect key presses
def detect_keypress():
    while True:
        for row in range(4):
            GPIO.setup(ROW_PINS[row], GPIO.OUT)  # Activate row by setting it as output
            for col in range(4):
                GPIO.setup(COL_PINS[col], GPIO.IN, pull_up_down=GPIO.PUD_UP)  # Set column as input to detect low voltage
                if GPIO.input(COL_PINS[col]) == GPIO.LOW:
                    key = KEYPAD[row][col]
                    if key == 'C':  # Clear
                        return "clear"
                    if key == '#':  # Equals
                        return "="
                    if key == '*':  # Multiplication
                        return "*"
                    if key == 'B':  # Subtract
                        return "-"
                    if key == 'D':  # Division
                        return "/"
                    print(f"Key Pressed: {key}")
                    time.sleep(0.3)  # Debounce delay to avoid multiple key presses

def main():
    current_input = ""
    operator = ""
    result = 0
    display = ""
    
    lcd_init()
    lcd_display("Ready")  # Initial message on LCD
    time.sleep(2)  # Display for 2 seconds
    
    while True:
        print("Display:", display)
        lcd_clear()  # Clear the LCD each time before updating
        lcd_display(display)  # Display the current value on the LCD
        
        key = detect_keypress()
        
        if key == "clear":
            current_input = ""
            operator = ""
            result = 0
            display = ""
        elif key == "=":
            if operator:
                try:
                    if operator == "+":
                        result += float(current_input)
                    elif operator == "-":
                        result -= float(current_input)
                    elif operator == "*":
                        result *= float(current_input)
                    elif operator == "/":
                        result /= float(current_input)
                    display = str(result)
                    current_input = ""
                    operator = ""
                except Exception as e:
                    print(f"Error: {e}")
                    display = "Error"
            else:
                display = current_input
        elif key == "*":
            operator = "*"
            display += " * "
        elif key == "-":
            operator = "-"
            display += " - "
        elif key == "/":
            operator = "/"
            display += " / "
        else:
            current_input += key
            display += key

# Start the calculator
try:
    main()
finally:
    GPIO.cleanup()
