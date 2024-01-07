from django.contrib import admin

from .models import Venue
from .models import WebUser
from .models import Event

@admin.register(Venue)
class Venue_Admin(admin.ModelAdmin):
    list_display= ("name", "city", "province", "owner")
    ordering= ("name", "city")
    search_fields= ("name", "city", "province", "owner__username")
    list_filter= ("city", "owner")

@admin.register(Event)
class Event_Admin(admin.ModelAdmin):
    list_display= ("name", "event_date", "venue_x", "city", "manager", "confirmed")
    ordering= ("event_date", "venue__city")
    search_fields= ("name", "venue__name", "venue__city", "manager__username")
    list_filter= ("venue__city", "event_date", "venue__name", "manager", "confirmed")

    # this is for having foreignkey object to be shown in table display in admin page
    def city(self, obj):
        if obj.venue:
            return obj.venue.city
        else:
            pass
    city.admin_order_field  = 'venue__city'
    city.short_description = 'Venue City'

    # this is for having foreignkey object to be shown in table display in admin page
    def venue_x(self, obj):
        if obj.venue:
            return obj.venue.name
        else:
            pass
    venue_x.admin_order_field  = 'venue__name'
    venue_x.short_description = 'Venue Name'


@admin.register(WebUser)
class Venue_Admin(admin.ModelAdmin):
    list_display= ("nick", "f_name", "l_name")
    ordering= ("nick",)
    search_fields= ("nick", "f_name", "l_name")
