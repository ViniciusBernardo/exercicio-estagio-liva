from django.db import models


class Lead(models.Model):

    name = models.CharField(max_length=80)

    email = models.CharField(max_length=80)

    phone = models.CharField(max_length=15, blank=True)

    property_code = models.PositiveIntegerField()
