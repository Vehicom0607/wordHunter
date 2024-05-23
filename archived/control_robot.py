import serial
import time

current_pos = [0, 0, 0]

SIZE = 12
X_TOP = 133
Y_TOP = 17

file_path = "archived/gcode/grbl_test.gcode"
serial_port = "/dev/tty.usbserial-130"  # Change this to your serial port
baud_rate = 115200  # Change this to match your device's baud rate

ser = serial.Serial(serial_port, baud_rate)
time.sleep(2)  # Wait for the connection to establish
def wait_time(x, y, pos):
    limiting_reagent = max(abs(pos[0] - x), abs(pos[1] - y))
    return limiting_reagent / 300

def move(x, y, pos):
    ser.write(("G0 X{x} Y{y}".format(x=x, y=y) + '\n').encode())
    time.sleep(wait_time(x, y, pos))
    return [x, y, pos[2]]
def up(pos):
    ser.write(("G0 Z0" + '\n').encode())
    time.sleep(0.1)
    return [pos[0], pos[1], 5]

def down(pos):
    ser.write(("G0 Z4" + '\n').encode())
    time.sleep(0.1)
    return [pos[0], pos[1], 0]

def reset(pos):
    ser.write(("$1=255" + '\n').encode())
    pos = move(0, 0, pos)
    pos = up(pos)
    return pos

def move_grid(x, y, pos):
    pos = move(X_TOP + y * SIZE, Y_TOP + x * SIZE, pos)
    return pos
def grid(pos):
    time.sleep(1)
    for i in range(4):
        for j in range(4):
            pos = move(X_TOP + i * SIZE, Y_TOP + j * SIZE, pos)
    return pos

def claim_word(letters, pos):
    pos = move_grid(letters[0][0], letters[0][1], pos)
    pos = down(pos)
    for letter in letters[1:]:
        pos = move_grid(letter[0], letter[1], pos)
    pos = up(pos)
    return pos

def send_gcode(file_path):
    try:
        # Open serial port

        # Open G-code file
        with open(file_path, 'r') as gcode_file:
            for line in gcode_file:
                line = line.strip()  # Remove leading/trailing whitespace
                if line and not line.startswith(';'):  # Skip comments and empty lines
                    print("Sending:", line)
                    ser.write((line + '\n').encode())  # Send line with newline character
                    time.sleep(0.5)  # Adjust as necessary for your setup

        # Close serial port
        ser.close()
        print("G-code file sent successfully!")

    except Exception as e:
        print("An error occurred:", e)


# send_gcode(file_path)
current_pos = reset(current_pos)
letters = [[2, 3],
           [1, 3],
           [0, 3],
           [1, 2],
           [1, 1]]

current_pos = claim_word(letters, current_pos)
current_pos = up(current_pos)
current_pos = move_grid(0, 0, current_pos)
current_pos = down(current_pos)
current_pos = move_grid(2, 2, current_pos)
current_pos = up(current_pos)


ser.close()


