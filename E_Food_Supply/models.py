from django.db import models

# Define your models here
class FoodSupply(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name 