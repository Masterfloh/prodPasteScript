import time
import random
import sys
import pyautogui  # Import pyautogui for simulating keyboard actions

# Path for the stop signal file
STOP_SIGNAL_FILE = "stop_signal.txt"

def paste_text(text):
    sleep_times = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7]  # List of possible sleep times

    for char in text:
        with open(STOP_SIGNAL_FILE, 'r') as f:
            stop_signal = f.read().strip()
            if stop_signal == "stop":
                print("Typing process stopped.")
                break  # Stop typing immediately when stop signal is received
        pyautogui.write(char)  # Simulate writing the character in the focused window
        time.sleep(random.choice(sleep_times))  # Simulate typing delay

if __name__ == "__main__":
    # Get the text from the command-line argument
    text = sys.argv[1]
    time.sleep(5)  # 5-second delay for the user to click into a text box
    paste_text(text)
