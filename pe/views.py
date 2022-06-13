from rest_framework import generics
from .models import Estimate
from .serializers import EstimateSerializer


class EstimateList(generics.ListCreateAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer

class EstimateDetail(generics.RetrieveUpdateDestroyAPIView):
  queryset = Estimate.objects.all()
  serializer_class = EstimateSerializer
