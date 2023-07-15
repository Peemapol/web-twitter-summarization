import requests
import json
import pandas as pd

url = "https://apps.beam.cloud/wijm0"

# Function for calling BERTopic API
def get_bert(clean):
    payload = {"clean": clean, "methods": 'bert'}
    headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Authorization": "Basic N2VkMWE1ZjY5ZjhiYzZjYzdlMzE0ZWVmMDc2YTIyNGI6YmI0NTY5OTBkYzI2MzNlODc2NzMzZTRkZDRiNGIwMTQ=",
    "Connection": "keep-alive",
    "Content-Type": "application/json"
    }

    # print('Sending Request...')
    response = requests.request("POST", url, 
    headers=headers,
    data=json.dumps(payload)
    )

    return response.json()
