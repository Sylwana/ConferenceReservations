from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, request
from django.utils.decorators import method_decorator

from reservations.models import Room

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
