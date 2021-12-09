from django.shortcuts import render
from user_authentication_app.forms import UserForm, UserInfoForm
from user_authentication_app.models import UserInfo
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def index(request):
    diction = {'title':'home page'}
    return render(request, 'user_authentication_app/index.html', context=diction)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        userinfo_form = UserInfoForm(data=request.POST)

        if user_form.is_valid() and userinfo_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            userinfo = userinfo_form.save(commit=False)
            userinfo.user = user

            if 'profile_pic' in request.FILES:
                userinfo.profile_pic = request.FILES['profile_pic']

            userinfo.save()
            registered = True
    else:
        user_form = UserForm()
        userinfo_form = UserInfoForm()

    diction = {'user_form':user_form,'userinfo_form':userinfo_form, 'registered':registered}
    return render(request, 'user_authentication_app/register.html', context=diction)

def log_in(request):
    diction = {'login':'Login Form'}
    return render(request, 'user_authentication_app/login.html', context=diction)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                log_in(request, user)
                print("Login Successfull!")
                return HttpResponseRedirect(reverse('user_authentication_app:index'))
            else:
                return HttpResponse('Account is not active!!')
        else:
            HttpResponse('Login Details are Wrong!')
    else:
        return render(request, 'user_authentication_app/login.html', context={})
