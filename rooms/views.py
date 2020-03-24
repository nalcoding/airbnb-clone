from django.utils import timezone
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView
from django.http import Http404
from django_countries import countries
from . import models


class HomeView(ListView):
    """ HomeView Definition """

    model = models.Room
    paginate_by = 2
    paginate_orphans = 1
    ordering = "created"
    page_kwarg = "page"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        return context


# 아래 방식은 Function Base View
"""
def room_detail(request, potato):
    # print("pk => ", potato)
    try:
        room = models.Room.objects.get(pk=potato)
        # print(dir(room))
        return render(request, "rooms/detail.html", context={"room": room})
    except models.Room.DoesNotExist:
        # return redirect(reverse("core:home"))
        raise Http404()
"""
# Class Base View 방식은 아래와 같음
class RoomDetail(DetailView):

    model = models.Room


def search(request):
    print(request.GET)
    city = request.GET.get("city", "aNywhere")
    city = str.capitalize(city)
    country = request.GET.get("country", "KR")
    room_type = int(request.GET.get("room_type", 0))
    price = int(request.GET.get("price", 0))
    guests = int(request.GET.get("guests", 0))
    bedrooms = int(request.GET.get("bedrooms", 0))
    beds = int(request.GET.get("beds", 0))
    baths = int(request.GET.get("baths", 0))
    instant = bool(request.GET.get("instant", False))
    superhost = bool(request.GET.get("superhost", False))

    s_amenities = request.GET.getlist("amenities")
    s_facilities = request.GET.getlist("facilities")

    form = {
        "city": city,
        "s_country": country,
        "s_room_type": room_type,
        "price": price,
        "guests": guests,
        "bedrooms": bedrooms,
        "beds": beds,
        "baths": baths,
        "s_amenities": s_amenities,
        "s_facilities": s_facilities,
        "instant": instant,
        "superhost": superhost,
    }

    room_types = models.RoomType.objects.all()
    amenities = models.Amenity.objects.all()
    facilities = models.Facility.objects.all()

    choices = {
        "countries": countries,
        "room_types": room_types,
        "amenities": amenities,
        "facilities": facilities,
    }

    filter_args = {}

    if city != "Anywhere":
        filter_args["city__startswith"] = city

    filter_args["country"] = country

    if room_type != 0:
        filter_args["room_type__pk"] = room_type

    # 가격은 같거나 싸야함, less then equals
    if price != 0:
        filter_args["price__lte"] = price

    # 가능 손님수는 같거나 많아야함 greater then equals
    if guests != 0:
        filter_args["guests__gte"] = guests

    # 침실수는 같거나 많아야함
    if bedrooms != 0:
        filter_args["bedrooms__gte"] = bedrooms

    # 침대수는 같거나 많아야함
    if beds != 0:
        filter_args["beds__gte"] = beds

    # 화장실수는 같거나 많아야함
    if baths != 0:
        filter_args["baths__gte"] = baths

    if instant is True:
        filter_args["instant_book"] = True

    if superhost is True:
        filter_args["host__superhost"] = True

    print(s_amenities)
    if len(s_amenities) > 0:
        for s_amenity in s_amenities:
            filter_args["amenities__pk"] = int(s_amenity)

    print(s_facilities)
    if len(s_facilities) > 0:
        for s_facility in s_facilities:
            filter_args["facilities__pk"] = int(s_facility)

    print(filter_args)
    rooms = models.Room.objects.filter(**filter_args)

    return render(
        request, "rooms/search.html", context={**form, **choices, "rooms": rooms}
    )
