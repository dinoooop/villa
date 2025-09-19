from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    builder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")  # ✅ link to User
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to="projects/", blank=True, null=True)
    bedrooms = models.IntegerField(blank=True, null=True)
    bathrooms = models.IntegerField(blank=True, null=True)
    area = models.IntegerField(blank=True, null=True)
    floor = models.IntegerField(blank=True, null=True)
    parking = models.IntegerField(blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
class Visit(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="visits")
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    scheduled_date_time = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit by {self.name} for {self.project.title} on {self.scheduled_date_time.strftime('%Y-%m-%d %H:%M')}"
