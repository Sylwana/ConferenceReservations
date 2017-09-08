from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, request

from reservations.models import Room

class Main(View):

    def __init__(self):
        self.message = ''
        self.html = 'Main.html'

    def get(self, request, *args, **kwargs):
        rooms = Room.objects.all().order_by('name')
        return render(request, self.html, {"rooms": rooms, "message": self.message})

