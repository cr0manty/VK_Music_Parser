import requests
import json

from bs4 import BeautifulSoup
from datetime import datetime, timedelta

from .models import Authorization
from .database import Database


class VKParse:
    MAIN_URL = 'https://vk.com'
    LOGIN_URL = 'https://login.vk.com/?act=login'
    AUDIO_URL = 'https://vk.com/audio'

    def __init__(self):
        self.db = Database()
        self.session = requests.Session()

    def check_location(self):
        ip_json = requests.get('http://www.trackip.net/ip?json')
        location = json.loads(ip_json.text)
        return location

    def get_csrf(self):
        auth_html = self.session.get(self.MAIN_URL)
        auth_parse = BeautifulSoup(auth_html.content, 'html.parser')
        action_url = auth_parse.select('form')[0].attrs['action'].split('&')
        return {
            'ip_h': action_url[2].split('=')[1],
            'lg_h': action_url[3].split('=')[1]
        }

    def create_payload(self, login, password):
        csrf = self.get_csrf()
        payload = {
            'act': 'login',
            'role': 'al_frame',
            '_origin': self.MAIN_URL,
            'email': login,
            'pass': password,
        }
        user = Authorization(
            login=login,
            password=password,
            ip_h=csrf['ip_h'],
            lg_h=csrf['lg_h']
        )
        payload.update(csrf)
        return payload, user

    def use_proxy(self):
        return True

    def authorization(self, login, password):
        user_location = self.check_location()
        used_proxy = self.use_proxy() if user_location['Country'] == 'UA' else 0

        payload, user = self.create_payload(login, password)
        user.use_proxy = used_proxy
        user.ip = user_location['IP']
        user.user_location = user_location['Country']
        user.save()

        return self.session.post(self.LOGIN_URL, data=payload).status_code == 200

    def refresh_authorization(self, login):
        last_auth = Authorization.objects(login=login).order_by('-auth_time')
        if last_auth and last_auth.auth_time <= datetime.now() - timedelta(hours=1):
            self.session = requests.Session()
            self.authorization(last_auth.login, last_auth.password)

    def get_audio(self):
        audio_page = self.session.get(self.AUDIO_URL)
        if audio_page.status_code == 200:
            audio_soup = BeautifulSoup(audio_page.text, 'html.parser')
            audio_html = audio_soup.find_all('div', class_='audio_item')
            for i in audio_html:
                pass
