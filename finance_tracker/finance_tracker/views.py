from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.models import User
from django.contrib import messages
from django.views.decorators.http import require_POST
def get_home(request):
    return render(request,"index.html")


def register(request):

    if request.method=='POST':
        
        username=request.POST['username']
        password=request.POST['password']
        email=request.POST['email']

        user=User.objects.create_user(username=username,email=email,password=password)
        login(request,user)
        return redirect('dashboard')
    return render(request,'register.html')

def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect("dashboard")
    
        else:
            messages.error(request, "Invalid username or password")


    return render(request,"login.html")



@require_POST
def logout_view(request):
    logout(request)
    return redirect('signin')
    