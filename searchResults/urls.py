from django.urls import path
from .views import searchFormGoogle, gets_filtered_items
from django.contrib.auth import views 
app_name='search'

urlpatterns = [
    # Authentication
    path('deshboard/', searchFormGoogle, name='search_google'),
    path('search-history/', gets_filtered_items, name='searchHistory')
  
]