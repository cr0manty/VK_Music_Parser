import requests
from bs4 import BeautifulSoup
from .local import LOGIN, PASSWORD

s = requests.Session()

auth_html = s.get('http://vk.com')
auth_bs = BeautifulSoup(auth_html.content, 'html.parser')
csrf_token = auth_bs.select('form')[0].attrs['action'].split('&')

ip_h = csrf_token[2].split('=')[1]
lg_h = csrf_token[3].split('=')[1]

playload = {
    'act': 'login',
    'role': 'al_frame',
    '_origin': 'https://vk.com',
    'ip_h': ip_h,
    'lg_h': lg_h,
    'email': LOGIN,
    'pass': PASSWORD
}

answ = s.post('https://login.vk.com/?act=login', data=playload)
audio_page = s.get('https://vk.com/audio')
test = BeautifulSoup(audio_page.text, 'html.parser')
audio_list_html = test.find_all('div', class_='audio_item')

print('1')
