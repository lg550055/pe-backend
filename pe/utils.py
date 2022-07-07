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

  Estimate.objects.create(symbol=ticker, num_analysts=num_analysts, 
    fwd_eps=fwd_eps, fwd2_eps=fwd2_eps, fwd_rev=fwd_rev, fwd2_rev=fwd2_rev, 
    fwd_rev_g=fwd_rev_g, fwd2_rev_g=fwd2_rev_g)
