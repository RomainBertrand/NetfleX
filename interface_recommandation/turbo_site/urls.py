from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = "accueil"),
    path('nouvelle_page/', views.nouvelle_page, name = "bidule"),
]
