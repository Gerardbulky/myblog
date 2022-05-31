from django.urls import path
from . import views

app_name = 'letter'


urlpatterns = [
     # post views
     path('', views.news_list, name='news_list'),
     path('tag/<slug:tag_slug>/',
          views.news_list, name='news_list_by_tag'),
     path('<int:year>/<int:month>/<int:day>/<slug:news>/',
          views.news_detail, name='news_detail'),
     path('<int:news_id>/share/', views.news_share, name='news_share')
]
