from django.db import models

# Create your models here.

class Box(models.Model):
    name = models.CharField(max_length=100)
    length = models.FloatField()
    width = models.FloatField()
    height = models.FloatField()
    max_weight = models.FloatField()
    cost = models.FloatField()

    def __str__(self):
        return self.name