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
from django.contrib import admin
from django.conf.urls import include, url
from django.conf import settings
from django.conf.urls.static import static


from water import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    #Home Page
    url(r'^$',views.index,name="home"),

    url(r'^water/', include('water.urls')),
]
    #about us and contact us
    # url(r'^aboutUs/',views.aboutUs),
    # url(r'^contact/',views.contact),

    # # User Registeration

    # url(r'^signup/',views.signup),
    # url(r'^signin_admin/',views.signinadmin),
    # url(r'^signin_user/',views.signin_user),

    path('aboutUs',views.aboutUs),
    path('contact',views.contact),
    path('adminn',views.adminland),



    # # Admin Pages

    # url(r'^admin/',views.adminland),
    # url(r'^admin/modelResult/',views.modelResult),
    # url(r'^admin/alerts/',views.adminAlerts),
    # url(r'^admin/addAdmin/',views.addAdmin),
    # url(r'^admin/userInfo/',views.userInfo),
    # url(r'^admin/getModel/',views.getModel),
    # url(r'^admin/uploadModel/',views.uploadModel),
    # url(r'^admin/logout/',views.admin_logout),


    # # url(r'admin/adminland',views.adminland),
    # # url('modelResult',views.modelResult),
    # # url('alerts',views.adminAlerts),
    # # url('addAdmin',views.addAdmin),
    # # url('userInfo',views.userInfo),
    # # url('getModel',views.getModel),
    # # url('uploadModel',views.uploadModel),
    # # url('logout',views.admin_logout),


    # # User Pages

    # url(r'^user/',views.userland),

<<<<<<< HEAD

    path('user',views.userland),
]
=======
>>>>>>> 8a30fe8b23e9d6c789bfc35b2ef3499ceeb5451e
