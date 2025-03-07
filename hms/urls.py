"""hms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from unicodedata import name
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from hostel.views import *

admin.site.site_header = 'Hostel Management System'
admin.site.index_title = 'Hostel Management System'
admin.site.site_title = 'Hostel Management System'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard, name='dashboard'),
    path('dashboard/', dashboard, name='dashboard'),
    path('newboarder', newboarder, name='newboarder'),
    path('boarders/', allboardersinformation, name='allboardersinformation'),
    path('boarder/view/<int:id>', viewboarder, name='viewboarder'),
    path('boarder/update/<str:id>', updateboarder, name='updateboarder'),
    path('boarder/delete/<str:id>', deleteboarder, name='deleteboarder'),
    path('roomtype/', roomtype, name='roomtype'),
    path('roomtype/update/<str:id>', updateroomtype, name='updateroomtype'),
    path('roomtype/delete/<str:id>', deleteroomtype, name='deleteroomtype'),
    path('room/', room, name='room'),
    path('room/update/<str:id>', updateroom, name='updateroom'),
    path('room/delete/<str:id>', deleteroom, name='deleteroom'),
    path('bed/', bed, name='bed'),
    path('bed/update/<str:id>', updatebed, name='updatebed'),
    path('bed/delete/<str:id>', deletebed, name='deletebed'),
    path('feecollection/', feecollection, name='feecollection'),
    path('feedue/', feedue, name='feedue'),
    path('feetype/', feetype, name='feetype'),
    path('feetype/update/<str:id>', updatefeetype, name='updatefeetype'),
    path('feetype/delete/<str:id>', deletefeetype, name='deletefeetype'),
    path('feegroup/', feegroup, name='feegroup'),
    path('feegroup/update/<str:id>', updatefeegroup, name='updatefeegroup'),
    path('feegroup/delete/<str:id>', deletefeegroup, name='deletefeegroup'),
    path('collectfee/<str:id>', collectfee, name='collectfee'),
    path('collectfee/update/<str:id>', updatecollectfee, name='updatecollectfee'),
    path('collectfee/delete/<str:id>', deletecollectfee, name='deletecollectfee'),
    path('expensehead/', expensehead, name='expensehead'),
    path('update/expensehead/<str:id>', updateexpensehead, name='updateexpensehead'),
    path('expensehead/delete/<str:id>', deleteexpensehead, name='deleteexpensehead'),
    path('expense/', expense, name='expense'),
    path('expense/update/<str:id>', updateexpense, name='updateexpense'),
    path('expense/delete/<str:id>', deleteexpense, name='deleteexpense'),
    path('expense/search/', expensesearch, name='expensesearch'),
    path('incomehead/', incomehead, name='incomehead'),
    path('update/incomehead/<str:id>', updateincomehead, name='updateincomehead'),
    path('incomehead/delete/<str:id>', deleteincomehead, name='deleteincomehead'),
    path('income/', income, name='income'),
    path('income/update/<str:id>', updateincome, name='updateincome'),
    path('income/delete/<str:id>', deleteincome, name='deleteincome'),
    path('income/search/', incomesearch, name='incomesearch'),
    path('profit/search/', profitsearch, name='profitsearch'),
    path('leavenotice/', leavenotice, name='leavenotice'),
    path('leavenotice/update/<str:id>', updateleavenotice, name='updateleavenotice'),
    path('leavenotice/delete/<str:id>', deleteleavenotice, name='deleteleavenotice'),
    path('todolist/', todolist, name='todolist'),
    path('todolist/update/<str:id>', updatetodolist, name='updatetodolist'),
    path('todolist/delete/<str:id>', deletetodolist, name='deletetodolist'),
    path('todolistdashboard/delete/<str:id>', deletetodolistdashboard, name='deletetodolistdashboard'),
    path('login/', loginpage, name='loginpage'),
    path('logout/', logoutUser, name='logoutUser'),
    path('change_password', change_password, name='change_password'),
] + static( settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
