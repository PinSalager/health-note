from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home(request):#ฟังค์ชันการหน้าหลัก
    return render(request, "health/index.html")

def registerPage(request): #ฟังค์ชันการ register

        # รับข้อมูลจาก register มาเป็น POST
        if request.method == "POST": 
            name = request.POST.get("name")
            username = request.POST.get("username")
            email = None
            password = request.POST.get("password")
            password_com = request.POST.get("com_pass")

            if User.objects.filter(username = username): #ถ้ามี username ซ้ำ
                 messages.error(request, "Username already exists")
                 return redirect('registerPage')

            if password != password_com: #password not same
                 messages.error(request, "Password didn't same")
                 return redirect('registerPage')
            #บันทำสร้าง user 
            myuser = User.objects.create_user(username, email, password)
            myuser.first_name = name
            myuser.save()

            messages.success(request, "Your Account has been created.")
            return redirect('loginPage')

        return render(request, "health/registerPage.html")

def loginPage(request): #ฟังค์ชันการ login
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            name = user.first_name
            return render(request, "health/index.html",{"name":name}) # edit this later
        else:
            messages.error(request, "Username or Password wrong")
            return redirect('loginPage')
    return render(request, "health/loginPage.html")

def log_out(request): #ฟังค์ชันการ logout
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return redirect('home')

def profile(request):
     return render(request, "health/profile.html")