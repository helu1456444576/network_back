"""NAT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from web_Nat.views import *
from django.urls import path


urlpatterns = [
    # path(r'dynamic/',views.dynamic),
    # path(r'dynamic_test/',views.dynamic_test),
    # path(r'balance/',views.balance),
    # path(r'balance_test/',views.balance_test),
    # path(r'reuse/',views.reuse),
    # path(r'reuse_test/',views.reuse_test),
    # path(r'static/',views.static),
    # path(r'static_test/',views.static_test),
    # url(r'^static$',views.static),
    #  url(r'^getInfo/$', getInfo)
     url(r'^static1/$', static1),
     url(r'^static_test/$', static_test),
     url(r'^dynamic/$', dynamic),
     url(r'^dynamic_test/$', dynamic_test),
     url(r'^balance/$', balance),
     url(r'^balance_test/$', balance_test),
     url(r'^reuse/$', reuse),
     url(r'^reuse_test/$', reuse_test),
]
