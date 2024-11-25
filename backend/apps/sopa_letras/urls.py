from . import views
from django.urls import path

urlpatterns = [
    path('prueba/', views.pruebaApi.as_view(), name='crear-prueba-api'),
    # path('pruebas/', views.prueba2.as_view(), name='crear-prueba-api'),
]