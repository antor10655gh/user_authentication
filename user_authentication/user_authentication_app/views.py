from django.shortcuts import render

# Create your views here.
def index(request):
    diction = {'title':'home page'}
    return render(request, 'user_authentication_app/index.html', context=diction)
