import os


from django.conf import settings
from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from my_api.serializers import PageSerializer
from my_api.models import Page
from text import line


class PageApiView(APIView):
   def get(self, request):
      queryset = Page.objects.all()
      serializer = PageSerializer(queryset, many=True)
      return Response(serializer.data)

   def post(self,request):
      serializer = PageSerializer(data=request.data)
      if(serializer.is_valid()):
         serializer.save()
         text1=''
         text2=''
         try:
            text1, text2 = line(os.path.join('.', settings.MEDIA_ROOT, 'uploads', 'image.jpg'))
         except:
            text1 = ''
            text2 = ''
         print(text1)
         print('\n')
         print(text2)
         return Response(text1+text2)

      return Response(serializer.errors)

