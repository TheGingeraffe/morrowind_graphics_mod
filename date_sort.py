#!/usr/bin/env python3

# Definitely gonna put some tests in here

import datetime
import json

### Refactor this to use the actual API response instead of txt file
with open('api_response_2.txt', 'r') as file:
    api_response_string = file.read()

# Converts json to dictionary
py_api = json.loads(api_response_string)

# Stores most relevant dictionary from API response
file_updates = py_api['file_updates']

updated_times = []

for mod_dict in file_updates:
    uploaded_time = (mod_dict["uploaded_time"])
    date_match = uploaded_time.split("T")
    if date_match[0] not in updated_times:
        updated_times.append(date_match[0])

recent_date = (max(updated_times))

# Returns info about the most recently modified files

for mod_dict in file_updates:
    if recent_date in mod_dict["uploaded_time"]:
        print(mod_dict)