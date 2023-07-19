from bs4 import BeautifulSoup
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime, timedelta
from collections import defaultdict

@dataclass
class Coin_info:
    value: float
    date: str

def initialize_soup(url, header):
    soup = None

    try:
        html = requests.get(url, headers=header).text
        soup = BeautifulSoup(html, 'lxml')

    except Exception as e:
        print('ERROR: Could not initialize soup object')
        print(e)

    return soup

def get_coin_info(soup, coins):
    coin = defaultdict(list)
    section = soup.find_all('tr')

    for i in range(len(section)):
        now = datetime.now()
        current_date = now.strftime("%Y-%m-%d")
        coin_name = section[i].find('span', class_='lg:tw-flex font-bold tw-items-center tw-justify-between')
        coin_value = section[i].find('span', class_='no-wrap')

        if(coin_name and coin_value and (coin_name.text.strip() in coins)):
            # Parsing and storing coin info
            parsed_value = float(coin_value.text.replace('$', '').replace(',', '').strip())
            coin[coin_name.text.strip()].append(Coin_info(parsed_value, current_date))

    return coin

def main():
    url = "https://www.coingecko.com"
    header = ({"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}) 

    coins = ['Bitcoin', 'Ethereum', 'Tether', 'Cardano', 'Solana']

    soup = initialize_soup(url, header)
    coin = get_coin_info(soup, coins)

    print(coin)

main()