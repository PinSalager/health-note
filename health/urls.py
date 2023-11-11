from django.urls import path, include
from . import views
from django.contrib import admin

#URL config
urlpatterns = [
    path('', views.home, name="home"),
    path('register_', views.registerPage, name="registerPage"),
    path('login', views.loginPage, name="loginPage"),
    path('logout', views.log_out, name="log_out"),
    path('profile', views.profile, name="profile"),
    path('workoutplan', views.startandstop, name="workoutplan"), #อย่าลืมเปลี่ยนคืนดด้วย
    path('fitness', views.fitness, name="fitness"),
    path('back', views.back, name="back"),

]
