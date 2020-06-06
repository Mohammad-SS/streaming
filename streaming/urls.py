"""streamingEsra URL Configuration

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
from django.contrib import admin
from django.urls import path, include
from streaming import views

urlpatterns = [
    # Archive Urls :
    path('archive/', views.showArchive),
    path('archive/addNewItem/', views.addNewItemToArchive),  # needs @admin access
    path('archive/editThisItem/', views.editThisArchiveItem),  # needs @admin access
    path('archive/deleteThisItem/', views.deleteThisArchiveItem),  # needs @admin access

    # Users Urls :
    path('user/register/', views.registerNewUser),
    path('user/login/', views.loginUsers),
    path('user/logout/', views.logOut),
    path('user/forgetPassword/' , views.forgetPassword),
    path('user/changePassword/', views.changePassword),
    # Conductor Urls :
    path('conductor/', views.showConductor),
    path('conductor/addNewItem/', views.addNewItemToConductor),  # needs @admin access
    path('conductor/editThisItem/', views.editThisConductorItem),  # needs @admin access
    path('conductor/deleteThisItem/', views.deleteThisConductorItem),  # needs @admin access

    # Live Urls :
    path('live/', views.showLive),
    path('live/changeurl/', views.changeLiveUrl),  # needs @admin access















    # ///////////////////////////////////////////////
    path('conductor/fakeit/', views.insertfake)

]
