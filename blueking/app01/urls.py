from django.conf.urls import url
from django.contrib import admin

from app01 import views



urlpatterns = [
    url(r'^home/', views.home),
    url(r'^page/', views.page),
]