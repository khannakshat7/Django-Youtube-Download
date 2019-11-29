from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    mydict = {'content':"Hello!! Demo text"}
    return render(request,'index.html',context=mydict)