import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta


class VKParse:
    MAIN_URL = 'https://vk.com'
    LOGIN_URL = 'https://login.vk.com/?act=login'
    AUDIO_URL = 'https://vk.com/audio'
    AUTH_INFO = {}
    content = {}

    def __init__(self):
        self.session = requests.Session()

    def get_csrf(self):
        auth_html = self.session.get('http://vk.com')
        auth_parse = BeautifulSoup(auth_html.content, 'html.parser')
        action_url = auth_parse.select('form')[0].attrs['action'].split('&')
        return {
            'ip_h': action_url[2].split('=')[1],
            'lg_h': action_url[3].split('=')[1]
        }

    def create_payload(self, login, password):
        csrf = self.get_csrf()
        self.AUTH_INFO = {
            'login': login,
            'password': password,
            'time': datetime.now()
        }
        payload = {
            'act': 'login',
            'role': 'al_frame',
            '_origin': self.MAIN_URL,
            'email': login,
            'pass': password,
        }

        self.AUTH_INFO.update(csrf)
        payload.update(csrf)
        return payload

    def authorization(self, login, password):
        payload = self.create_payload(login, password)
        return self.session.post(self.LOGIN_URL, data=payload).status_code == 200

    def refresh_authorization(self):
        last_login = self.AUTH_INFO[-1]
        if last_login and last_login['time'] <= datetime.now() - timedelta(hours=1):
            self.session = requests.Session()
            self.authorization(last_login['login'], last_login['password'])

    def get_audio(self):
        audio_page = self.session.get(self.AUDIO_URL)
        if audio_page.status_code == 200:
            audio_soup = BeautifulSoup(audio_page.text, 'html.parser')
            audio_html = audio_soup.find_all('div', class_='audio_item')
            for i in audio_html:
                pass
