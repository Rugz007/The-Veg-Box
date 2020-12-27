from django.db import models
from simple_history.models import HistoricalRecords


class Unit(models.Model):
    unit = models.CharField(max_length=50)
    abbreviation = models.CharField(max_length=5)
    history = HistoricalRecords()

    def __str__(self):
        return self.abbreviation

    class Meta:
        verbose_name_plural = ' Units'
