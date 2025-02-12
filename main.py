import RPi.GPIO as GPIO
import time

# GPIO Pin Setup
ROW_PINS = [19, 5, 16, 17]  # Row 1 → GPIO 19, Row 2 → GPIO 5, Row 3 → GPIO 16, Row 4 → GPIO 17
COL_PINS = [6, 27, 22, 23]  # Column 1 → GPIO 6, Column 2 → GPIO 27, Column 3 → GPIO 22, Column 4 → GPIO 23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Setup rows as output
for row_pin in ROW_PINS:
    GPIO.setup(row_pin, GPIO.OUT)
    GPIO.output(row_pin, GPIO.HIGH)

# Setup columns as input
for col_pin in COL_PINS:
    GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def read_keypad():
    for row_index, row_pin in enumerate(ROW_PINS):
        GPIO.output(row_pin, GPIO.LOW)  # Activate the row by setting it LOW
        for col_index, col_pin in enumerate(COL_PINS):
            if GPIO.input(col_pin) == GPIO.LOW:  # Check if the key is pressed
                time.sleep(0.2)  # Debounce
                GPIO.output(row_pin, GPIO.HIGH)  # Reset the row to HIGH
                return (row_index, col_index)  # Return the key coordinates
        GPIO.output(row_pin, GPIO.HIGH)  # Reset the row to HIGH

    return None  # No key pressed

def get_key(row, col):
    key_map = [
        ['1', '2', '3', 'A'],
        ['4', '5', '6', 'B'],
        ['7', '8', '9', 'C'],
        ['*', '0', '#', 'D']
    ]
    return key_map[row][col]

def sanitize_input(input_str):
    # We want to allow numbers, +, -, *, /, ( ) and . only
    allowed_chars = '0123456789+-*/.()'
    sanitized_input = ''.join(c for c in input_str if c in allowed_chars)
    return sanitized_input

# Initialize variables
current_input = ""
operation = None

try:
    while True:
        key = read_keypad()
        if key:
            row, col = key
            key_pressed = get_key(row, col)
            print(f"Key Pressed: {key_pressed}")

            if key_pressed == 'C':  # Clear
                current_input = ""
                print("Cleared")
            elif key_pressed == '#':  # Equals
                if current_input:
                    # Sanitize the input to only allow safe characters
                    sanitized_input = sanitize_input(current_input)
                    try:
                        result = eval(sanitized_input)  # Evaluate the expression
                        print(f"Result: {result}")
                        current_input = str(result)  # Store the result for future operations
                    except Exception as e:
                        print("Error:", e)
                        current_input = "Error"
            elif key_pressed == 'A':  # Plus
                current_input += "+"
            elif key_pressed == 'B':  # Minus
                current_input += "-"
            elif key_pressed == '*':  # Multiply
                current_input += "*"
            elif key_pressed == '/':  # Divide
                current_input += "/"
            elif key_pressed == '.':  # Decimal Point
                current_input += "."
            elif key_pressed in '0123456789':  # Numbers
                current_input += key_pressed

            print(f"Current Input: {current_input}")

            time.sleep(0.1)  # Small delay to prevent spamming

except KeyboardInterrupt:
    GPIO.cleanup()
    print("Exiting.")
