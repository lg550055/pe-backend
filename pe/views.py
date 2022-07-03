from rest_framework import generics
from .models import Estimate
from .serializers import EstimateSerializer
import requests
import json
import re


class EstimateList(generics.ListAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer

class EstimateDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer

class EstimateStock(generics.ListCreateAPIView):
  serializer_class = EstimateSerializer
  
  def get_queryset(self):
    """ if stock in db, return estimates, otherwise get estimates, create entry and return estimates"""
    ticker = self.request.query_params.get('ticker')
    if ticker:
      queryset = Estimate.objects.filter(symbol=ticker)
      if not queryset:
        # get estimates and create db entry
        headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) (KHTML, like Gecko) Chrome/102.0.5005.63'}
        url = 'https://finance.yahoo.com/quote/'+ ticker + '/analysis?p=' + ticker
        page = requests.get(url, headers=headers, timeout=5)
        data = json.loads(re.search('root\.App\.main\s*=\s*(.*);', page.text).group(1))
        f = [t for t in data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["earningsTrend"]["trend"] if t["period"] in ['0y','+1y']]
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
        queryset = [Estimate.objects.get(symbol=ticker)]

    return queryset
