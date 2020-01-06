from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="accueil"),
    path('block_avis/', views.manage_notations, name="Première page"),
    path('page_finale/', views.page_finale, name="Page finale"),
    path('page_contact/', views.contact, name="Page Contact"),
    path('page_sources/', views.sources, name="Page Sources"),
    path('changement/', views.changement_nombre_films,
         name="Changement nombre films"),
]
