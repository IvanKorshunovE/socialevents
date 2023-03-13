from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('<int:year>/<str:month>/', views.home, name='home'),
    path('events', views.all_events, name='list-events'),
    path('add_venue', views.add_venue, name='add_venue'),
]

# URL is empty string '' which points to the views.py --> def home()

# int: numbers
# str: strings
# path: all urls, / - slashes.
# slug: - _ hyphen-underscores-stuff
# UUID: Universally unique identifyer

# name='home' - this is for HTML url (from web page or template)