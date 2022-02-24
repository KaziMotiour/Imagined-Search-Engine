from django.urls import path
from .views import searchFormGoogle, gets_filtered_items, filter_search_resuls
from django.contrib.auth import views 
app_name='search'

urlpatterns = [
    # Authentication
    path('', searchFormGoogle, name='search_google'),
    path('search-history/', gets_filtered_items, name='searchHistory'),
    path('filter-resuls/', filter_search_resuls, name='filterResuls')
  
]