from rest_framework import serializers
from my_api.models import Page

class PageSerializer(serializers.ModelSerializer):
   class Meta:
       model = Page
       fields = '__all__'

