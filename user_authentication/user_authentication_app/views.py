from django.shortcuts import render
from user_authentication_app.forms import UserForm, UserInfoForm
from user_authentication_app.models import UserInfo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# Create your views here.
def log_in(request):
    return render(request, 'user_authentication_app/login.html', context={})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('user_authentication_app:index'))
            else:
                return HttpResponse('Account is not active!!')
        else:
            HttpResponse('Login Details are Wrong!')
    else:
        return render(request, 'user_authentication_app/login.html', context={})
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_authentication_app:index'))

def index(request):
    diction = {'title':'home page'}
    if request.user.is_authenticated:
        current_user = request.user
        user_id = current_user.id
        user_basic_info = User.objects.get(pk=user_id)
        user_more_info = UserInfo.objects.get(user__pk=user_id)
        diction = {'user_basic_info':user_basic_info,'user_more_info':user_more_info}
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

            if 'profile_pics' in request.FILES:
                userinfo.profile_pic = request.FILES['profile_pics']

            userinfo.save()
            registered = True
    else:
        user_form = UserForm()
        userinfo_form = UserInfoForm()

    diction = {'user_form':user_form,'userinfo_form':userinfo_form, 'registered':registered}
    return render(request, 'user_authentication_app/register.html', context=diction)
