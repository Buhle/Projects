from django.db import models
from django.utils import timezone


class Staff(models.Model):
    staff_id = models.UUIDField(primary_key=True)
    company_id = models.UUIDField()
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    address = models.TextField()
    documents = models.FileField(upload_to='documents', null=True, blank=True)
    created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.firstname
