# pip install pyperclip
import pyperclip
from datetime import datetime

def copy_datetime_to_clipboard(western=True):
    # Get current date and time
    now = datetime.now()
    
    # Format the time part (HH:mm)
    time_part = now.strftime("%H:%M")
    
    # Format the date part based on the 'western' flag
    if western:
        date_part = now.strftime("%Y.%d.%m")  # YYYY.DD.MM
    else:
        date_part = now.strftime("%Y.%m.%d")  # YYYY.MM.DD
    
    # Combine time and date
    formatted_datetime = f"{time_part} {date_part}"
    
    # Copy to clipboard
    pyperclip.copy(formatted_datetime)
    print(f"Copied to clipboard: {formatted_datetime}")

# Example usage:
Western = True  # Change this to False if you want YYYY.MM.DD format
copy_datetime_to_clipboard(Western)