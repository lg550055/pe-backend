from rest_framework import generics
from .models import Estimate
from .serializers import EstimateSerializer


class EstimateList(generics.ListCreateAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer

class EstimateDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer

class EstimateStock(generics.ListAPIView):
  serializer_class = EstimateSerializer
  
  def get_queryset(self):
    queryset = Estimate.objects.all()
    ticker = self.request.query_params.get('ticker')
    if ticker is not None:
      queryset = queryset.filter(symbol=ticker)
      if not queryset:
        locObj = {
            # symbol: ticker, num_analysts: 0, fwd_eps: 0, fwd2_eps: 0, fwd_rev: 0, fwd2_rev: 0, fwd_rev_g: 0, fwd2_rev_g: 0
        }
        Estimate.objects.create(symbol=ticker, num_analysts=0, fwd_eps=0, fwd2_eps=0, fwd_rev=0, fwd2_rev=0, fwd_rev_g=0, fwd2_rev_g=0)
        queryset = queryset.filter(symbol=ticker)
    return queryset
