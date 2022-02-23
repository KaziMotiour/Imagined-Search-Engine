from lib2to3.pgen2.token import EQUAL
from django.shortcuts import render
from .models import SearchDetails, searchItems
import requests
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
# Create your views here.

@login_required(login_url='/auth/login/')
def searchFormGoogle(request):
    query = request.GET.get('q')
    user = request.user

    if query:
        search_result_exist = SearchDetails.objects.filter(user=user, search_keyword=query)

        if search_result_exist:
    
            search_result = search_result_exist[0]
            search_results={
                "search_detail":search_result,
                "search_items":searchItems.objects.filter(search_detail=search_result.id)
            }

        else:
            API_KEY = "AIzaSyD93i1N7mg_No2G_yb1dLrMuMltaubAuLI"
            SEARCH_ENGINE_ID = "df7753a6decb04222"
            url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}" 
            data = requests.get(url).json()
            search_items = data.get("items")
            numberOfSearchItems = len(search_items)
            search_details, created  = SearchDetails.objects.get_or_create(user=request.user, search_keyword=query, number_of_result=numberOfSearchItems)
            print(search_details.id)

            if created: 
                for i, search_item in enumerate(search_items, start=1):

                    title = search_item.get("title")
                    snippet = search_item.get("snippet")
                    link = search_item.get("link")
                    search_items = searchItems(search_detail=search_details, site_link=link, site_title=title, site_description=snippet)
                    search_items.save()

            search_result = SearchDetails.objects.get(id=search_details.id)
            search_results={
                "search_detail":search_result,
                "search_items":searchItems.objects.filter(search_detail=search_result.id)
            }
            
    else:
        
        search_results={
            'search_detail':request,
            "search_items":''
        }
  
    
    return render(request, 'search_from_google.html', {'search_result':search_results['search_detail'],'search_items':search_results['search_items']})




@login_required(login_url='/auth/login/')
def gets_filtered_items(request):
    user = request.GET.get('user')
    asd = request.GET.get('date')
    search_items = searchItems.objects.filter(search_detail__user=request.user)
    print(search_items)
    return render(request, 'search_history.html', {'message':'message'})
 

