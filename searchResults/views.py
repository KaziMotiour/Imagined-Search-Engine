
from django.shortcuts import render
from django.contrib.auth.models import User
from .models import SearchDetails, searchItems
from django.utils import timezone
from django.db.models import Q, Sum
import requests
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import api_view, permission_classes
from .serializers import searchItemsSerializer
import time
import datetime
from rest_framework.response import Response
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
    filtering_items={
        'users':User.objects.all(),
        'keywords': SearchDetails.objects.values('search_keyword', 'number_of_result').distinct()
    }
    return render(request, 'search_history.html', {'users':filtering_items['users'], 'keywords':filtering_items['keywords']})
 

@api_view(['GET'])
def filter_search_resuls(request):
    q = request.GET.get('q')
    user = request.GET.get('user')
    keyword = request.GET.get('keyword')
    data = request.GET.get('data')
    startDate = request.GET.get('startDate')
    endDate = request.GET.get('endDate')
    if data:
        if data=='yesterday':
             data_fetch = datetime.datetime.now() - datetime.timedelta(days=2)
        else:
            data_fetch = datetime.datetime.now() - datetime.timedelta(days=30) if data=='last_month' else datetime.datetime.now() - datetime.timedelta(days=7)

    
    if startDate and endDate:
        date1=  datetime.datetime.strptime(startDate,"%Y-%m-%d")
        date2=  datetime.datetime.strptime(endDate,"%Y-%m-%d")

    if user:
        if startDate and endDate:
            filterd_items = searchItems.objects.filter(search_detail__user__username=user).filter(search_detail__search_keyword__icontains=keyword if keyword else '').filter(timestamp__gte=date1).filter(timestamp__lte=date2)
        elif data:
            filterd_items = searchItems.objects.filter(search_detail__user__username=user).filter(search_detail__search_keyword__icontains=keyword if keyword else '').filter(timestamp__gte=data_fetch)
        else:
            filterd_items = searchItems.objects.filter(search_detail__user__username=user).filter(search_detail__search_keyword__icontains=keyword if keyword else '')
    else:
        if startDate and endDate:
            filterd_items = searchItems.objects.filter(search_detail__search_keyword__icontains=keyword if keyword else '').filter(timestamp__gte=date1).filter(timestamp__lte=date2)
        elif data:
            print('fetch_data 2', keyword)
            filterd_items = searchItems.objects.filter(search_detail__search_keyword__icontains=keyword if keyword else '').filter(timestamp__gte=data_fetch)
        else:
           
            filterd_items = searchItems.objects.filter( Q(search_detail__search_keyword__icontains=keyword if keyword else ''))

    if not filterd_items:
        empty='No result found for this query'
        return Response({'empty':empty})
    else:
        serializer = searchItemsSerializer(filterd_items, many=True)
        return Response({'data':'data', 'filterd_items':serializer.data})