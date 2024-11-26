from . import views
from django.urls import path

urlpatterns = [
    path('word-search/', views.wordSearch.as_view(), name='crear-prueba-api'),
]