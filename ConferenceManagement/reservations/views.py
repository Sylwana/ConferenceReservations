from datetime import date, datetime
import datetime
from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, request
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from reservations.models import Room, Reservation

class Main(View):

    def __init__(self):
        self.message = ''
        self.html = 'Main.html'

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all().order_by('name')
        return render(request, self.html, {"rooms": rooms, "message": self.message})


class NewRoom(Main):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        return render(request, 'newRoom.html')

    def post(self, request):
        if request.POST.get('projector_available') == '1':
            projector = 1
        else:
            projector = 0
        r = Room.objects.create(name=request.POST["name"], capacity=request.POST["capacity"], \
                                projector_available=projector)
        self.message = "Room {} added to the database".format(r.name)
        return super().get(request)


class NewReservation(Main):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id):
        picked_room = Room.objects.get(id=id)
        return render(request, 'newReservation.html', {"room": picked_room})

    def post(self, request, id):
        picked_room = Room.objects.get(id=id)
        date_today = date.today()
        date_form = datetime.datetime.strptime(request.POST["date"], '%Y-%m-%d').date()
        dates_taken = Reservation.objects.values_list().filter(room__id=id)
        t1 = []
        for i in dates_taken:
            t1.append(i[1])
        if date_form < date.today():
            self.message = "Cannot add a reservation. This date has passed"
            self.html = 'newReservation.html'
        elif date_form in t1:
            self.message = "Cannot add a reservation. This date is taken"
            self.html = 'newReservation.html'
        else:
            r = Reservation.objects.create(date=request.POST["date"], room=picked_room, comment=request.POST["comment"])
            self.message = "Reservation of room {} for {} added to the database. {}".format(picked_room.name, r.date, \
                                                                                            date_today)
        return super().get(request)


class ShowRoom(Main):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request, id):
        room = Room.objects.get(id=id)
        reservations = Reservation.objects.filter(room__id=id)
        dates_taken = Reservation.objects.values_list('date').filter(room__id=id)

        return render(request, 'ShowRoom.html', {"room": room, "reservations": reservations, "taken": dates_taken})

    def post(self, request, id):
        picked_room = Room.objects.get(name=request.POST['room'])
        r = Reservation.objects.create(date = request.POST["date"], room=picked_room, comment=request.POST["comment"])
        self.message = "Reservation of room {} for {} added to the database".format(picked_room.name, r.date)
        return super().get(request)