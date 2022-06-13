from dataclasses import fields
from rest_framework import serializers
from .models import Estimate


class EstimateSerializer(serializers.ModelSerializer):
  class Meta:
    fields = '__all__'
    model = Estimate
