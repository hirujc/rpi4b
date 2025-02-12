KEYPAD = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']  # 'D' represents division
]

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
    
    while True:
        print("Display:", display)
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
