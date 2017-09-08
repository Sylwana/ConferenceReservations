from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=16)
    capacity = models.IntegerField()
    projector_available = models.BooleanField()

    def __str__(self):
        return "{}".format(self.name)


