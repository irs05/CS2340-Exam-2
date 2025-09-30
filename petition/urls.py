from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='petition.index'),
    path('create/', views.create_petition, name='petition.create_petition'),
    path('<int:id>/delete/', views.delete_petition, name='petition.delete_petition'),
    path('<int:id>/vote/', views.vote_petition, name='petition.vote_petition'),
]