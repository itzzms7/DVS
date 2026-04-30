from django.db import models

class Voter(models.Model):
    aadhar_number = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.aadhar_number}"