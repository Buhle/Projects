from django.db import models
from django.utils import timezone


class Companies(models.Model):
    company_id = models.UUIDField(primary_key=True, auto_created=True)
    company_name = models.CharField(unique=True, max_length=255)
    company_reg = models.CharField(max_length=255)
    address = models.TextField()
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.company_name
