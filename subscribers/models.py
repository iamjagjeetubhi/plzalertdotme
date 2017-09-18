from django.db import models

# Create your models here.

class Subscribers(models.Model):
    email = models.CharField(max_length=200, blank=True)

    
class Posts(models.Model):
    post_id = models.CharField(max_length=200, blank=True)
    created_date = models.CharField(max_length=200, blank=True)
    created_time = models.CharField(max_length=200, blank=True)
    message = models.CharField(max_length=10000, blank=True)

class EmailSent(models.Model):
	post_id = models.CharField(max_length=200, blank=True)
