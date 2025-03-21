from django.db import models

# Define your models here
class InventoryItem(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()

    def __str__(self):
        return self.name 