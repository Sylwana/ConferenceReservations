from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=16)
    capacity = models.IntegerField()
    projector_available = models.BooleanField()

    def __str__(self):
        return "{}".format(self.name)


class Reservation(models.Model):
    date = models.DateField()
    room = models.ForeignKey(Room)
    comment = models.CharField(max_length=127)

    def __str__(self):
        return "{} {}".format(self.room, self.date)

