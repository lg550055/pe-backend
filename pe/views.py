from rest_framework import generics
from .serializers import EstimateSerializer
from .utils import get_estimates
from .models import Estimate


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
        get_estimates(ticker)

        queryset = [Estimate.objects.get(symbol=ticker)]

    return queryset
