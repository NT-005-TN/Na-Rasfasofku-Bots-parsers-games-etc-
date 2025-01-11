import webbrowser as wb
import urllib.parse
import urllib.request
import json
from bs4 import BeautifulSoup

task = 'Kafe Adress'

task = task.replace(' ', '+')
url = 'https://yandex.ru/search/?text={}&clid=2411726&lr=10747'.format(task)
#wb.open(url)

print(0)
parsed_url = urllib.parse.urlparse(url)
#print(parsed_url)

print(1)
response = urllib.request.urlopen(url)
#print(response.read())

print(2)
soup = BeautifulSoup(response.read(), 'html.parser')

print(soup)
print(soup.prettify())


#data = {'title': soup.title.text, 'links': []}
#for link in soup.find_all('a'):
 #   data['links'].append({'href': link.get('href'), 'text': link.text})

#print(json.dumps(data, indent=4))
