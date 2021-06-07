from rest_framework import serializers

from .models import *


class PlanSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Plan
        fields = ('name', 'amount')