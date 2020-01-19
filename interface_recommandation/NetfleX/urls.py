from django.urls import path
from . import views

# urlpattern is a Django variable, this is why it doesn't conform the snake_case convention

urlpatterns = [
    path('', views.home, name="accueil"),
    path('recommendation/', views.manage_notations, name="Première page"),
    path('final_page/', views.final_page, name="Page finale"),
    path('advice/', views.advice, name='Conseil'),
    path('contact/', views.contact, name="Page Contact"),
    path('sources/', views.sources, name="Page Sources"),
    path('changement/', views.change_movie_number,
         name="Changement nombre movies"),
]
