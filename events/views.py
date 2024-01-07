# from unicodedata import name
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.models import User
import calendar
from calendar import HTMLCalendar
from datetime import datetime, date
from .models import Event, Venue
from .forms import EventForm, VenueForm

def home(request):
    if  str(request.user) == "AnonymousUser":
        acc = "Non-Member"
    else:
        acc = request.user

    # do copywriht footer just for fun
    copy_time = datetime.now().year

    return render(request, "events/home.html", {
        "acc" : acc,
        "copy_time" : copy_time,
        })

def see_calendar(request, year=datetime.now().year, month=datetime.now().strftime("%B")):
    if  str(request.user) == "AnonymousUser":
        acc = "Non-Member"
    else:
        acc = request.user

    # convert month name into number
    month_capitalized = month.title()
    month_number = list(calendar.month_name).index(month_capitalized)
    
    # create calendar
    cal = HTMLCalendar().formatmonth(year, month_number)

    # do copywriht footer just for fun
    copy_time = datetime.now().year

    event_list = Event.objects.filter(event_date__year = year, event_date__month = month_number, confirmed = True)

    if not event_list:
        messages.info(request, f"No events yet on {month_capitalized}/{year}...")
        return render(request, "events/see_calendar.html", {
            "acc" : acc,
            "year" : year,
            "month" : month,
            "cal" : cal,
            "copy_time" : copy_time,
            })
    else:
        pagin = Paginator(event_list, 6)
        page = request.GET.get("page")
        event_list = pagin.get_page(page)
        range = pagin.page_range
        return render(request, "events/see_calendar.html", {
            "acc" : acc,
            "year" : year,
            "month" : month,
            "cal" : cal,
            "copy_time" : copy_time,
            "event_list" : event_list,
            "range" : range,
            })

def this_month(request):
    # check the user
    if  str(request.user) == "AnonymousUser":
        acc = "Non-Member"
    else:
        acc = request.user
    
    # do copywriht footer just for fun
    copy_time = datetime.now().year

    # create current month and year
    month = datetime.now().strftime("%B")
    month_no= datetime.now().strftime("%m")
    year = datetime.now().year

    # find events in given month
    events_list = Event.objects.filter(confirmed = True, event_date__year = year, event_date__month = month_no, event_date__gte = date.today())
    return render(request, "events/this_month.html", {
        "acc" : acc,
        "copy_time" : copy_time,
        "month" : month,
        "year" : year,
        "events_list" : events_list,
        })

def next(request):
    if  str(request.user) == "AnonymousUser":
        acc = "Non-Member"
    else:
        acc = request.user

    # create next month and year
    month_no = datetime.now().strftime("%m")
    year = datetime.now().year
    if month_no != "12":
        next_month_no = str(int(datetime.now().strftime("%m")) + 1)
        print(type(next_month_no))
        datetime_object = datetime.strptime(next_month_no, "%m")
        month = datetime_object.strftime("%B")
    else:
        next_month_no = "1"
        datetime_object = datetime.strptime(next_month_no, "%m")
        month = datetime_object.strftime("%B")
        year = year + 1

    # find events in next month
    events_list = Event.objects.filter(confirmed = True, event_date__year = year, event_date__month = next_month_no)

    # do copywriht footer just for fun
    copy_time = datetime.now().year

    return render(request, "events/next.html", {
        "acc" : acc,
        "year" : year,
        "month" : month,
        "copy_time" : copy_time,
        "events_list" : events_list,
        })

def add_venue(request):
    copy_time = datetime.now().year

    if request.user.is_superuser or request.user.groups.filter(name='Owner').exists():
        if request.method == "POST":
            form = VenueForm(request.POST)
            if form.is_valid():
                complete = form.save(commit=False)
                complete.owner = request.user # bunu aşağıda form = VenueForm(initial={'owner': request.user}) olarak da yapabilirdik
                complete.save()
                messages.success(request, "Venue Created...")
                return redirect("home")
            else:
                messages.error(request, "Somethin's wrong with the form...")
                return render(request, "events/add_venue.html", {
                "copy_time" : copy_time,
                "form" : form,
                })
        else:
            form = VenueForm()
            return render(request, "events/add_venue.html", {
            "copy_time" : copy_time,
            "form" : form,
            })
    else:
        messages.error(request, "No Admin privileges...")
        return redirect("home")

