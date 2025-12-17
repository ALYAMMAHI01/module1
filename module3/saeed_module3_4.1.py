# module3/saeed_module3_4.1.py
# This script fetches a person's data from a REST API, appends a random number to the phone number,
# and prints the name along with the modified phone number.
# Requirements: requests library
# To install requests, run: pip install requests
# Usage: python module3/saeed_module3_4.1.py

import requests
import random

# Assuming the API is running on localhost:8000
response = requests.get("http://localhost:8000/person")
if response.status_code == 200:
    person = response.json()
    if person:
        random_num = random.randint(1000, 9999)
        modified_phone = f"{person['phone']}{random_num}"
        print(f"Name: {person['name']}")
        print(f"Original Phone: {person['phone']}")
        print(f"Modified Phone: {modified_phone}")
    else:
        print("No person data found")
else:
    print(f"Error: {response.status_code}")