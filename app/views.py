from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from app.forms import *
from app.models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


def registration(request):
    ufo=UserForm()
    pfo=ProfileForm()
    d={'ufo':ufo,'pfo':pfo}
    return render(request,'registration.html',d)
    if request.method=='POST' and request.FILES:
        ufd=UserForm(request.POST)
        pfd=ProfileForm(request.POST,request.FILES)
        if ufo.is_valid() and pfo.is_valid():
            MUFDO=ufo.save(commit=False)
            pw=ufo.cleaned_data['password']
            MUFDO.set_password(pw)
            MUFDO.save()

            MPFDO=pfo.save(commit=False)
            MPFDO.username=MUFDO
            MPFDO.save()

            send_mail(registration,
                'congratulations on your registration ,your registration is registered',
                'hemanthnh837@gmail.com',
                [MUFDO.email],
                fail_silently=False,)
            return HttpResponse('registartion is successfulll')
        else:
            return HttpResponse('invalid')
    return render(request,'registration.html',d)


def homepage(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'homepage.html',d)
    return render(request,'homepage.html')

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('homepage'))
        else:
            return HttpResponse("Invalid Login Details")
    return render(request,'user_login.html')

@login_required
def profile_display(request):
    un=request.session.get('username')
    UO=User.objects.get(username=un)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}

    return render(request,'profile_display.html',d)

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('homepage'))

@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Password changed Successfully')
    return render(request,'change_password.html')



def reset_password(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('reset is done')
        else:
            return HttpResponse('U r Username is not in our DataBase')

    return render(request,'reset_password.html')