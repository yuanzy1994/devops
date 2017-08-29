from django.shortcuts import render,HttpResponse

# Create your views here.

from app01 import models


def home(request):
    return HttpResponse('app01.home')

def page(request):
    return HttpResponse('app01.page')

def db_handle(request):
    dic = {'username':'admin','password':'duiba.com','age':18}
    #insert
    models.UserInfo.objects.create(**dic)
    #delete
    models.UserInfo.objects.filter(username='yaunzy').delete()
    #update
    models.UserInfo.objects.all().update(username='fucksjc')
    #select
    models.UserInfo.objects.filter(age=20).first()

    return HttpResponse('ok')
