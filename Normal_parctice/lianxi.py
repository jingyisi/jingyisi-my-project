import requests

# 删掉后面重复的部分
url = 'https://jingyisi.github.io/'

headers = {
    'User-Agent': 'Mozilla/5.0 ...' # 你的 headers 保持不变
}

response = requests.get(url, headers=headers)
print(response.text) 