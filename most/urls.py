from django.urls import path
from most.views import most_view

urlpatterns = [
    path("dashboard/", most_view),
]