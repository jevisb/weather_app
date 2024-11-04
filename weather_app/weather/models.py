# weather/models.py

from django.db import models

class SearchHistory(models.Model):
    city = models.CharField(max_length=100)
    country_code = models.CharField(max_length=5)
    search_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-search_time']

    def __str__(self):
        return f"{self.city}, {self.country_code}"
