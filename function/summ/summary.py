import requests
import json

url = "https://apps.beam.cloud/8houu"

# Function for calling API
def summarise(inputs):
  payload = {"batch": inputs}
  headers = {
  "Accept": "*/*",
  "Accept-Encoding": "gzip, deflate",
  "Authorization": "Basic N2VkMWE1ZjY5ZjhiYzZjYzdlMzE0ZWVmMDc2YTIyNGI6YmI0NTY5OTBkYzI2MzNlODc2NzMzZTRkZDRiNGIwMTQ=",
  "Connection": "keep-alive",
  "Content-Type": "application/json"
  }

  response = requests.request("POST", url, 
  headers=headers,
  data=json.dumps(payload)
  )

  return response.json()