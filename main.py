import RPi.GPIO as GPIO
from time import sleep, time
from smbus2 import SMBus
from RPLCD.i2c import CharLCD

# Initialize GPIO and LCD
GPIO.setmode(GPIO.BCM)

# Define keypad configuration
KEYPAD = [
    ['1', '2', '3', 'A'],  # Row 0
    ['4', '5', '6', 'B'],  # Row 1
    ['7', '8', '9', 'C'],  # Row 2
    ['*', '0', '#', 'D']   # Row 3
]

ROW_PINS = [5, 6, 13, 19]  # GPIO pins connected to the row pins
COL_PINS = [12, 16, 20, 21]  # GPIO pins connected to the column pins

# Configure GPIO pins
for row_pin in ROW_PINS:
    GPIO.setup(row_pin, GPIO.OUT, initial=GPIO.LOW)
for col_pin in COL_PINS:
    GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Initialize the I2C LCD
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1, cols=16, rows=2)
lcd.clear()

# Function to read key press
def get_key():
    for row_idx, row_pin in enumerate(ROW_PINS):
        GPIO.output(row_pin, GPIO.HIGH)
        for col_idx, col_pin in enumerate(COL_PINS):
            if GPIO.input(col_pin) == GPIO.LOW:
                GPIO.output(row_pin, GPIO.LOW)
                return KEYPAD[row_idx][col_idx]
        GPIO.output(row_pin, GPIO.LOW)
    return None

# Function to handle long press
def check_long_press(key, duration=5):
    start_time = time()
    while time() - start_time < duration:
        if get_key() != key:
            return False
    return True

# Function to evaluate fractions
def evaluate_fraction(equation):
    try:
        num, denom = map(int, equation.split('/'))
        return str(num / denom)
    except:
        return "Error!"

# Calculator logic
def calculator():
    lcd.clear()
    lcd.write_string("Calculator Ready!")
    sleep(2)
    lcd.clear()

    equation = ""
    fraction_mode = False

    while True:
        key = get_key()
        if key:
            if key == '#':  # Handle # for equal or point
                if check_long_press('#'):
                    try:
                        if fraction_mode:
                            result = evaluate_fraction(equation)
                        else:
                            result = str(eval(equation))
                        lcd.clear()
                        lcd.write_string(f"{equation}=\n{result}")
                    except:
                        lcd.clear()
                        lcd.write_string("Error!")
                    sleep(2)
                    equation = ""
                    lcd.clear()
                else:
                    equation += '.'
                    lcd.write_string('.')
            elif key == '*':  # Handle * for fractions
                equation += '/'
                fraction_mode = True
                lcd.write_string('/')
            elif key == 'A' or key == 'B' or key == 'C' or key == 'D':  # Ignore A-D
                continue
            else:  # Handle numbers and other operators
                equation += key
                lcd.write_string(key)
        sleep(0.2)

try:
    calculator()
except KeyboardInterrupt:
    lcd.clear()
    GPIO.cleanup()
