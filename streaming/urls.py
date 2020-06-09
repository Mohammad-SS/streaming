from django.contrib import admin
from django.urls import path, include
from streaming import views

urlpatterns = [
    # Archive Urls :
    path('archive/showAll/', views.showArchive),
    path('archive/addNewItem/', views.addNewItemToArchive),  # needs @admin access
    path('archive/editItems/', views.editThisArchiveItem),  # needs @admin access
    path('archive/deleteItems/', views.deleteThisArchiveItem),  # needs @admin access

    # Users Urls :
    path('user/register/', views.registerNewUser),
    path('user/login/', views.loginUsers),
    path('user/logout/', views.logOut),
    path('user/forgetPassword/', views.forgetPassword),
    path('user/changePassword/', views.changePassword),
    path('user/editData/', views.changeUserDataByUser),
    path('user/deleteAccount/', views.deleteAccountByUser),
    path('user/getUserData/', views.getUserData),
    # Users for admin ! :
    path('user/getAllUsers/', views.getAllUsers),
    # path('user/admin/editdata/', views.changeUserDataByAdmin), # needs @admin access
    # path('user/admin/deleteaccount/', views.deleteAccountByAdmin), # needs @admin access

    # Conductor Urls :
    path('conductor/showAll/', views.showConductor),
    path('conductor/addNewItem/', views.addNewItemToConductor),  # needs @admin access
    path('conductor/editItems/', views.editThisConductorItem),  # needs @admin access
    path('conductor/deleteItems/', views.deleteThisConductorItem),  # needs @admin access

    # Live Urls :
    path('live/', views.showLive),
    path('live/changeurl/', views.changeLiveUrl),  # needs @admin access

    # ///////////////////////////////////////////////
    path('conductor/fakeit/', views.insertfake)

]
