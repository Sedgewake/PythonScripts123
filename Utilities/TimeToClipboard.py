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
        date_part = now.strftime("%Y.%m.%d")  # YYYY.MM.DD
        formatted_datetime = f"{date_part} {time_part}" # Combine time and date
    else:
        date_part = now.strftime("%d.%m.%Y")  # YYYY.DD.MM
        formatted_datetime = f"{time_part} {date_part}" # Combine time and date

    
    # Combine time and date
    
    # Copy to clipboard
    pyperclip.copy(formatted_datetime)
    print(f"Copied to clipboard: {formatted_datetime}")

# Example usage:
Western = True  # Change this to False if you want YYYY.MM.DD format
copy_datetime_to_clipboard(Western)