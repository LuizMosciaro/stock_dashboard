import requests

def get_quote(ticker, range_, interval, fundamentals, dividends):
    #https://brapi.dev/docs
    url = f'https://brapi.dev/api/quote/{ticker}?range={range_}&interval={interval}&fundamental={fundamentals}&dividends={dividends}'
    header = {'accept': 'application/json'}
    payload = ''
    response = requests.get(url=url, headers=header, data=payload)
    resultados = response.json()
    return resultados

def get_historic_prices(symbol):
    alphaavantage_api = '5360KM6F1W76V4V8'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}.SAO&apikey={alphaavantage_api}'
    r = requests.get(url)
    data_json = r.json()
    
    labels = [] #Dias
    data = [] #Preco
    for key,value in data_json["Time Series (Daily)"].items():
        labels.append(key)
        data.append(value['1. open'])
    
    context = {
        'labels':list(reversed(labels)),
        'data':list(reversed(data))
    }
    return context