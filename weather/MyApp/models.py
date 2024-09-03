from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=25, default="")
    #intha name vanthu oru object ah than varum

    def __str__(self):          #__str__ eathukku use panrom na antha object ah string ah change panna
        return self.name            #string ah change pannathan -> itha vachi than search panna mudium