def my_venues(request):
    copy_time = datetime.now().year
    venue_list = Venue.objects.filter(owner=request.user.id)
    if not venue_list:
        messages.error(request, "You have no venues...")
        return redirect("home")
    else:
        pagin = Paginator(venue_list, 6)
        page = request.GET.get("page")
        venue_list = pagin.get_page(page)
        range = pagin.page_range
        return render(request, "events/my_venues.html", {
            "venue_list" : venue_list,
            "copy_time" : copy_time,
            "range" : range
        })

def add_event(request):
    copy_time = datetime.now().year

    if request.user.is_superuser or request.user.groups.filter(name__in=["Manager", "Owner"]).exists():
        if request.method == "POST":
            form = EventForm(request.POST, request.FILES)
            if form.is_valid():
                complete = form.save(commit=False)
                complete.manager = request.user # bunu aşağıda form = EventForm(initial={'manager': request.user}) olarak da yapabilirdik
                complete.save()
                messages.success(request, "Event Created...")
                return redirect("home")
            else:
                messages.error(request, "Form was not valid...")
                return render(request, "events/add_event.html", {
                "copy_time" : copy_time,
                "form" : form,
                })
        else:
            form = EventForm() 
            return render(request, "events/add_event.html", {
                "copy_time" : copy_time,
                "form" : form,
                })
    else:
        messages.error(request, "No Admin privileges...")
        return redirect("home")

def my_events(request):
    copy_time = datetime.now().year
    event_list = Event.objects.filter(manager=request.user.id).order_by("-event_date")
    if not event_list:
        messages.error(request, "You have no events...")
        return redirect("home")
    else:
        pagin = Paginator(event_list, 6)
        page = request.GET.get("page")
        event_list = pagin.get_page(page)
        range = pagin.page_range
        return render(request, "events/my_events.html", {
            "event_list" : event_list,
            "copy_time" : copy_time,
            "range" : range
        })

