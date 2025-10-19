from django.urls import path
from . import views

app_name = 'geomap'
urlpatterns = [
    path('', views.index, name='index'),
    path('get_regional_trends/', views.get_regional_trends, name = 'get_regional_trends'),
    path('get_trending_movies_in_bbox/', views.get_trending_movies_in_bbox, name = 'get_trending_movies_in_bbox'),
]