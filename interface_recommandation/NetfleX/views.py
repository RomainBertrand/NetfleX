from django.shortcuts import render
from django.http import HttpResponse
from .forms import NotationFilms 
import sqlite3
from django.forms import formset_factory
from NetfleX.etude_donnees_base import *
# Create your views here.

def manage_notations(request):
    lien = sqlite3.connect("base_noms_film.db")
    curseur = lien.cursor()
    curseur.execute("SELECT DISTINCT title FROM noms_film")
    liste_movies = curseur.fetchall()
    i=0
    for movie in liste_movies:
        liste_movies[i] = str(movie[0])
        i += 1

    NotationFilmsFormSet = formset_factory(NotationFilms,extra=5,max_num=10)
    films_choisis = []
    if request.method == 'POST':
        formset = NotationFilmsFormSet(request.POST,request.FILES)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')
                films_choisis.append([titre,note])
    else :
        formset=NotationFilmsFormSet()
    return render(request, "NetfleX/block_avis.html", locals())

def home(request):
    return HttpResponse("<h2>Hello World</h2>")

def page_finale(request):
    NotationFilmsFormSet = formset_factory(NotationFilms,extra=5,max_num=10)
    films_choisis = []
    if request.method=="POST":
        formset = NotationFilmsFormSet(request.POST,request.FILES)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')
                films_choisis.append([titre,note])
            lien = sqlite3.connect("base_noms_film.db")
            liste_titres=[]
            for film in films_choisis:
                liste_titres.append(film[0])
            curseur = lien.cursor()
            curseur.execute("SELECT movieId FROM noms_film WHERE title IN {}".format(str(tuple(liste_titres))))
            liste_movieId = curseur.fetchall()
            utilisateur = []
            for i in range(len(liste_movieId)):
                utilisateur.append([int(liste_movieId[i][0]),films_choisis[i][1]])
            film_recommande = [1]
            film_recommande.append(str(meilleure_correlation(utilisateur)))
            curseur.execute("SELECT title FROM noms_film WHERE movieId IN {}".format(str(tuple(film_recommande))))
            titre_recommande = curseur.fetchall()[0][0]
            return render(request, "NetfleX/page_finale.html", locals())
    else :
        notation = NotationFilms() 
    return render(request, "NetfleX/block_avis.html", locals())
