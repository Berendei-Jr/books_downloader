import requests
import os
import magic
from bs4 import BeautifulSoup
from urllib.parse import urlencode

yandex_base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
 
base = "http://retrolib.narod.ru/"
#print("Окончание ссылки (html/book...): ")
input = 'html/book_gg1.html'

r = requests.get(base + input)

html = BeautifulSoup(r.text, 'lxml')
#print(html)
table = html.find_all('table')[5]

path = "Books"

if (not os.path.exists(path)):
    os.mkdir(path)

for row in table.find_all('tr'):
    a = row.find_all('a', href = True)
    if (len(a) > 0):
        name = row.b.text
        if (name != '[1]'):
            url = a[0]['href']
            if (url[0] == '.'):
                end_url = url[3:]
                url = base + end_url

            if (url.startswith('http://retrolib.narod.ru')):
                f = open('Books/' + name + url[url.rfind('.'):], "wb")
                #print("URL:", url)
                ufr = requests.get(url)
                f.write(ufr.content)
                f.close()
            else:
                final_url = yandex_base_url + urlencode(dict(public_key=url))
                response = requests.get(final_url)
                download_url = response.json()['href']
                
                f = open('Books/tmp', "wb")
                print("Download started/...")
                download_response = requests.get(download_url)
                f.write(download_response.content)
                f.close()
                mime = magic.Magic(mime=True)
                mime = magic.Magic(mime=True)
                res = mime.from_file('Books/tmp')
                if (res == 'application/pdf'):
                    os.rename('Books/tmp', 'Books/' + name + '.pdf')
                else:
                    os.rename('Books/tmp', 'Books/' + name + '.djvu')
    