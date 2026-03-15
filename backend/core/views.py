from django.shortcuts import render

# Create your views here.

def login_view(request):
    return render(request, "core/login.html")

def events(request):
    return render(request, "core/create_event.html")


def dashboard(request):
    return render(request, "core/dashboard.html")


def places(request):
    return render(request, "core/places.html")


def create_event(request):
    return render(request, "core/create_event.html")


def create_team(request):
    return render(request, "core/create_team.html")


def add_place(request):
    return render(request, "core/add_place.html")