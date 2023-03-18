from django.shortcuts import render
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Events, Venue
from .forms import VenueForm

# Create your views here.

def search_venues(request):
	if request.method == 'POST':
		searched = request.POST['searched']  # Grabs what you searched for
		venues = Venue.objects.filter(name__contains=searched)
		return render(request, 'events/search_venues.html', {
			'venues': venues,
			'searched': searched,
	})

def show_venue(request, venue_id):
	venue = Venue.objects.get(id=venue_id)
	return render(request, 'events/show_venue.html', {
		'venue': venue
	})

def list_venues(request):
	venue_list = Venue.objects.all()
	return render(request, 'events/venues.html', {
		'venue_list': venue_list
	})

def add_venue(request):
	submitted = False
	if request.method == 'POST':
		form = VenueForm(request.POST)
		# request.POST is whatever they posted
		if form.is_valid():
			# If form is written correctly - we want to save it to the database
			form.save()
			return HttpResponseRedirect('/add_venue?submitted=True')
	else:
		form = VenueForm
		if 'submitted' in request.GET:
			# We check if ('/add_venue?submitted=True') will be in GET request
			submitted = True

	print(submitted)
	# form = VenueForm
	return render(request, 'events/add_venue.html', {
		'form': form,
		'submitted': submitted,
	})

def all_events(request):
	event_list = Events.objects.all()
	return render(request, 'events/event_list.html', {
		'event_list': event_list
	})

def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
	name = 'Ivan'
	month = month.title()
	# convert month from name to number
	month_number = list(calendar.month_name).index(month)
	month_number = int(month_number)

	# create a calendar
	cal = HTMLCalendar()
	cal_month = cal.formatmonth(year, month_number)

	# Get current year
	now = datetime.now()
	current_year = now.year

	# Get current time
	time = now.strftime('%I:%M:%S %p')

	return render(request, 'events/home.html', {
		'name': name,
		'year': year,
		'month': month,
		'month_number': month_number,
		'cal_month': cal_month,
		'current_year': current_year,
		'time': time,
	})