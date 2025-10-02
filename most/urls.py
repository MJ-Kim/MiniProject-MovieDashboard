from django.urls import path
from most.views import most_view, dashboard_view

urlpatterns = [
    path("crawl/", most_view, name="most_view"),
    path("dashboard/", dashboard_view),
]