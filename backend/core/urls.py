from django.urls import path
from . import views

urlpatterns = [

    # Auth
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("change-password/", views.change_password, name="change_password"),

    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),

    # Event
    path("events/", views.event_list, name="event_list"),
    path("events/create/", views.event_create, name="event_create"),
    path("events/<int:id>/", views.event_detail, name="event_detail"),

    # Place
    path("places/", views.place_list, name="place_list"),
    path("places/create/", views.place_create, name="place_create"),
    path("places/edit/<int:id>/", views.place_edit, name="place_edit"),
    path("places/<int:id>/", views.place_detail, name="place_detail"),

    # Team
    path("teams/", views.team_list, name="team_list"),
    path("teams/create/", views.team_create, name="team_create"),
    path("teams/edit/<int:id>/", views.team_edit, name="team_edit"),
    path("teams/<int:id>/", views.team_detail, name="team_detail"),

    # User
    path("users/", views.user_list, name="user_list"),
    path("users/create/", views.user_create, name="user_create"),
    path("profile/", views.user_profile, name="user_profile"),

    # Planning
    path("plan/", views.plan_create, name="plan_create"),
    path("plan/result/", views.plan_result, name="plan_result"),
]