from django.db import models
from django.utils import timezone
# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=20)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to = "images/", null=True, blank=True)
    
    
    def __str__(self):
        return str(self.title)  
    
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    body = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    
class AdminUser(models.Model):
    username = models.CharField(max_length=150)
    birth_year = models.IntegerField()
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    exercise_area = models.CharField(max_length=150)

    def __str__(self):
        return self.username