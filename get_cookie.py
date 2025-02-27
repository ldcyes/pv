import requests

# 定义目标网站的URL
url = "https://xueqiu.com/S/NVDA"

# 创建一个会话对象
session = requests.Session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
}
response = session.get(url, headers=headers)


# 获取响应头中的cookies
cookies = session.cookies

print(cookies)
# 打印cookies
for cookie in cookies:
    print(f"{cookie.name}: {cookie.value}")
