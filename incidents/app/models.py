from django.db import models

# Create your models here.
class Incident(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)
    severity = models.CharField(max_length=100)

    class Meta:
        ordering = ['-created_at']