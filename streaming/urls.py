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
    # this url is for archive showing :
    path('archive/', views.showArchive),

    # these urls are for operating on users table
    path('register/', views.registerNewUser),
    path('login/', views.loginUsers),
    path('logout/', views.logOut),

    # conductor :
    path('conductor/', views.showConductor),
    path('conductor/addNewItem/', views.addNewItemToConductor),  # needs @admin access
    path('conductor/editThisItem/', views.editThisItem),  # needs @admin access
    path('conductor/deleteThisItem/', views.deleteThisItem),  # needs @admin access

    # live :
    path('live/', views.showLive),
    path('live/changeurl/', views.changeLiveUrl),  # needs @admin access














    # ///////////////////////////////////////////////
    path('conductor/fakeit/', views.insertfake)

]
