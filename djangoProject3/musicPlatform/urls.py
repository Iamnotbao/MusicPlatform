from . import views
from django.urls import path

urlpatterns = [
    path('', views.MusicListView.as_view(), name='music.all'),
    path('search/', views.MusicSearchView.as_view(), name='search'),
    path('<int:pk>', views.MusicDetailView.as_view(), name='music.show'),
    path('<int:id>/review', views.review, name='music.review'),

]
