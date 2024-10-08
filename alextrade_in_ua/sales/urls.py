from django.urls import path

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from . import views

urlpatterns = [
    path('', views.frontend),
    path('sales/', views.adminpage),
    path('sales/uploadsprtvr/', views.uploadsprtvr),
    path('sales/clearsprtvr/',  views.clearsprtvr),
    path('sales/uploadost/',    views.uploadost),
    path('sales/savenkl/',      views.savenkl),
    path('sales/delnkl/',       views.delnkl),
]
