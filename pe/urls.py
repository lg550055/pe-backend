from django.urls import path
from .views import EstimateList, EstimateDetail


urlpatterns = [
  path('', EstimateList.as_view(), name='estimate_list'),
  path('<int:pk>/', EstimateDetail.as_view(), name='estimate_detail')
]
