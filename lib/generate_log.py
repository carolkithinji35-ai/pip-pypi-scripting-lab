from datetime import datetime
import os


def generate_log(data):
    # STEP 1: Validate input
    if not isinstance(data, list):
        raise ValueError("data must be a list")

    # STEP 2: Generate filename with today's date
    filename = f"log_{datetime.now().strftime('%Y%m%d')}.txt"

    # STEP 3: Write the log entries to a file
    with open(filename, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(f"{entry}\n")

    # STEP 4: Print confirmation and return filename
    print(f"Log file created: {filename}")
    return filename
