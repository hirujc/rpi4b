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
    ['1', '2', '3', 'A'],  # A -> mapped to '+'
    ['4', '5', '6', 'B'],  # B -> mapped to '-'
    ['7', '8', '9', 'C'],  # C -> mapped to '*'
    ['*', '0', '#', 'D']   # D -> mapped to '/'
]

# Initialize the LCD using I2C address 0x27
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1)

# Variables for calculation
expression = ""
last_key = None
last_time = 0

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

# Function to update the LCD display
def update_display():
    lcd.clear()
    lcd.write_string(expression)

# Function to implement debounce
def debounce(key, current_time, debounce_delay=0.3):
    global last_key, last_time
    if key == last_key and (current_time - last_time) < debounce_delay:
        return False  # If the same key is pressed too quickly, ignore it
    last_key = key
    last_time = current_time
    return True  # Otherwise, accept the key press

# Main loop to read the keypad and perform calculations
try:
    while True:
        key = scan_keypad()
        
        if key:
            current_time = time.time()
            
            if debounce(key, current_time):  # Check if the key press is debounced
                if key == "#":  # Equals button (No extra functionality for # key)
                    try:
                        result = str(eval(expression))  # Evaluate the expression
                        expression = result
                    except Exception as e:
                        expression = "Error"
                elif key == 'A':  # Clear the expression (mapped to +)
                    expression += '+'  # Add '+' to the expression
                elif key == 'B':  # Backspace (remove last character)
                    expression = expression[:-1]
                elif key == 'C':  # '*' button
                    expression += '*'  # Multiply operator
                elif key == 'D':  # '/' button
                    expression += '/'  # Division operator
                elif key.isdigit() or key in ['+', '-', '*', '/']:  # If the key is a digit or operator
                    expression += key

                update_display()  # Update the LCD display with the current expression
                print(f"Current Expression: {expression}")
        
        time.sleep(0.05)  # Small delay for debouncing

except KeyboardInterrupt:
    GPIO.cleanup()  # Clean up GPIO on exit
