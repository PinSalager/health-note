from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import phonenumbers
from phonenumbers import geocoder
from opencage.geocoder import OpenCageGeocode
import time
import math

# Create your views here.

def home(request):#ฟังค์ชันการหน้าหลัก
    return render(request, "health/index.html")

def registerPage(request): #ฟังค์ชันการ register

        # รับข้อมูลจาก register มาเป็น POST
        if request.method == "POST": 
            name = request.POST.get("name")
            username = request.POST.get("username")
            phonenum = request.POST.get("phonenum")
            password = request.POST.get("password")
            password_com = request.POST.get("com_pass")

            if User.objects.filter(username = username): #ถ้ามี username ซ้ำ
                messages.error(request, "Username already exists")
                return redirect('registerPage')

            if password != password_com: #password not same
                messages.error(request, "Password didn't same")
                return redirect('registerPage')
            #บันทำสร้าง user 
            myuser = User.objects.create_user(username, phonenum, password)
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
@login_required(login_url="/login")

def profile(request):
    if request.method == "POST": 
        height = float(request.POST['height'])
        weight = float(request.POST['weight'])
        bmi = weight / (height / 100 * height / 100)
        if bmi <= 0:
            heal = "Error"
        elif bmi < 18.5:
            heal = "น้ำหนักน้อย"
        elif bmi > 18.5 and bmi < 23:
            heal = "สุขภาพปกติ"
        elif bmi >= 23:
            heal = "น้ำหนักเกิน"
        return render(request, "health/profile.html",{"bmi":int(round(bmi)), "heal":heal})
        
    return render(request, "health/profile.html",{"bmi":0, "heal":"รอการประมวลผล"})

def fitness(request):
    return render(request, "health/fitness.html")

def checkvar(rule):
    if rule == "False":
        return False
    if rule == "True":
        return True

def startandstop(request): #ฟังก์แปลงค่าในปุ่ม
    if request.method == "POST":
        global mycheck
        mycheck = None
        check = request.POST['check']
        if check == "False":
            mycheck = checkvar(check)
            return render(request, "health/workoutplan.html", {"check":False})
        elif check == "True":
            mycheck = checkvar(check)
            return render(request, "health/workoutplan.html", {"check":True})

    return render(request, "health/workoutplan.html",{"name":request.user.email})

def workoutplan(request): #เหลือปุ่ม เปิดปิด
    if request == 'POST':
        phonenum = request.user.email#เเก้อันนี้เป็นการเอาค่าจาก user phone nuber จาก email
        #สร้างตัวแปรเอาไว้หาความต่างของระยะทาง
        previous_lat, previous_lng = None, None
        rule = True
        start = mycheck
        phone_number = phonenum #เบอร์โทร
        distance = 0
        count = 0
        countforstop = 0
        while rule:
            if start == True:
                pep_number = phonenumbers.parse(phone_number)

                # Get location information
                location = geocoder.description_for_number(pep_number, "en")

                # Get geographic coordinates using OpenCageGeocode
                key = '7380084ddefb4271aa47fc93d93008c3'
                geocoder_instance = OpenCageGeocode(key)

                query = str(location)
                results = geocoder_instance.geocode(query)

                # รับและเก็บค่า ละติจูด และ ละจิจูด
                lat = results[0]['geometry']['lat']
                lng = results[0]['geometry']['lng']

                if previous_lat is not None and previous_lng is not None:
                    # Differences in coordinates
                    dlat = lat - previous_lat
                    dlng = lng - previous_lng

                    # Haversine formula
                    a = math.sin(dlat/2)**2 + math.cos(previous_lat) * math.cos(lat) * math.sin(dlng/2)**2
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

                    # Calculate the distance in meters
                    d = 6378.137 * c * 1000
                    distance += d
                    count += 1
                    cal = 13*count/60
                    previous_lat, previous_lng = lat, lng

                    time.sleep(1)  # เว้น 1 วิเพื่อให้ค่าเปลี่ยน
                    countforstop = 1
                    continue
            elif start == False and countforstop == 1:
                countforstop = 0
                distance = "Your distance is : " + str(round(distance, 2)) + " meter"
                cal = "calories you burn today :" + str(round(cal, 2)) + " cal"
                break
    return render(request, "health/workoutplan.html",(distance, cal))

def back(request):
    return render(request, "health/index.html")
