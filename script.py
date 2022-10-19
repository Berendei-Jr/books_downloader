import requests
import os
import magic
from bs4 import BeautifulSoup
from urllib.parse import urlencode

yandex_base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
 
print("Название папки (по-английски):")
dir_name = input()
#dir_name = "Ener"
base = "http://retrolib.narod.ru/"
print("Окончание ссылки (после ...narod.ru/). Нужна ссылка на ПЕРВУЮ страницу:")
input_url = input()
#input_url = "book_s1.html"
print("Количество страниц:")
pages_num = int(input())
#pages_num = 6
tmp_url = base + input_url
if (pages_num > 1):
    index = tmp_url.find('1')

r = requests.get(tmp_url)

html = BeautifulSoup(r.text, 'lxml')

table = html.find_all('table')[5]

path = dir_name
mail_ru_path = 'Mail.ru ссылки (' + path + ')'

if (not os.path.exists(path)):
    os.mkdir(path)

if (not os.path.exists(mail_ru_path)):
    os.mkdir(mail_ru_path)

books_num = pages_num*20

counter = 1
book_counter = 0
while (True):
    #print("tmp_url: ", tmp_url)
    for row in table.find_all('tr'):
        a = row.find_all('a', href = True)
        if (len(a) == 1):
            row_name = row.b.text
            if (not row_name.startswith('[')):
               # print('\nROW\n', row)
                url = a[0]['href']

                book_counter += 1
                print('Прогресс: ', round(book_counter/books_num * 100), '%')
                if (url[0] == '.'):
                    end_url = url[3:]
                    url = base + end_url
                
                if (len(row_name) > 80):
                    row_name = row_name[:80]
                name = row_name.replace('/', '') 
                name = name.replace('"', '') 
                name = name.replace('.', '')

                flag = True
                i = 1
                while (flag):
                    if (os.path.exists(path + '/' + name + url[url.rfind('.'):]) or os.path.exists(path + '/' + name + '.pdf') or os.path.exists(path + '/' + name + '.djvu')):
                        name = name + '(' + str(i) + ')'
                        i += 1
                    else:
                        flag = False

                if (url.startswith('book')):
                    url = base + url
                if (url.startswith('http://clck.ru')):
                    continue    

                #print("Book: ", name, "; url: ", url)    
                if (url.startswith('http://retrolib.narod.ru')):
                    f = open(path + '/' + name + url[url.rfind('.'):], "wb")
                    #print("URL:", url)
                    ufr = requests.get(url)
                    f.write(ufr.content)
                    f.close()
                elif (url.startswith('https://cloud.mail.ru')):
                    f = open(mail_ru_path + '/' + name + '.txt', 'w')
                    f.write(url)
                    f.close()
                else:
                    final_url = yandex_base_url + urlencode(dict(public_key=url))
                    response = requests.get(final_url)
                    try:
                        download_url = response.json()['href']
                    except KeyError:
                        print('У книги ', name, ' битая ссылка: ', url)
                        continue
                    
                    f = open(path + '/tmp', "wb")
                    #print("Download started/...")
                    download_response = requests.get(download_url)
                    f.write(download_response.content)
                    f.close()
                    mime = magic.Magic(mime=True)
                    res = mime.from_file(path + '/tmp')
                    if (res == 'application/pdf'):
                        os.rename(path + '/tmp', path + '/' + name + '.pdf')
                    else:
                        os.rename(path + '/tmp', path + '/' + name + '.djvu')

    counter += 1
    if (counter == pages_num + 1):
        break
    tmp_url = tmp_url[:index] + str(counter) + '.html'
    #print ("new url:", tmp_url)
    r = requests.get(tmp_url)

    html = BeautifulSoup(r.text, 'lxml')
    table = html.find_all('table')[5]

print('\nЗавершено успешно!\nЧтобы закрыть это окно, нажмите любую кнопку')
input()
