from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
import pandas as pd
from datetime import datetime
import os

url = "https://data.bs.ch/api/explore/v2.1/catalog/datasets/100088/records?limit=20"

headers = {
    'Accept':'application/json'
}

session = Session()
session.headers.update(headers)

try:
    response = session.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    all_rows = []

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    
    for parking in data['results']:
        total = parking.get('total')
        free = parking.get('free')

        if total is not None and free is not None:
            occupied = int(total) - int(free)
        else:
            occupied = None

        row = {
            'timestamp': current_time,
            'parking_name': parking.get('name'),
            'address': parking.get('address'),
            'total_spots': total,
            'free_spots': free,
            'occupied_spots': occupied,
            'parking_status':parking.get('status')
        }

        all_rows.append(row)

    df = pd.DataFrame(all_rows)

    cols_to_fix = ['total_spots', 'free_spots', 'occupied_spots']
    for col in cols_to_fix:
        df[col] = df[col].astype('Int64')
        
    file_name = 'parking_data.csv'

    if os.path.exists(file_name):
        df.to_csv(file_name, mode='a', header=False, index=False)
    else:
        df.to_csv(file_name, mode='w', header=True, index=False)

    print(f"Success! Saved {len(all_rows)} parking lots to {file_name}")



except (ConnectionError, Timeout, TooManyRedirects) as e:
    print(f"Network error occurred:{e}")
except Exception as e:
    print(f"An unexpected error occured:{e}")

