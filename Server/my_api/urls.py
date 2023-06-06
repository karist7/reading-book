from django.urls import include, path
from rest_framework import routers
from my_api.views import  PageApiView

urlpatterns = [
   path('page/', PageApiView.as_view()),
]