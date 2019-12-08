from django.urls import path
from PyDownload import views

urlpatterns = [
    path('',views.urlcheck,name='urlcheck'),
    
]