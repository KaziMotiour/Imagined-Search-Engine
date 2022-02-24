from pyexpat import model
from rest_framework import serializers
from .models import searchItems, SearchDetails
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['id','username']
class SearchDetailsSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = SearchDetails
        fields = ['user', 'search_keyword']


class searchItemsSerializer(serializers.ModelSerializer):
    search_detail=SearchDetailsSerializer()
    class Meta:
        model = searchItems
        fields = ['search_detail', 'site_link', 'site_title', 'site_description']
