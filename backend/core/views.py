from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import User, Event, Place, Team

# =========================
# Auth Views
# =========================
def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
        
    if request.method == "POST":
        u = request.POST.get("username")
        p = request.POST.get("password")
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid username or password.")
            
    return render(request, "auth/login.html")

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def change_password(request):
    return render(request, "auth/change_password.html")

# =========================
# Dashboard View
# =========================
@login_required
def dashboard(request):
    total_places = Place.objects.count()
    visited_places = Place.objects.filter(status="visited").count()
    pending_places = Place.objects.filter(status="pending").count()
    total_teams = Team.objects.count()
    
    recent_places = Place.objects.order_by('-created_at')[:4]
    teams = Team.objects.all()[:3]
    
    context = {
        "total_places": total_places,
        "visited_places": visited_places,
        "pending_places": pending_places,
        "total_teams": total_teams,
        "recent_places": recent_places,
        "teams": teams
    }
    return render(request, "dashboard/dashboard.html", context)

# =========================
# Event Views
# =========================
@login_required
def event_list(request):
    events = Event.objects.all().order_by("-created_at")
    return render(request, "event/event_list.html", {"events": events})

@login_required
def event_create(request):
    if request.method == "POST":
        print("DEBUG EVENT POST:", request.POST)
        name = request.POST.get("name")
        date = request.POST.get("date")
        venue = request.POST.get("venue")
        coordinator = request.POST.get("coordinator")
        number_of_people = request.POST.get("number_of_people")
        description = request.POST.get("description", "")
        
        if name and date and venue:
            Event.objects.create(
                name=name,
                date=date,
                venue=venue,
                coordinator=coordinator,
                number_of_people=number_of_people or 0,
                description=description,
                created_by=request.user
            )
            messages.success(request, "Event created successfully")
            return redirect("event_list")
        else:
            messages.error(request, "Missing required fields")
            
    return render(request, "event/event_create.html")

@login_required
def event_detail(request, id):
    event = get_object_or_404(Event, id=id)
    places = event.places.all()
    teams = event.teams.all()
    
    context = {
        "event": event,
        "places": places,
        "teams": teams
    }
    return render(request, "event/event_detail.html", context)

# =========================
# Place Views
# =========================
@login_required
def place_list(request):
    places = Place.objects.all().order_by("-created_at")
    return render(request, "place/place_list.html", {"places": places})

@login_required
def place_create(request):
    if request.method == "POST":
        print("DEBUG PLACE POST:", request.POST)
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email", "")
        address = request.POST.get("address", "")
        family = request.POST.get("family", "")
        location = request.POST.get("location")
        status = request.POST.get("status", "pending")
        priority = request.POST.get("priority", "medium")
        event_id = request.POST.get("event_id")
        notes = request.POST.get("notes", "")

        print("DEBUG EVENT ID:", event_id)
        
        event = Event.objects.filter(id=event_id).first()
        
        if not event:
            print("ERROR: Event not found")
            messages.error(request, "Event is required")
            return redirect("place_create")

        Place.objects.create(
            name=name,
            phone=phone,
            email=email,
            address=address,
            family=family,
            location=location,
            status=status,
            priority=priority,
            event=event,
            notes=notes
        )
        messages.success(request, "Place created successfully")
        return redirect("place_list")
            
    events = Event.objects.all()
    return render(request, "place/place_create.html", {"events": events})

@login_required
def place_edit(request, id):
    place = get_object_or_404(Place, id=id)
    
    if request.method == "POST":
        place.name = request.POST.get("name", place.name)
        place.phone = request.POST.get("phone", place.phone)
        place.email = request.POST.get("email", place.email)
        place.address = request.POST.get("address", place.address)
        place.family = request.POST.get("family", place.family)
        place.location = request.POST.get("location", place.location)
        place.status = request.POST.get("status", place.status)
        place.priority = request.POST.get("priority", place.priority)
        place.notes = request.POST.get("notes", place.notes)
        
        event_id = request.POST.get("event_id")
        if event_id:
            place.event = get_object_or_404(Event, id=event_id)
            
        place.save()
        messages.success(request, "Place updated successfully")
        return redirect("place_list")

    events = Event.objects.all()
    context = {"place": place, "events": events}
    return render(request, "place/place_edit.html", context)

