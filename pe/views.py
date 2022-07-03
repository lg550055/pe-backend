from rest_framework import generics
from .models import Estimate
from .serializers import EstimateSerializer


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
        locObj = {
            # symbol: ticker, num_analysts: 0, fwd_eps: 0, fwd2_eps: 0, fwd_rev: 0, fwd2_rev: 0, fwd_rev_g: 0, fwd2_rev_g: 0
        }
        Estimate.objects.create(symbol=ticker, num_analysts=0, fwd_eps=0, fwd2_eps=0, fwd_rev=0, fwd2_rev=0, fwd_rev_g=0, fwd2_rev_g=0)
        queryset = [Estimate.objects.get(symbol=ticker)]
    return queryset
