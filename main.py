import requests
from bs4 import BeautifulSoup

ip = requests.get('http://www.trackip.net/ip?json')
soup = BeautifulSoup(ip.text, 'html.parser')

ip_info = soup.find_all('span', class_='ip-info-entry__value')

print()
