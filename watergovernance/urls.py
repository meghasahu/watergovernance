"""watergovernance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from water import views

urlpatterns = [

    #Home Page
    path(r'',views.index),

    #about us and contact us
    path(r'aboutUs',views.aboutUs),
    path(r'contact',views.contact),

    # User Registeration

    path(r'signup',views.signup),
    path('signin_admin',views.signinadmin),
    path('signin_user',views.signin_user),


    # Admin Pages

    path(r'admin/',views.adminland),
    path('admin/modelResult',views.modelResult),
    path('admin/alerts',views.adminAlerts),
    path('admin/addAdmin',views.addAdmin),
    path('admin/userInfo',views.userInfo),
    path('admin/getModel',views.getModel),
    path('admin/uploadModel',views.uploadModel),
    path('admin/logout',views.admin_logout),


    path(r'admin/adminland',views.adminland),
    path('modelResult',views.modelResult),
    path('alerts',views.adminAlerts),
    path('addAdmin',views.addAdmin),
    path('userInfo',views.userInfo),
    path('getModel',views.getModel),
    path('uploadModel',views.uploadModel),
    path('logout',views.admin_logout),


    # User Pages

    path('user',views.userland),
]
