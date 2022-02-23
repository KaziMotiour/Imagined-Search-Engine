from datetime import datetime
from email.policy import default
from sqlite3 import Timestamp
from tokenize import Number
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class SearchDetails(models.Model):
    user = models.ForeignKey(User, related_name='userSearch', on_delete=models.CASCADE)
    search_keyword = models.CharField( max_length=1000)
    number_of_result=models.IntegerField(default=0)
    timestamp = models.DateTimeField( auto_now_add=True)

class searchItems(models.Model):
    search_detail = models.ForeignKey(SearchDetails, related_name='search_detail', on_delete=models.CASCADE)
    site_link = models.CharField(max_length=500)
    site_title = models.CharField(max_length=500)
    site_description  = models.CharField(max_length=1000)
    timestamp = models.DateTimeField( auto_now_add=True)