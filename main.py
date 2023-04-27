import requests

base = 'https://fapi.binance.com'
path = '/fapi/v1/premiumIndex'
url = base + path
min_price = 10000000
max_price = -1
min_price_BTC = 1000000
max_price_BTC = -1
tm_base = 0
flag = True

while True:
    r_ETH = requests.get(url, params={'symbol': 'ETHUSDT'})
    r_BTC = requests.get(url, params={'symbol': 'BTCUSDT'})
    if r_ETH.status_code == 200 and r_BTC.status_code == 200:
        price = float(r_ETH.json()['markPrice'])
        price_BTC = float(r_BTC.json()['markPrice'])
        tm = r_ETH.json()['time']
        if flag:
            min_price = 10000000
            max_price = -1
            tm_base = r_ETH.json()['time']
            flag = False
            continue

        if tm - tm_base >= 3600000:
            flag = True

        if price < min_price:
            min_price = price
        if price > max_price:
            max_price = price
        if price_BTC < min_price_BTC:
            min_price_BTC = price_BTC
        if price_BTC > max_price_BTC:
            max_price_BTC = price_BTC

        pr_ETH = round(((max_price / min_price) * 100 - 100), 3)
        pr_BTC = round(((max_price_BTC / min_price_BTC) * 100 - 100), 3)
        actual_change = pr_ETH - pr_BTC
        if actual_change >= 0.001:
            if price == min_price:
                print(f'Понизился курс ETHUSDT на - {actual_change}%')
                print(f'Цена в данный момент = {price}')
            else:
                print(f'Повысился курс ETHUSDT на {actual_change}%')
                print(f'Цена в данный момент = {price}')
            flag = True
    else:
        print('error')
        break
