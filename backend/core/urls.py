
from django.urls import path
from .views import *


urlpatterns = [
    path("", dashboard, name="dashboard"),
    path("login/", login_view, name="login"),
    path("events/", events, name="events"),
    path("places/", places, name="places"),
    path("create-event/", create_event, name="create_event"),
    path("create-team/", create_team, name="create_team"),
    path("add-place/", add_place, name="add_place"),
    path("logout/", add_place, name="logout"),
]
