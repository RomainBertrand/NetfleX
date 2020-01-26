from django.urls import path
from . import views

# urlpattern is a Django variable, this is why it doesn't conform the snake_case convention

urlpatterns = [
    path('', views.home, name="home"),
    path('recommendation/', views.manage_notations, name="First" page"),
    path('final_page/', views.final_page, name="Final page"),
    path('advice/', views.advice, name='Advice'),
    path('contact/', views.contact, name="Contact"),
    path('sources/', views.sources, name="Sources"),
    path('changement/', views.change_movie_number,
         name="Change_movie_number"),
]
