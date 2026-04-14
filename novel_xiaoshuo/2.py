import requests
import random
import time
headers = {
        "user_agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36 Edg/145.0.0.0"
} 
for page in range(1,3):
    url = f'https://www.22biqu.com/biqu1/{page}.html'
    response = requests.get(url,headers = headers)
    print(response.text)
time.sleep(1)