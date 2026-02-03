from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request,'core/home.html')

def places(request):
    return render(request, 'places.html')

def plan(request):
    return render(request, 'plan.html')