@login_required
def place_detail(request, id):
    place = get_object_or_404(Place, id=id)
    return render(request, "place/place_detail.html", {"place": place})

# =========================
# Team Views
# =========================
@login_required
def team_list(request):
    teams = Team.objects.all().order_by("-created_at")
    return render(request, "team/team_list.html", {"teams": teams})

@login_required
def team_create(request):
    if request.method == "POST":
        name = request.POST.get("name")
        event_id = request.POST.get("event_id")
        member_ids = request.POST.getlist("members")
        place_ids = request.POST.getlist("places")
        
        event = get_object_or_404(Event, id=event_id) if event_id else None
        if event:
            team = Team.objects.create(name=name, event=event)
            if member_ids:
                team.members.set(member_ids)
            if place_ids:
                team.assigned_places.set(place_ids)
            
            messages.success(request, "Team created successfully")
            return redirect("team_list")
        else:
            messages.error(request, "Valid Event required.")
            
    events = Event.objects.all()
    users = User.objects.all()
    places = Place.objects.all()
    context = {"events": events, "users": users, "places": places}
    return render(request, "team/team_create.html", context)

@login_required
def team_edit(request, id):
    team = get_object_or_404(Team, id=id)
    
    if request.method == "POST":
        team.name = request.POST.get("name", team.name)
        event_id = request.POST.get("event_id")
        if event_id:
            team.event = get_object_or_404(Event, id=event_id)
            
        member_ids = request.POST.getlist("members")
        place_ids = request.POST.getlist("places")
        
        if member_ids:
            team.members.set(member_ids)
        if place_ids:
            team.assigned_places.set(place_ids)
            
        team.save()
        messages.success(request, "Team updated successfully")
        return redirect("team_list")

    events = Event.objects.all()
    users = User.objects.all()
    places = Place.objects.all()
    context = {"team": team, "events": events, "users": users, "places": places}
    return render(request, "team/team_edit.html", context)

@login_required
def team_detail(request, id):
    team = get_object_or_404(Team, id=id)
    members = team.members.all()
    places = team.assigned_places.all()
    
    context = {
        "team": team,
        "members": members,
        "places": places
    }
    return render(request, "team/team_detail.html", context)

# =========================
# User Views
# =========================
@login_required
def user_list(request):
    users = User.objects.all()
    return render(request, "user/user_list.html", {"users": users})

@login_required
def user_create(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        email = request.POST.get("email", "")
        phone = request.POST.get("phone", "")
        designation = request.POST.get("designation", "member")
        
        if username and password:
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email,
                phone=phone,
                designation=designation
            )
            messages.success(request, "User created successfully")
            return redirect("user_list")
        else:
            messages.error(request, "Username and password are required.")
            
    return render(request, "user/user_create.html")

@login_required
def user_profile(request):
    user = request.user
    return render(request, "user/user_profile.html", {"user": user})

# =========================
# Planning (AI) View
# =========================
@login_required
def plan_create(request):
    return render(request, "planning/plan_create.html")

@login_required
def plan_result(request):
    places = Place.objects.all()
    
    plan_dict = {}
    for place in places:
        loc = place.location or "Unknown Location"
        if loc not in plan_dict:
            plan_dict[loc] = []
        plan_dict[loc].append(place.name)
        
    grouped_plan = {}
    day_counter = 1
    for loc, locations_list in plan_dict.items():
        day_key = f"Day {day_counter}"
        grouped_plan[day_key] = locations_list
        day_counter += 1
        
    context = {"plan": grouped_plan}
    return render(request, "planning/plan_result.html", context)