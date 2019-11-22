__author__ = "Vasile2k"

import requests

url = "https://www.olx.ro/oferte/q-corsair-k95/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36"
headers = {"User-Agent": user_agent}

response = requests.get(url, headers=headers)
print(response.content)
print("cal")
