from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=120)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)  # blank=False - can't be empty

    def __str__(self):
        return self.name

class MyClubUser(models.Model):
    first_name = models.CharField('First Name', max_length=30)
    last_name = models.CharField('Last Name', max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

class Events(models.Model):
    name = models.CharField('Event Name', max_length=120)
    event_date = models.DateTimeField('Event Date')
    # venue = models.CharField(max_length=120)
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    # Deleting venue (AREA 41) deletes Event: Alien Party
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    #  User IS NOT and has NOTHING TO DO with MyClubUser !!!
    # If a manager deletes his profile - what happens to all that events? SET_NULL - in this case we set the manager
    # field to NULL
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyClubUser, blank=True)

    def __str__(self):
        return self.name


# CharFiels = simple text
# blank=True means that we do not have to put data here.

# !!! venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE) - We use foreign key here
# because the key will be ONE. This is ONE-TO-MANY relationships.
# We can't add just column with foreign key with MANY-TO-MANY relationships - because there will be many foreign keys.