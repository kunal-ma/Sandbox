# Task: GUI-based TOTP Generator.
# Description: Generates and displays a 6-digit Time-based OTP that refreshes every 30 seconds using a Base32-encoded secret key.

# Permissions: None
# Dependencies: Tkinter for GUI Application

# WARNING: Scripting TOTP defeats the purpose of 2FA by storing secrets and credentials together. DO NOT DO THIS unless you fully understand the security risks.

# Acknowledgements: Thanks to mintotp (https://github.com/susam/mintotp) for the TOTP generation algorithm. 

# --------------------------------------------------

# Variables for OTP Generation
secret = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"   # Base32 secret key
length = 6       				        # Character length of OTP
window = 30      				        # Token period in seconds
digest = "sha1"  			            # Encryption algorithm

# Variables for GUI Interface
bcolor = "black"                        # Background color
fcolor = "white"                        # Text color

# --------------------------------------------------

# Importing necessary libraries
import time
import hmac
import base64
import struct
import tkinter as tk
from tkinter import font

# Generate Time-based OTP using variables
def code_generate():
    key = secret.strip()
    key = base64.b32decode(key.upper() + '=' * ((8 - len(key)) % 8))
    counter = struct.pack('>Q', int(time.time() / window))
    mac = hmac.new(key, counter, digest).digest()
    offset = mac[-1] & 0x0f
    binary = struct.unpack('>L', mac[offset:offset+4])[0] & 0x7fffffff
    return str(binary)[-length:].zfill(length)

# Calculate time remaining before the OTP changes
def code_time():
    current_time = int(time.time())
    remaining = window - (current_time % window)
    return f"Remaining time: {remaining}s"

# Updates the OTP and time display
def code_update():
    number_label.config(text=code_generate())
    text_label.config(text=code_time())
    root.after(1000, code_update)

# --------------------------------------------------

# Create main window
root = tk.Tk()
root.title("Authenticator")
root.geometry("250x150")
root.configure(bg=bcolor)

# Fonts
large_font = font.Font(family="Helvetica", size=36, weight="bold")
small_font = font.Font(family="Helvetica", size=12)

# Create a center frame to hold both labels
center_frame = tk.Frame(root, bg=bcolor)
center_frame.pack(expand=True)

# Number label
number_label = tk.Label(center_frame, text=code_generate(), font=large_font, bg=bcolor, fg=fcolor)
number_label.pack()

# Smaller text label
text_label = tk.Label(center_frame, text=code_time(), font=small_font, bg=bcolor, fg=fcolor)
text_label.pack()

# Start refreshing
code_update()

# Run app
root.mainloop()
