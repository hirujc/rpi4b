from RPLCD.i2c import CharLCD
import time

# Initialize the LCD (Change address if needed)
lcd = CharLCD(i2c_expander='PCF8574', address=0x27, port=1,
              cols=16, rows=2, charmap='A00', auto_linebreaks=True)

# Display Messages
lcd.write_string("Hello, World!")
lcd.cursor_pos = (1, 0)  # Move to second line
lcd.write_string("Raspberry Pi 4")

# Keep the message for 5 seconds
time.sleep(5)

# Clear the display
lcd.clear()
