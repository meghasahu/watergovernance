"""watergovernance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, url
    2. Add a URL to urlpatterns:  url('blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name='water'


urlpatterns = [

    

    #about us and contact us
    url(r'aboutUs/$',views.aboutUs,name="aboutUs"),
    url(r'^contact/',views.contact,name="contactUs"),

    # User Registeration

    url(r'^signup/',views.signup+,name="signup"),
    url(r'^signin_admin/',views.signinadmin,name="signin_admin"),
    url(r'^signin_user/',views.signin_user,name="signin_user"),


    # Admin Pages

    url(r'^admin/',views.adminland,name="adminland"),
    url(r'^modelResult/',views.modelResult,name="modelResult"),
    url(r'^alerts/',views.adminAlerts,name="alerts"),
    url(r'^addAdmin/',views.addAdmin,name="addAdmin"),
    url(r'^userInfo/',views.userInfo,name="userInfo"),
    url(r'^getModel/',views.getModel,name="getModel"),
    url(r'^uploadModel/',views.uploadModel,name="uploadModel"),
    url(r'^adminlogout/',views.admin_logout,name="adminlogout"),


    # User Pages

    url(r'^user/',views.userland,name="user"),
    url(r'^userlogout/',views.user_logout,name="userlogout"),
    url(r'^useralerts/',views.user_alerts,name="useralerts"),
]
