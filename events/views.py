from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Events, Venue
from .forms import VenueForm, EventForm

# Create your views here.

def add_event(request):
	"""

	The return HttpResponseRedirect('/add_event?submitted=True') statement will redirect the user to the same page
	with the GET parameter submitted=True appended to the URL. The URL /add_event?submitted=True is the URL
	of the same view that was just executed, but with the submitted parameter set to True.

	This is a common pattern in web development where after a form submission, instead of rendering a template directly,
	the view redirects the user to another page, in this case, the same page with a success message.
	This helps prevent accidental resubmissions of the form when the user refreshes the page or navigates back and
	forth in their browser history.

	"""
	submitted = False
	if request.method == 'POST':
		form = EventForm(request.POST)
		# request.POST is whatever they posted
		if form.is_valid():
			# If form is written correctly - we want to save it to the database
			form.save()
			return HttpResponseRedirect('/add_event?submitted=True')
	else:
		form = EventForm
		if 'submitted' in request.GET:
			# We check if ('/add_venue?submitted=True') will be in GET request
			submitted = True
	return render(request, 'events/add_event.html', {
		'form': form,
		'submitted': submitted,
	})

def update_venue(request, venue_id):
	venue = Venue.objects.get(id=venue_id)
	form = VenueForm(request.POST or None, instance=venue)  # If you are going to post - use this form, otherwise do nothing
	#  instance is what we are going to put in the form
	#  if I do not put None - the form will be empty
	if form.is_valid():
		form.save()
		return redirect('list-venues')
	return render(request, 'events/update_venue.html', {
		'venue': venue,
		'form': form,
})

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