from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "accueil"),
    path('block_avis/', views.block_avis, name = "Première page"),
    path('page_finale/', views.page_finale, name = "Page finale"),
]
