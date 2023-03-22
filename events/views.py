from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from django.http import HttpResponseRedirect
from .models import Events, Venue
# import user model from django
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponse
from django.contrib import messages
import csv

from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Import pagination stuff
from django.core.paginator import Paginator


# Create your views here.
def my_events(request):
    """
    Owner: IvanK (id = 1) I can edit 2 of that events because IvanK is logged user that is owner (Event.owner) - User
    Attendee: IvanKorshunov (id=1) 3 events where attendee is IvanKorshunov - MyClubUser
    """
    if request.user.is_authenticated:
        me = request.user.id
        # atts = Events.objects.get(id=4).attendees.all()
        events = Events.objects.filter(attendees=me)  # or attendees=request.user.id
        return render(request, 'events/my_events.html', {
            'events': events,
            # "atts": atts,
            'me': me,
        })
    else:
        messages.success(request, 'You are not authorized')
        return redirect('home')

def venue_pdf(request):
    # Create Bytestream Buffer
    buf = io.BytesIO()
    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    # Create a text object
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont('Helvetica', 14)

    # Add some lines of text
    # lines = [
    #     'This is line 1',
    #     'This is line 2',
    #     'This is line 3',
    # ]

    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(venue.name)
        lines.append(venue.address)
        lines.append(venue.zip_code)
        lines.append(venue.phone)
        lines.append(venue.web)
        lines.append(venue.email_address)
        lines.append(' ')

    for line in lines:
        textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='Venue.pdf')


def venue_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    #  Create a CSV writer
    writer = csv.writer(response)

    # Designate a model - this is a list of all of venues
    venues = Venue.objects.all()

    # Add column headings to CSV file - FIRST ROW OF HEADER STUFF
    writer.writerow(['ID', 'Venue name', 'Address', 'Zip Code', 'Phone', 'Web address', 'Email'])

    for venue in venues:
        writer.writerow([venue.id, venue.name, venue.address, venue.phone, venue.zip_code, venue.web,
                         venue.email_address])

    return response


def venue_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    # lines = ['This is line one\n',
    # 		 'this is line two\n',
    # 		 'this is line 3']

    lines = []
    venues = Venue.objects.all()

    for venue in venues:
        lines.append(f'{venue.name}, \n{venue.address}, \n{venue.phone}, \n{venue.zip_code}, \n{venue.web}, \n'
                     f'{venue.email_address} \n\n\n')

    response.writelines(lines)
    return response


def delete_venue(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    venue.delete()
    return redirect('list-venues')


def delete_event(request, event_id):
    event = Events.objects.get(id=event_id)
    if request.user == event.manager:
        event.delete()
        messages.success(request, 'Event deleted')
        return redirect('list-events')
    else:
        messages.success(request, 'You are not authorized to delete this event')
        return redirect('list-events')


def update_event(request, event_id):
    event = Events.objects.get(id=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)  # If you are going to post - use this form,
    # otherwise do nothing
    #  instance is what we are going to put in the form
    #  if I do not put None - the form will be empty
    if form.is_valid():
        form.save()
        # Here we do not need to pass manager since we already saved it
        return redirect('list-events')
    return render(request, 'events/update_event.html', {
        'event': event,
        'form': form,
    })


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
        if request.user.is_superuser:  # if request.user.id == 4:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')
        else:
            form = EventForm(request.POST)
            # request.POST is whatever they posted
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                # If form is written correctly - we want to save it to the database
                # form.save()
                return HttpResponseRedirect('/add_event?submitted=True')

    else:
        # Just going to the page, Not submitting
        if request.user.is_superuser:
            form = EventFormAdmin
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
    form = VenueForm(request.POST or None,
                     instance=venue)  # If you are going to post - use this form, otherwise do nothing
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
    # venue_owner = User.objects.get(pk=venue.owner)
    venue_owner = User.objects.get(id=venue.owner)  # Grabs username of owner - but grabs the object itself
    # (pk = primary key, == id - they are the same)
    return render(request, 'events/show_venue.html', {
        'venue': venue,
        'venue_owner': venue_owner
    })


def list_venues(request):
    # venue_list = Venue.objects.all().order_by('?')
    venue_list = Venue.objects.all()

    p = Paginator(Venue.objects.all(), 1)  # Paginate: 2 venues per page
    page = request.GET.get('page')
    venues = p.get_page(page)
    nums = 'a' * venues.paginator.num_pages

    return render(request, 'events/venues.html', {
        'venues': venues,
        'venue_list': venue_list,
        'nums': nums,
    })


def add_venue(request):
    submitted = False
    if request.method == 'POST':
        form = VenueForm(request.POST)
        # request.POST is whatever they posted
        if form.is_valid():
            # If form is written correctly - we want to save it to the database
            venue = form.save(commit=False)  # We say 'hey, save it, but just do not save it jet'.
            venue.owner = request.user.id
            venue.save()
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
    event_list = Events.objects.all().order_by('-event_date', 'venue')  # Name or event date in reversed order
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
