import requests
from decimal import Decimal

import pandas as pd
import datefinder

import settings

def getHtml(ticker, page):
  url = settings.baseUrl + ticker + settings.paths[page]
  print('Parsing', url)
  response = requests.get(url, headers = settings.headers)

  if response.status_code != 200:
    raise ValueError('Invalid response. Code', response.status_code)
  
  return response.text

def checkRunTime():
  marketInfo = getJson(None, 'marketInfo')
  marketIndicator = marketInfo['data']['marketIndicator']
  marketClosingTime = marketInfo['data']['marketClosingTime'].split(' ', 3)[3]
  preMarketOpeningTime = marketInfo['data']['preMarketOpeningTime'].split(' ', 3)[3]
  marketCountDown = marketInfo['data']['marketCountDown']

  if (marketIndicator == 'Market Open' or marketIndicator == 'Pre Market'):
    message = (
      f'This tool can only be used between {marketClosingTime} (market closes) and {preMarketOpeningTime} (pre-market opens).\n'
      f'Current market status: {marketIndicator}.\n'
    )
    print(message)
    quit()

def getJson(ticker, section):
  url = settings.url[section].format(ticker) if ticker != None else settings.url[section]
  response = requests.get(url, headers = settings.headers)
  return response.json()

def getXml(ticker):
  url = 'https://content1.edgar-online.com/cfeed/ext/charts.dll?81-0-0-0-0-008002000-03NA000000AAPL=&SF:1000-FREQ=1-STOK=2i/5uHsFKIIpf710h9a8S0HnloiLj9/4dlOVKhthoYbcBfXu0Bb6lD4669HCBkxl-1624946537954'
  h = {
    'Host': 'content1.edgar-online.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://content1.edgar-online.com/chartiq/edgr/edgar-chartiq.html'
  }
  
  response = requests.get(url, headers=h)
  print(response.text)

def parseNumber(string):
  table = str.maketrans({
    ',': '',
    '$': ''
  })
  return Decimal(string.translate(table))

def parseDate(string):
  for match in datefinder.find_dates(string):
    return match.date()

def getTopGainers():
  marketMovers = getJson(None, 'marketMovers')
  dataAsOf = marketMovers['data']['STOCKS']['MostAdvanced']['dataAsOf']
  topGainers = marketMovers['data']['STOCKS']['MostAdvanced']['table']['rows']
  return pd.DataFrame.from_dict(topGainers), dataAsOf

