from .models import Estimate
import requests
import json
import re


def get_estimates(ticker):
  """ Get estimates and create db entry """
  headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) (KHTML, like Gecko) Chrome/102.0.5005.63'}
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/analysis?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]
  f = [t for t in data["QuoteSummaryStore"]["earningsTrend"]["trend"] if t["period"] in ['0y','+1y']]
  num_analysts = f[0]['earningsEstimate']['numberOfAnalysts']['fmt']
  fwd_eps = f[0]['earningsEstimate']['avg']['fmt']
  fwd_rev = f[0]['revenueEstimate']['avg']['raw'] / 1e9
  fwd_rev_g = f[0]['revenueEstimate']['growth']['raw']
  fwd2_eps = f[1]['earningsEstimate']['avg']['fmt']
  fwd2_rev = f[1]['revenueEstimate']['avg']['raw'] / 1e9
  fwd2_rev_g = f[1]['revenueEstimate']['growth']['raw']

  # url for is, bs, cf -but not all items, e.g. q dil shrs or net debt
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/financials?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]
  # IS, CF items for prev 4 fy and IS for TTM
  date1 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][-1]['asOfDate'].replace('-','')
  rev1 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][-1]['reportedValue']['raw'] / 1e9
  eps1 = data["QuoteTimeSeriesStore"]['timeSeries']['annualDilutedEPS'][-1]['reportedValue']['raw']
  cfo1 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][0]['totalCashFromOperatingActivities']['raw'] / 1e9

  date2 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][2]['asOfDate'].replace('-','')
  rev2 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][2]['reportedValue']['raw'] / 1e9
  eps2 = data["QuoteTimeSeriesStore"]['timeSeries']['annualDilutedEPS'][2]['reportedValue']['raw']
  cfo2 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][1]['totalCashFromOperatingActivities']['raw'] / 1e9

  date3 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][1]['asOfDate'].replace('-','')
  rev3 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][1]['reportedValue']['raw'] / 1e9
  eps3 = data["QuoteTimeSeriesStore"]['timeSeries']['annualDilutedEPS'][1]['reportedValue']['raw']
  cfo3 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][2]['totalCashFromOperatingActivities']['raw'] / 1e9

  date4 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][0]['asOfDate'].replace('-','')
  rev4 = data["QuoteTimeSeriesStore"]['timeSeries']['annualTotalRevenue'][0]['reportedValue']['raw'] / 1e9
  eps4 = data["QuoteTimeSeriesStore"]['timeSeries']['annualDilutedEPS'][0]['reportedValue']['raw']
  cfo4 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][3]['totalCashFromOperatingActivities']['raw'] / 1e9
  
  trail_rev = data["QuoteTimeSeriesStore"]['timeSeries']['trailingTotalRevenue'][0]['reportedValue']['raw'] / 1e9
  trail_date = data["QuoteTimeSeriesStore"]['timeSeries']['trailingTotalRevenue'][0]['asOfDate'].replace('-','')

  if len(data["QuoteTimeSeriesStore"]['timeSeries']['annualNormalizedEBITDA']) == 4:
    ebitda1 = data["QuoteTimeSeriesStore"]['timeSeries']['annualNormalizedEBITDA'][-1]['reportedValue']['raw'] / 1e9
    capex1 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][0]['capitalExpenditures']['raw'] / -1e9
    ebitda2 = data["QuoteTimeSeriesStore"]['timeSeries']['annualNormalizedEBITDA'][2]['reportedValue']['raw'] / 1e9
    capex2 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][1]['capitalExpenditures']['raw'] / -1e9
    ebitda3 = data["QuoteTimeSeriesStore"]['timeSeries']['annualNormalizedEBITDA'][1]['reportedValue']['raw'] / 1e9
    capex3 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][2]['capitalExpenditures']['raw'] / -1e9
    ebitda4 = data["QuoteTimeSeriesStore"]['timeSeries']['annualNormalizedEBITDA'][0]['reportedValue']['raw'] / 1e9
    capex4 = data["QuoteSummaryStore"]['cashflowStatementHistory']['cashflowStatements'][3]['capitalExpenditures']['raw'] / -1e9
    trail_ebitda = data["QuoteTimeSeriesStore"]['timeSeries']['trailingNormalizedEBITDA'][0]['reportedValue']['raw'] / 1e9
  else:
    ebitda4 = ebitda3 = ebitda2 = ebitda1 = trail_ebitda = None
    capex4 = capex3 = capex2 = capex1 = None

  # url for trailing CF items
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/cash-flow?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]['QuoteTimeSeriesStore']['timeSeries']

  trail_capex = None
  if data['trailingCapitalExpenditure']:
    trail_capex = data['trailingCapitalExpenditure'][0]['reportedValue']['raw'] / -1e9 # list w 1 obj
  trail_cfo = data['trailingOperatingCashFlow'][0]['reportedValue']['raw'] / 1e9 # list w 1 obj

  # url for netDebt
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/balance-sheet?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]["QuoteTimeSeriesStore"]['timeSeries']['annualNetDebt']
  ndebt1 = ndebt2 = ndebt3 = ndebt4 = None
  if len(data) == 4:
    ndebt1 = data[3]['reportedValue']['raw'] / 1e9 if data[3] else None
    ndebt2 = data[2]['reportedValue']['raw'] / 1e9 if data[2] else None
    ndebt3 = data[1]['reportedValue']['raw'] / 1e9 if data[1] else None
    ndebt4 = data[0]['reportedValue']['raw'] / 1e9 if data[0] else None

  # url for industry and sector
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/profile?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]['QuoteSummaryStore']['assetProfile']
  sector = data['sector'] # invesment, e.g. WMT = consumer defensive
  industry = data['industry'] # E.g. WMT = Discount Stores

  # url for shrs outstanding
  url = 'https://finance.yahoo.com/quote/'+ ticker + '/key-statistics?p=' + ticker
  page = requests.get(url, headers=headers, timeout=5)
  data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))["context"]["dispatcher"]["stores"]['QuoteSummaryStore']['defaultKeyStatistics']
  shrs_out = data['sharesOutstanding']['raw'] / 1e9

  Estimate.objects.create(symbol=ticker, num_analysts=num_analysts, 
    fwd_eps=fwd_eps, fwd2_eps=fwd2_eps, fwd_rev=fwd_rev, fwd2_rev=fwd2_rev, 
    fwd_rev_g=fwd_rev_g, fwd2_rev_g=fwd2_rev_g, 
    date1=date1, date2=date2, date3=date3, date4=date4, 
    rev1=rev1, rev2=rev2, rev3=rev3, rev4=rev4, 
    eps1=eps1, eps2=eps2, eps3=eps3, eps4=eps4, 
    ebitda1=ebitda1, ebitda2=ebitda2, ebitda3=ebitda3, ebitda4=ebitda4, 
    capex1=capex1, capex2=capex2, capex3=capex3, capex4=capex4, 
    cfo1=cfo1, cfo2=cfo2, cfo3=cfo3, cfo4=cfo4, 
    trail_rev=trail_rev, trail_date=trail_date, trail_ebitda=trail_ebitda, 
    trail_capex=trail_capex, trail_cfo=trail_cfo, 
    ndebt1=ndebt1, ndebt2=ndebt2, ndebt3=ndebt3, ndebt4=ndebt4, 
    sector=sector, industry=industry, shrs_out=shrs_out)
