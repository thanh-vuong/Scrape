url = {
  'marketInfo': 'https://api.nasdaq.com/api/market-info',
  'companyInfo': 'https://api.nasdaq.com/api/company/{0}/company-profile',
  'summary': 'https://api.nasdaq.com/api/quote/{0}/summary?assetclass=stocks',
  'stockInfo': 'https://api.nasdaq.com/api/quote/{0}/info?assetclass=stocks',
  'preMarket': 'https://api.nasdaq.com/api/quote/{0}/extended-trading?assetclass=stocks&markettype=pre',
  'realTime': 'https://api.nasdaq.com/api/quote/{0}/chart?assetClass=stocks&charttype=real',
  'summaryChart': 'https://api.nasdaq.com/api/quote/{0}/chart?assetclass=stocks',
  'marketMovers': 'https://api.nasdaq.com/api/marketmovers?assetclass=stocks&exchange=n&exchangestatus=default'
}

headers = {
  'Host': 'api.nasdaq.com',
  # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
  'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
  'Accept': 'application/json, text/plain, */*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'Origin': 'https://www.nasdaq.com',
  'DNT': '1',
  'Connection': 'keep-alive',
  'Referer': 'https://www.nasdaq.com/',
  'Cache-Control': 'max-age=0',
  'TE': 'Trailers'
}

# headers = {
#   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
#   "Accept-Encoding":"gzip, deflate",
#   "Accept-Language":"en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7",
#   "Connection":"keep-alive",
#   "Host":"www.nasdaq.com",
#   "Referer":"http://www.nasdaq.com",
#   "Upgrade-Insecure-Requests":"1",
#   "User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36"
# }

baseUrl = 'https://www.nasdaq.com/market-activity/stocks/'

paths = {
  'summary': '',
  'premarket': '/pre-market',
  'charts': '/advanced-charting'
}

columns = [
  'Date',
  'Ticker',
  'Sector',
  'Index',
  'Setup',
  'Outstanding Shares (per last filing) mm',
  'Float (m)',
  'Market Cap (m)',
  'Daily Volume (mm)',
  'Prev. Close',
  'Open',
  'Open Candle Volume',
  'High (top tick)',
  'Time of Top Tick',
  'Low of Day',
  'Low After Top Tick',
  'Time of low Tick after Top Tick',
  'Close',
  'Premarket High',
  'Premarket Low (after top tick)',
  'Premarket Vol.(MM)',
  'Total Vol to Top Tick (MM)',
  'EV',
  'Highest Vol. Bar up to TopTick',
  'SSR?',
  'Notes'
]

urlTda = {
    'priceHistory': 'https://api.tdameritrade.com/v1/marketdata/{0}/pricehistory',
    'fundamental': 'https://api.tdameritrade.com/v1/instruments',
}