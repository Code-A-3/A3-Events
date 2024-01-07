from email.policy import default
from random import choices
from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# to make User email required and unique
User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

class Venue(models.Model):
    name= models.CharField("Venue Name", max_length=60)
    city= models.CharField("Venue City", max_length=60)
    address= models.CharField("Venue Address", max_length=120)
    province= models.CharField("Venue Province", max_length=20)
    phone= models.CharField("Venue Phone", max_length=20, blank=True)
    web= models.URLField("Venue Web", blank=True, max_length=60)
    email= models.EmailField("Venue Email", max_length=30, blank=True)
    owner= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #bunu (User, to_field='username' yaparsan username ile çalışabilirsin.

    class Meta:
        ordering = ["name", "city"]

    def __str__(self):
        return self.name

class WebUser(models.Model):
    f_name = models.CharField("First Name", max_length=20)
    l_name = models.CharField("Last Name", max_length=20)
    nick = models.CharField("User Nick", max_length=20, unique=True)
    email = models.EmailField("User Email", unique=True, max_length=40)
    phone = models.CharField("User Phone", max_length=20)

    def __str__(self):
        return self.f_name + " " + self.l_name

class Event(models.Model):

    # bu confirmation i checkbox yerine selection yapmak icin...
    class confirm_choices(models.TextChoices):
        TRUE = True
        FALSE = False
    
    name= models.CharField("Event Name", max_length=60)
    event_date= models.DateTimeField("Event Date")
    venue= models.ForeignKey(Venue, on_delete=models.SET_NULL, null=True, blank=False)
    manager= models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True) #bunu (User, to_field='username' yaparsan username ile çalışabilirsin.
    description= models.TextField("Event Description", blank=True, max_length=600)
    participants = models.ManyToManyField(User, blank=True, related_name='event_participants')
    event_image = models.ImageField("Event Image", default= "images/Tradeshow.png", upload_to= "images/", blank=False, null=False)
    confirmed = models.CharField("Confirmation", max_length=5, choices=confirm_choices.choices, default=confirm_choices.FALSE)

    class Meta:
        ordering = ["event_date", "venue"]

    def __str__(self):
        return self.name

    @property
    def Validity(self):
        event_due_raw = self.event_date.strftime("%Y-%m-%d %H:%M:%S.%f")
        event_due = datetime.strptime(event_due_raw, "%Y-%m-%d %H:%M:%S.%f")
        if event_due > datetime.now():
            return True
        else:
            return False