def all_events(request):
    copy_time = datetime.now().year
    if request.method == "POST":
        try:
            request.POST["search_city"]
        except:
            pass
        else:
            search_for_raw = request.POST["search_city"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, venue__city__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_city"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })

        try:
            request.POST["search_venue"]
        except:
            pass
        else:
            search_for_raw = request.POST["search_venue"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, venue__name__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_venue"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })

        try:
            request.POST["search_manager"]
        except:
            pass
        else:
            search_for_raw = request.POST["search_manager"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, manager__username__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_manager"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
        messages.error(request, "Something was wrong...")
        return redirect("home")
                
    else:
        try:
            request.GET["search_city"]
        except:
            pass
        else:
            search_for_raw = request.GET["search_city"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, venue__city__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_city"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })

        try:
            request.GET["search_venue"]
        except:
            pass
        else:
            search_for_raw = request.GET["search_venue"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, venue__name__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_venue"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })

        try:
            request.GET["search_manager"]
        except:
            pass
        else:
            search_for_raw = request.GET["search_manager"]

            # baştaki türkçe İ i sorununu çözmek için
            if not search_for_raw:
                messages.error(request, "No valid search data...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })
            else:
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            events_all = Event.objects.filter(confirmed = True, manager__username__icontains=search_for, event_date__gte = date.today())
            events = events_all.order_by("event_date", "name", "venue")
            if events:
                pagin = Paginator(events, 6)
                page = request.GET.get("page")
                event_list = pagin.get_page(page)

                range = pagin.page_range
                look_for = "search_manager"

                return render(request, "events/events_list.html", {
                    "search_for" : search_for,
                    "events" : events,
                    "range" : range,
                    "copy_time" : copy_time,
                    "event_list" : event_list,
                    "look_for" : look_for,
                }) 
            else:
                messages.error(request, "No Result...")
                return render(request, "events/events_list.html", {
                    "copy_time" : copy_time,
                })

        return render(request, "events/events_list.html", {
            "copy_time" : copy_time,
        })

def show_event(request, event_id):
    copy_time = datetime.now().year
    event = Event.objects.get(id=event_id)
    if request.user.is_superuser or request.user == event.manager or event.confirmed:
        if request.user in event.participants.all():
            participate = True
        else:
            participate = False
        return render(request, "events/show_event.html", {
            "event" : event,
            "copy_time" : copy_time,
            "participate" : participate
        })
    else:
        messages.error(request, "No priviledge or active event...")
        return redirect("home")

def mod_event(request, event_id):
    copy_time = datetime.now().year
    event = Event.objects.get(id=event_id)
    if request.user.is_superuser or request.user == event.manager:
        if event.Validity:
            form = EventForm(request.POST or None, request.FILES or None, instance=event)
            if form.is_valid():
                form.save()
                messages.success(request, "Event modified...")
                return render(request, "events/show_event.html", {
                "event" : event,
                "copy_time" : copy_time,
                })
            else:
                return render(request, "events/mod_event.html", {
                    "event" : event,
                    "form" : form,
                    "copy_time" : copy_time,
                })
        else:
            messages.error(request, "Cannot modify past events...")
            return render(request, "events/show_event.html", {
            "event" : event,
            "copy_time" : copy_time,
            })
    else:
        messages.error(request, "No Modify privilege...")
        return redirect("home")

def del_event(request, event_id):
    copy_time = datetime.now().year
    event = Event.objects.get(id=event_id)
    if request.user.is_superuser or request.user == event.manager:
        if event.Validity:
            event.delete()
            messages.success(request, "Event deleted...")
            return redirect("home") # neden HttpResponseRedirect çalışmıyor burda?
        else:
            messages.error(request, "Cannot modify past events...")
            return render(request, "events/show_event.html", {
            "event" : event,
            "copy_time" : copy_time,
            })
        
    else:
        messages.error(request, "No Delete privilege...")
        return redirect("home")

def list_venues(request):
    copy_time = datetime.now().year
    if request.method == "POST":
        try:
            search_for_raw = request.POST["search_for_city"]
        except:
            pass
        else:
            # baştaki türkçe İ i sorununu çözmek için
            if search_for_raw[0] == "İ":
                search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            venues_all = Venue.objects.filter(city__icontains=search_for)
            
            if venues_all:
                venues = venues_all.order_by("name", "province")
                pagin = Paginator(venues, 8)
                page = request.GET.get("page")
                venue_list = pagin.get_page(page)

                range = pagin.page_range

                return render(request, "events/venues.html", {
                    "search_for" : search_for,
                    "venue_list" : venue_list,
                    "range" : range,
                    "copy_time" : copy_time,
                }) 
            else:
                messages.error(request, "No Venues found...")
                return render(request, "events/venues.html", {
                "copy_time" : copy_time,
                })
        try:
            search_for_raw = request.POST["search_for"]
        except:
            pass
        else:
            # baştaki türkçe İ i sorununu çözmek için
            if search_for_raw[0] == "İ":
                search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            venues_all = Venue.objects.filter(name__icontains=search_for)
            
            if venues_all:
                venues = venues_all.order_by("name", "province")
                pagin = Paginator(venues, 8)
                page = request.GET.get("page")
                venue_list = pagin.get_page(page)

                range = pagin.page_range

                return render(request, "events/venues.html", {
                    "search_for" : search_for,
                    "venue_list" : venue_list,
                    "range" : range,
                    "copy_time" : copy_time,
                }) 
            else:
                messages.error(request, "No Venues found...")
                return render(request, "events/venues.html", {
                "copy_time" : copy_time,
                })
        messages.error(request, "No valid search...")
        return render(request, "events/venues.html", {
            "copy_time" : copy_time,
        })
    else:
        try:
            search_for_raw = request.POST["search_for"]
        except:
            try:
                search_for_raw = request.POST["search_for_city"]
            except:
                return render(request, "events/venues.html", {
                "copy_time" : copy_time,
                })
            else:
                # baştaki türkçe İ i sorununu çözmek için
                if search_for_raw[0] == "İ":
                    search_for_raw = "I" + search_for_raw[1:]
                
                search_for = search_for_raw.lower()
                venues_all = Venue.objects.filter(city__icontains=search_for)
                
                if venues_all:
                    venues = venues_all.order_by("name", "province")
                    pagin = Paginator(venues, 8)
                    page = request.GET.get("page")
                    venue_list = pagin.get_page(page)

                    range = pagin.page_range

                    return render(request, "events/venues.html", {
                        "search_for" : search_for,
                        "venue_list" : venue_list,
                        "range" : range,
                        "copy_time" : copy_time,
                    }) 
                else:
                    messages.error(request, "No Venues found...")
                    return render(request, "events/venues.html", {
                    "copy_time" : copy_time,
                    })
        else:
            search_for_raw = request.POST["search_for"]

            # baştaki türkçe İ i sorununu çözmek için
            if search_for_raw[0] == "İ":
                search_for_raw = "I" + search_for_raw[1:]
            
            search_for = search_for_raw.lower()
            venues_all = Venue.objects.filter(name__icontains=search_for)
            
            if venues_all:
                venues = venues_all.order_by("name", "province")
                pagin = Paginator(venues, 8)
                page = request.GET.get("page")
                venue_list = pagin.get_page(page)

                range = pagin.page_range

                return render(request, "events/venues.html", {
                    "search_for" : search_for,
                    "venue_list" : venue_list,
                    "range" : range,
                    "copy_time" : copy_time,
                }) 
            else:
                messages.error(request, "No Venues found...")
                return render(request, "events/venues.html", {
                "copy_time" : copy_time,
                })

def show_venue(request, venue_id):
    venue = Venue.objects.get(id=venue_id)
    copy_time = datetime.now().year

    return render(request, "events/show_venue.html", {
        "venue" : venue,
        "copy_time" : copy_time,
    })

def search(request):
    copy_time = datetime.now().year
    if request.method == "POST":
        search_for_raw = request.POST["search_for"]

        # baştaki türkçe İ i sorununu çözmek için
        if search_for_raw[0] == "İ":
            search_for_raw = "I" + search_for_raw[1:]
        
        search_for = search_for_raw.lower()

        venues_per_name = Venue.objects.filter(name__icontains =search_for)
        venues_per_city = Venue.objects.filter(city__icontains=search_for)
        venues_all = venues_per_name | venues_per_city
        venues = venues_all.order_by("name", "city")
        
        if str(venues) == "<QuerySet []>":
            search_for_split = search_for.split()
            for search_split in search_for_split:
                venues_name = Venue.objects.filter(name__icontains=search_split)
                venues_city = Venue.objects.filter(city__icontains=search_split)
                venues_con = venues_name | venues_city
                venues_all = venues_all | venues_con
                venues = venues_all.order_by("name", "city")

        pagin_v = Paginator(venues, 4)
        page_v = request.GET.get("page_v")
        venues = pagin_v.get_page(page_v)

        range_v = pagin_v.page_range

        events_per_name = Event.objects.filter(confirmed = True, name__icontains=search_for, event_date__gte = date.today())
        events_per_venue = Event.objects.filter(confirmed = True, venue__name__icontains=search_for, event_date__gte = date.today())
        events_per_city = Event.objects.filter(confirmed = True, venue__city__icontains=search_for, event_date__gte = date.today())
        events_all = events_per_name | events_per_venue | events_per_city
        events = events_all.order_by("event_date", "name", "venue")

        if str(events) == "<QuerySet []>":
            search_for_split = search_for.split()
            for search_split in search_for_split:
                events_name = Event.objects.filter(confirmed = True, name__icontains=search_split, event_date__gte = date.today())
                events_city = Event.objects.filter(confirmed = True, venue__city__icontains=search_split, event_date__gte = date.today())
                events_venue = Event.objects.filter(confirmed = True, venue__name__icontains=search_split, event_date__gte = date.today())
                events_con = events_name | events_city | events_venue
                events_all = events_all | events_con
                events = events_all.order_by("event_date", "name", "venue")

        pagin_e = Paginator(events, 3)
        page_e = request.GET.get("page_e")
        events = pagin_e.get_page(page_e)

        range_e = pagin_e.page_range

        return render(request, "events/search.html", {
            "search_for" : search_for,
            "venues" : venues,
            "range_v" : range_v,
            "events" : events,
            "range_e" : range_e,
            "copy_time" : copy_time,
        })
    else:
        search_for_raw = request.GET["search_for"]

        # baştaki türkçe İ i sorununu çözmek için
        if search_for_raw[0] == "İ":
            search_for_raw = "I" + search_for_raw[1:]
        
        search_for = search_for_raw.lower()

        venues_per_name = Venue.objects.filter(name__icontains =search_for)
        venues_per_city = Venue.objects.filter(city__icontains=search_for)
        venues_all = venues_per_name | venues_per_city
        venues = venues_all.order_by("name", "city")
        
        if str(venues) == "<QuerySet []>":
            search_for_split = search_for.split()
            for search_split in search_for_split:
                venues_name = Venue.objects.filter(name__icontains=search_split)
                venues_city = Venue.objects.filter(city__icontains=search_split)
                venues_con = venues_name | venues_city
                venues_all = venues_all | venues_con
                venues = venues_all.order_by("name", "city")

        pagin_v = Paginator(venues, 4)
        page_v = request.GET.get("page_v")
        venues = pagin_v.get_page(page_v)

        range_v = pagin_v.page_range

        events_per_name = Event.objects.filter(confirmed = True, name__icontains=search_for, event_date__gte = date.today())
        events_per_venue = Event.objects.filter(confirmed = True, venue__name__icontains=search_for, event_date__gte = date.today())
        events_per_city = Event.objects.filter(confirmed = True, venue__city__icontains=search_for, event_date__gte = date.today())
        events_all = events_per_name | events_per_venue | events_per_city
        events = events_all.order_by("event_date", "name", "venue")

        if str(events) == "<QuerySet []>":
            search_for_split = search_for.split()
            for search_split in search_for_split:
                events_name = Event.objects.filter(confirmed = True, name__icontains=search_split, event_date__gte = date.today())
                events_city = Event.objects.filter(confirmed = True, venue__city__icontains=search_split, event_date__gte = date.today())
                events_venue = Event.objects.filter(confirmed = True, venue__name__icontains=search_split, event_date__gte = date.today())
                events_con = events_name | events_city | events_venue
                events_all = events_all | events_con
                events = events_all.order_by("event_date", "name", "venue")

        pagin_e = Paginator(events, 3)
        page_e = request.GET.get("page_e")
        events = pagin_e.get_page(page_e)

        range_e = pagin_e.page_range

        return render(request, "events/search.html", {
            "search_for" : search_for,
            "venues" : venues,
            "range_v" : range_v,
            "events" : events,
            "range_e" : range_e,
            "copy_time" : copy_time,
        })

    
def check_date(request):
    copy_time = datetime.now().year
    month_no = datetime.now().strftime("%m")
    year = datetime.now().year
    min_date = str(year) + "-" + month_no
    max_date = str(year + 2) + "-" + month_no 
    if request.method == "POST":
        check_for = request.POST["check_for"]
        if check_for:
            split = check_for.split("-")
            year = split[0]
            month = split[1]
            events_list = Event.objects.filter(confirmed = True, event_date__year = year, event_date__month = month)
            if events_list:
                return render(request, "events/check_date.html", {
                    "check_for" : check_for,
                    "copy_time" : copy_time,
                    "events_list" : events_list,
                })
            else:
                messages.error(request, "No Event on selected date...")
                return HttpResponseRedirect("check_date")
        else:
            messages.error(request, "Select a date...")
            return HttpResponseRedirect("check_date")
    else:
        return render(request, "events/check_date.html", {
            "copy_time" : copy_time,
            "min_date" : min_date,
            "max_date" : max_date,
        })

def admin_approve(request):
    copy_time = datetime.now().year
    if request.user.is_superuser:
        if request.method == "POST":
            id_list = request.POST.getlist("confirmation")
            for event in id_list:
                splitted = event.split(", ")
                id = splitted[0]
                app_status = splitted[1]
                if app_status == "True":
                    print(id)
                    Event.objects.filter(id=int(id)).update(confirmed=True)
            messages.info(request, "Approvals Are Modified...")
            return redirect("admin-approve")
        else:    
            events_list = Event.objects.filter(confirmed = False, event_date__gte = date.today()).order_by("-event_date")
            if events_list:
                return render(request, "events/admin_approval.html", {
                        "copy_time" : copy_time,
                        "events_list" : events_list,
                    })
            else:
                messages.info(request, "No Pending Events...")
                return redirect("statistics")
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def statistics(request):
    copy_time = datetime.now().year
    if request.user.is_superuser:
        past_events = Event.objects.filter(event_date__lt = date.today()).count()
        on_hold_events = (Event.objects.filter(confirmed = True, event_date__gte = date.today(), manager = None) | Event.objects.filter(confirmed = True, event_date__gte = date.today(), venue = None) | Event.objects.filter(confirmed = True, event_date__gte = date.today(), venue__owner = None)).count()
        pending_events = Event.objects.filter(confirmed = False, event_date__gte = date.today()).count()
        upcoming_events = Event.objects.filter(confirmed = True, event_date__gte = date.today()).exclude(manager = None).exclude(venue = None).exclude(venue__owner = None).count()
        on_hold_venues = Venue.objects.filter(owner = None).count()
        active_venues = Venue.objects.exclude(owner = None).count()
        owner_users = User.objects.filter(groups__name__icontains = 'Owner').count()
        manager_users = User.objects.filter(groups__name__icontains = 'Manager').count()
        normal_users = User.objects.filter(groups = None).count()

        return render(request, "events/statistics.html", {
                    "copy_time" : copy_time,
                    "past_events" : past_events,
                    "on_hold_events" : on_hold_events,
                    "pending_events" : pending_events,
                    "upcoming_events" : upcoming_events,
                    "on_hold_venues" : on_hold_venues,
                    "active_venues" : active_venues,
                    "owner_users" : owner_users,
                    "manager_users" : manager_users,
                    "normal_users" : normal_users,
                })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def upcoming_events(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        events_all = Event.objects.filter(confirmed = True, event_date__gte = date.today()).exclude(manager = None).exclude(venue = None).exclude(venue__owner = None)
        events = events_all.order_by("event_date", "name", "venue")
        
        if events:
            pagin = Paginator(events, 6)
            page = request.GET.get("page")
            event_list = pagin.get_page(page)

            range = pagin.page_range
            search_for = "Upcoming Events"

            return render(request, "events/events_list.html", {
                "events" : events,
                "range" : range,
                "copy_time" : copy_time,
                "event_list" : event_list,
                "search_for" : search_for,
            }) 
        else:
            messages.error(request, "No Result...")
            return render(request, "events/events_list.html", {
                "copy_time" : copy_time,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def on_hold_events(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        events_all = Event.objects.filter(confirmed = True, event_date__gte = date.today(), manager = None) | Event.objects.filter(confirmed = True, event_date__gte = date.today(), venue = None) | Event.objects.filter(confirmed = True, event_date__gte = date.today(), venue__owner = None)
        events = events_all.order_by("event_date", "name", "venue")
        
        if events:
            pagin = Paginator(events, 6)
            page = request.GET.get("page")
            event_list = pagin.get_page(page)

            range = pagin.page_range
            search_for = "On Hold Events"

            return render(request, "events/events_list.html", {
                "events" : events,
                "range" : range,
                "copy_time" : copy_time,
                "event_list" : event_list,
                "search_for" : search_for,
            }) 
        else:
            messages.error(request, "No Result...")
            return render(request, "events/events_list.html", {
                "copy_time" : copy_time,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def past_events(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        events_all = Event.objects.filter(confirmed = True, event_date__lt = date.today())
        events = events_all.order_by("event_date", "name", "venue")
        
        if events:
            pagin = Paginator(events, 6)
            page = request.GET.get("page")
            event_list = pagin.get_page(page)

            range = pagin.page_range
            search_for = "Past Events"

            return render(request, "events/events_list.html", {
                "events" : events,
                "range" : range,
                "copy_time" : copy_time,
                "event_list" : event_list,
                "search_for" : search_for,
            }) 
        else:
            messages.error(request, "No Result...")
            return render(request, "events/events_list.html", {
                "copy_time" : copy_time,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def active_venues(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        venue_list = Venue.objects.exclude(owner=None)
        special = "active"
        if not venue_list:
            messages.error(request, "No active venues...")
            return redirect("statistics")
        else:
            pagin = Paginator(venue_list, 6)
            page = request.GET.get("page")
            venue_list = pagin.get_page(page)
            range = pagin.page_range
            return render(request, "events/my_venues.html", {
                "venue_list" : venue_list,
                "copy_time" : copy_time,
                "range" : range,
                "special" : special,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def on_hold_venues(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        venue_list = Venue.objects.filter(owner=None)
        special = "passive"
        if not venue_list:
            messages.error(request, "No passive venues...")
            return redirect("statistics")
        else:
            pagin = Paginator(venue_list, 6)
            page = request.GET.get("page")
            venue_list = pagin.get_page(page)
            range = pagin.page_range
            return render(request, "events/my_venues.html", {
                "venue_list" : venue_list,
                "copy_time" : copy_time,
                "range" : range,
                "special" : special,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def venue_owners(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        user_list = User.objects.filter(groups__name="Owner")
        special = "owners"
        if not user_list:
            messages.error(request, "No Venue Owners...")
            return redirect("statistics")
        else:
            pagin = Paginator(user_list, 8)
            page = request.GET.get("page")
            user_list = pagin.get_page(page)
            range = pagin.page_range
            return render(request, "events/show_users.html", {
                "user_list" : user_list,
                "copy_time" : copy_time,
                "range" : range,
                "special" : special,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def event_managers(request):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        user_list = User.objects.filter(groups__name="Manager")
        special = "managers"
        if not user_list:
            messages.error(request, "No Event Managers...")
            return redirect("statistics")
        else:
            pagin = Paginator(user_list, 8)
            page = request.GET.get("page")
            user_list = pagin.get_page(page)
            range = pagin.page_range
            return render(request, "events/show_users.html", {
                "user_list" : user_list,
                "copy_time" : copy_time,
                "range" : range,
                "special" : special,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def owner_venues(request, look_owner):
    if request.user.is_superuser:
        copy_time = datetime.now().year
        venue_list = Venue.objects.filter(owner=look_owner)
        special = "owner"
        if not venue_list:
            messages.error(request, "No venues of this Owner...")
            return redirect("venue-owners")
        else:
            pagin = Paginator(venue_list, 6)
            page = request.GET.get("page")
            venue_list = pagin.get_page(page)
            range = pagin.page_range
            look_owner_name = get_object_or_404(User, id=look_owner)
            return render(request, "events/my_venues.html", {
                "venue_list" : venue_list,
                "copy_time" : copy_time,
                "range" : range,
                "special" : special,
                "look_owner_name" : look_owner_name,
            })
    else:
        messages.error(request, "No Privilege...")
        return redirect("home")

def venue_events(request, venue_id):
    copy_time = datetime.now().year
    events_all = Event.objects.filter(confirmed = True, event_date__gte = date.today(), venue=venue_id)
    events = events_all.order_by("event_date", "name", "venue")
    
    if events:
        pagin = Paginator(events, 6)
        page = request.GET.get("page")
        event_list = pagin.get_page(page)

        range = pagin.page_range
        search_for = get_object_or_404(Venue, id=venue_id)

        return render(request, "events/events_list.html", {
            "events" : events,
            "range" : range,
            "copy_time" : copy_time,
            "event_list" : event_list,
            "search_for" : search_for,
        }) 
    else:
        messages.error(request, "No Events...")
        return render(request, "events/events_list.html", {
            "copy_time" : copy_time,
        })

def join_event(request, event_id):
    copy_time = datetime.now().year
    event = Event.objects.get(id=event_id)
    if request. user. is_authenticated:
        if request.user in event.participants.all():
            messages.error(request, "Already joined...")
            return redirect("home")
        else:
            event.participants.add(request.user)
            messages.success(request, f"Joined to: {event}...")
            return render(request, "events/events_list.html", {
                "copy_time" : copy_time,
                })
    else:
        messages.error(request, "Need to Login first...")
        return redirect("login-user")

def leave_event(request, event_id):
    copy_time = datetime.now().year
    event = Event.objects.get(id=event_id)
    if request. user. is_authenticated:
        if request.user in event.participants.all():
            event.participants.remove(request.user)
            messages.success(request, f"You have left: {event}...")
            return render(request, "events/events_list.html", {
                "copy_time" : copy_time,
                })
        else:
            
            messages.error(request, "You are not joined...")
            return redirect("home")
    else:
        messages.error(request, "Need to Login first...")
        return redirect("login-user")
 