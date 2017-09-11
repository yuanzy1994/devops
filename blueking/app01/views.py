from django.shortcuts import render,HttpResponse

# Create your views here.

from app01 import models


def home(request):
    return HttpResponse('app01.home')

def page(request):
    return HttpResponse('app01.page')

def db_handle(request):
    # dic = {'username':'admin','password':'duiba.com','age':18}
    # #insert
    # models.UserInfo.objects.create(**dic)
    # #delete
    # models.UserInfo.objects.filter(username='yaunzy').delete()
    # #update
    # models.UserInfo.objects.all().update(username='fucksjc')
    # #select
    # models.UserInfo.objects.filter(age=20).first()


    # for line in user_list_obj:
    #     print line.username,line.age

    if request.method == "POST":
        print request.POST

    models.UserInfo.objects.create(username=request.POST.get('username'),
                                   password=request.POST.get('password'),
                                   age=request.POST.get('age')
                                   )

    user_list_obj = models.UserInfo.objects.all()

    #return HttpResponse('ok')
    return render(request,'t1.html',{'li': user_list_obj})

def date_time(request,year):
    print "date_time: %s",year
    return HttpResponse(year)
