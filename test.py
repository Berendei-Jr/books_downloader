import requests
import os
import magic
from bs4 import BeautifulSoup
from urllib.parse import urlencode

yandex_base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
 
base = "http://retrolib.narod.ru/"
#print("Окончание ссылки (html/book...): ")
input = 'html/book_gg23.html'

r = requests.get(base + input)

html = BeautifulSoup(r.text, 'lxml')
#print(html)
table = (html.find_all('tr')[7]).find('b')
page_num = int(table.text[table.text.find('[') + 1 : table.text.find(']')])
print(page_num)
