from bs4 import BeautifulSoup
from dataclasses import dataclass
import matplotlib.pyplot as plt
import numpy as np
import requests
from datetime import datetime, timedelta
from collections import defaultdict
import csv

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

def convert_to_list_of_dicts(coin_dict):
    result = []
    for coin_name, coin_info_list in coin_dict.items():
        for coin_info in coin_info_list:
            coin_data = {
                'coin_name': coin_name,
                'value': coin_info.value,
                'date': coin_info.date
            }
            result.append(coin_data)
    return result

def dict_to_csv(coin_list_of_dicts):
    with open('data.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['coin_name', 'value', 'date'])
        writer.writeheader()
        writer.writerows(coin_list_of_dicts)

def csv_to_dict(coin_list_of_dicts):
    result_dict = {}
    for coin_data in coin_list_of_dicts:
        coin_name = coin_data['coin_name']
        value = coin_data['value']
        date = coin_data['date']

        if coin_name not in result_dict:
            result_dict[coin_name] = []

        result_dict[coin_name].append(Coin_info(value, date))
    return result_dict

def main():
    url = "https://www.coingecko.com"
    header = ({"User-Agent": "Mozilla/5.0 (iPad; CPU OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148"}) 

    coins = ['Bitcoin', 'Ethereum', 'Tether', 'Cardano', 'Solana']

main()