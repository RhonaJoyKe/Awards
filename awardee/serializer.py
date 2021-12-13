from rest_framework import serializers
from .models import Project,Profile
class MerchSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoringaMerch
        fields = ('name', 'description', 'price')
