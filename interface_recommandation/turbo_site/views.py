from django.shortcuts import render
from django.http import HttpResponse
from .forms import NotationFilms 
import sqlite3
# Create your views here.

def home(request):
    return HttpResponse("<h2>Hello World</h2>")

def nouvelle_page(request):
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
    return render(request, "turbo_site/nouvelle_page.html", locals())

def premiere_note(request):
    if request.method == 'POST':
        note = NotationFilms(request.POST)
        if note.is_valid():
            return render(request, "turbo_site/premiere_note.html", locals())
    else :
        note = NotationFilms() 
    return render(request, "turbo_site/nouvelle_page.html", locals())
