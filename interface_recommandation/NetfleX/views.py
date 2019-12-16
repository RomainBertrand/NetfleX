from django.shortcuts import render
from django.http import HttpResponse
from .forms import NotationFilms 
import sqlite3
# Create your views here.

def home(request):
    return HttpResponse("<h2>Hello World</h2>")

def block_avis(request):
    lien = sqlite3.connect("../base_noms_film.db")
    curseur = lien.cursor()
    curseur.execute("SELECT DISTINCT title FROM noms_film")
    liste_movies = curseur.fetchall()
    i=0
    for movie in liste_movies:
        liste_movies[i] = str(movie[0])
        i += 1
    form = NotationFilms(request.POST or None)
    if form.is_valid() :
        nomFilm = form.cleaned_data['nomFilm']
        note = form.cleaned_data['note']
        envoi = True
    return render(request, "NetfleX/block_avis.html", locals())

def page_finale(request):
    if request.method=="POST":
        notation = NotationFilms(request.POST)
        #print(notation.__dict__)
        if notation.is_valid:
            return render(request, "NetfleX/page_finale.html", locals())
    else :
        notation = NotationFilms() 
    return render(request, "NetfleX/block_avis.html", locals())
