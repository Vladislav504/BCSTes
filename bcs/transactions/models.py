from django.db import models

class Transaction(models.Model):
    id = models.CharField(primary_key=True, editable=False, max_length=64)
    description = models.TextField(max_length=500, null=False, blank=True)

