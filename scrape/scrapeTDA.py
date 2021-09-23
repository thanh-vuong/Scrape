import requests
import pandas as pd
import json

import settings
import secret

def getPriceHistory(ticker):
  url = settings.urlTda['priceHistory'].format(ticker)
  params = {
    'apikey': secret.tdaApiKey,
    'periodType': 'day',
    'period': 1,
    'frequencyType': 'minute',
    'frequency': 1,
    'needExtendedHoursData': 'true'
  }
  return requests.get(url, params).json()

def getFundamental(ticker):
  url = settings.urlTda['fundamental']
  params = {
    'apikey': secret.tdaApiKey,
    'symbol': ticker,
    'projection': 'fundamental'
  }
  return requests.get(url, params).json()

def scrape(ticker):
  fundamental = getFundamental(ticker)[ticker]
  # print(json.dumps(fundamental, indent=2))

  timePreMktOpen = pd.to_datetime('5:30:00').time()
  timePreMktClose = pd.to_datetime('9:29:59').time()
  timeRegMktOpen = pd.to_datetime('9:30:00').time()
  timeRegMktClose = pd.to_datetime('16:00:00').time()

  priceHistory = pd.DataFrame.from_dict(getPriceHistory(ticker)['candles'])

  priceHistory['datetime'] = pd.to_datetime(priceHistory['datetime'], unit='ms', utc=True)
  priceHistory['datetime'] = priceHistory['datetime'].dt.tz_convert('US/Eastern')
  date = (priceHistory['datetime'][0].date()).strftime('%Y-%m-%d')

  priceHistory['time'] = priceHistory['datetime'].dt.time

  print(priceHistory)
  priceHistory = priceHistory.set_index('time')
  preMktHistory = priceHistory.loc[timePreMktOpen : timePreMktClose]
  regMktHistory = priceHistory.loc[timeRegMktOpen : timeRegMktClose]

  print(preMktHistory)
  print(regMktHistory)

  sector = ''
  index = fundamental['exchange']
  sharesOutstanding = fundamental['fundamental']['sharesOutstanding']
  float = fundamental['fundamental']['marketCapFloat']
  mktCap = fundamental['fundamental']['marketCap']
  dailyVol = int(priceHistory['volume'].sum())
  prevDayClose = ''
  open = '' # priceHistory['9:30:00']['open'] # crashing, KeyError
  openCandleVol = ''
  dayHigh = ''
  timeDayHigh = ''
  dayLow = ''
  dayLowAfterDayHigh = ''
  timeDayLowAfterDayHigh = ''
  close = ''
  preMktHigh = ''
  preMktLowAfterHigh = ''
  preMktVol = ''
  volToDayHigh = ''
  highVolBeforeDayHigh = ''

  return {
    'Ticker': ticker,
    'Date': date,
    'Index': index,
    'Setup': '',
    'Sector': sector,
    'Shares Outstanding': sharesOutstanding,
    'Float': float,
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
  print('Enter tickers, separated by space. Example: aapl tsla')
  tickers = input().upper().split(' ')
  
  # for testing only
  # tickers=['HOOD']

  for ticker in tickers:
    print(json.dumps(scrape(ticker), indent=2))

if __name__ == "__main__":
  main()