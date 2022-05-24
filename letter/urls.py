from django.urls import path
from . import views

app_name = 'letter'


urlpatterns = [
    # post views
    path('', views.news_list, name='news_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/',
         views.news_detail,
         name='news_detail'),
]
