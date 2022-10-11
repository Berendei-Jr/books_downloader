import requests
r = requests.get("http://retrolib.narod.ru/books19.html")
html = r.text
print(html)