def scrape(ticker):
  timePreMktOpen = '5:30:00'
  timePreMktClose = '9:29:59'
  timeMktOpen = '9:30:00'
  timeMktClose = '16:00:00'

  stockInfo = getJson(ticker, 'stockInfo')
  summary = getJson(ticker, 'summary')
  preMarket = getJson(ticker, 'preMarket')
  realTime = getJson(ticker, 'realTime')
  summaryChart = getJson(ticker, 'summaryChart')

  # real time chart only gives closing price of candle

  df = pd.DataFrame.from_dict(realTime['data']['chart'])
  df = pd.DataFrame.from_records(df['z'])
  df.drop('prevCls', axis=1, inplace=True)
  # df = df.iloc[::-1].reset_index(drop=True)
  df['time'] = pd.to_datetime(df['time'])
  df['shares'] = df['shares'].apply(parseNumber)
  df['price'] = df['price'].apply(parseNumber)
  df_pre = df[df['time'].between(timePreMktOpen, timePreMktClose)]
  df_day = df[df['time'].between(timeMktOpen, timeMktClose)]

  date = parseDate(stockInfo['data']['primaryData']['lastTradeTimestamp'])

  sector = summary['data']['summaryData']['Sector']['value']
  
  index = summary['data']['summaryData']['Exchange']['value']
  
  mktCap = parseNumber(stockInfo['data']['keyStats']['MarketCap']['value'])
  
  dailyVol = parseNumber(summary['data']['summaryData']['ShareVolume']['value'])
  
  prevDayClose = parseNumber(stockInfo['data']['keyStats']['PreviousClose']['value'])

  # price of candle just before 9:30:00/before num shares shoot up
  # open = parseNumber(stockInfo['data']['keyStats']['OpenPrice']['value'])
  open = df_day['price'].iloc[-1]

  openCandleVol = df_day['shares'].iloc[-1]
  
  dayHigh = parseNumber(summary['data']['summaryData']['TodayHighLow']['value'].split('/')[0])
  # dayHigh = Decimal(realTime['data']['chartPrcMax'])
  # dayHigh = df_day['price'].max()
  
  timeDayHigh = df_day[df_day['price'] == dayHigh]['time'].values[0]
  
  dayLow = parseNumber(summary['data']['summaryData']['TodayHighLow']['value'].split('/')[1])
  # dayLow = Decimal(realTime['data']['chartPrcMin'])
  # dayLow = df_day['price'].min()
  
  dayLowAfterDayHigh = df_day[df_day['time'].between(timeDayHigh, timeMktClose)]['price'].min()
  
  timeDayLowAfterDayHigh = df_day[df_day['price'] == dayLowAfterDayHigh]['time'].values[0]
  
  close = parseNumber(stockInfo['data']['primaryData']['lastSalePrice'])
  
  sharesOutstanding = mktCap / close
  
  volToDayHigh = df[df['time'].between(timePreMktOpen, timeDayHigh)]['shares'].sum()
  
  highVolBeforeDayHigh = df_day[df_day['time'].between(timeMktOpen, timeDayHigh)]['shares'].max()
  
  # preMktVol = parseNumber(preMarket['data']['infoTable']['rows'][0]['volume'])
  preMktVol = df_pre['shares'].sum()
  
  # preMktHigh = parseNumber(preMarket['data']['infoTable']['rows'][0]['highPrice'].split(' ')[0])
  preMktHigh = df_pre['price'].max()
  
  timePreMktHigh = df_pre[df_pre['price'] == preMktHigh]['time'].values[0]
  preMktLowAfterHigh = df_pre[df_pre['time'].between(timePreMktHigh, timePreMktClose)]['price'].min()

  return {
    'Ticker': ticker.upper(),
    'Date': date,
    'Sector': sector,
    'Index': index,
    'Shares Outstanding': sharesOutstanding,
    'Market Cap': mktCap,
    'Daily Volume': dailyVol,
    'Prev Day Close': prevDayClose,
    'Open': open,
    'Open Candle Vol': openCandleVol,
    'Day High': dayHigh,
    'Time of Day High': timeDayHigh,
    'Day Low': dayLow,
    'Day Low After Day High': dayLowAfterDayHigh,
    'Time of Day Low After Day High': timeDayLowAfterDayHigh,
    'Close': close,
    'Pre-market High': preMktHigh,
    'Pre-market Low After High': preMktLowAfterHigh,
    'Pre-market Vol': preMktVol,
    'Vol to Day High': volToDayHigh,
    'High Vol Before Day High': highVolBeforeDayHigh
  }

def main():
  checkRunTime()

  # topGainers, dataAsOf = getTopGainers()
  # print(f'Today\'s NASDAQ Top Gainers\n{dataAsOf}\n{topGainers}')
  # print('Select tickers to scrape using indexes of the top gainers table. Separate indexes by space. Ex: 0 2 3')
  # indexes = [int(i) for i in input().split(' ')]
  # tickers = topGainers['symbol'][indexes].tolist()
  # print(f'Scraping: {tickers}\n')

  print('Enter tickers, separated by space. Example: aapl tsla')
  tickers = input().split(' ')

  for ticker in tickers:
    for key, value in scrape(ticker).items():
      print(key, '=', f'{value:.5f}' if type(value) == Decimal else value)

if __name__ == "__main__":
  main()



