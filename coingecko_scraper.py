from bs4 import BeautifulSoup
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class Point:
    value: float
    date: float

coin_info = defaultdict(list)

coins = ['Bitcoin', 'Ethereum', 'Tether', 'Cardano', 'Solana']
URL = "https://www.coingecko.com"
HEADERS = ({"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"})

try:
    html = requests.get(URL, headers=HEADERS).text
    soup = BeautifulSoup(html, 'lxml')

except Exception as e:
    print(e)

# Getting coin info (name, value, and date)
section = soup.find_all('tr')
for i in range(len(section)):
    now = datetime.now()
    current_date = now.strftime("%Y-%m-%d")
    coin_name = section[i].find('span', class_='lg:tw-flex font-bold tw-items-center tw-justify-between')
    coin_value = section[i].find('span', class_='no-wrap')

    if(coin_name and coin_value and (coin_name.text.strip() in coins)):
        # Parsing and storing coin info
        coin_value_parsed = float(coin_value.text.replace('$', '').replace(',', '').strip())
        coin_info[coin_name.text.strip()].append(Point(coin_value_parsed, current_date))


