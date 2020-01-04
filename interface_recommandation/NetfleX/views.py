"""
fichier qui gère l'affichage, créé les variables nécessaires pour les fichiers html.
"""

import sqlite3
from django.http import HttpResponse
from django.shortcuts import render
from django.forms import formset_factory
from NetfleX.etude_donnees_base import meilleure_correlation
from .forms import NotationFilms, ChoixNombreFilms


def manage_notations(request):
    """ Gère le formulaire de demande de films et de notes """
    # on créé la liste des noms de films pour avoir le menu déroulant
    lien = sqlite3.connect("base_noms_film.db")
    curseur = lien.cursor()
    curseur.execute("SELECT DISTINCT title FROM noms_film")
    liste_movies = curseur.fetchall()
    i = 0
    for movie in liste_movies:
        liste_movies[i] = str(movie[0])
        i += 1
    nombre_films = 5
    form_nombre_choix = ChoixNombreFilms(request.GET, request.FILES)
    if form_nombre_choix.is_valid():
        nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')
        print(nombre_films)
    # on créé une formSet factory issue de la classe NotationFilms
    NotationFilmsFormSet = formset_factory(NotationFilms, extra=nombre_films, max_num=10)
    films_choisis = []  # liste de titre et de notes correspondant aux films choisis
    if request.method == 'POST':
        formset = NotationFilmsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')
                films_choisis.append([titre, note])
    else:
        formset = NotationFilmsFormSet()
    return render(request, "NetfleX/block_avis.html", locals())


def home(request):
    """ Page d'accueil """
    return render(request, "NetfleX/page_accueil.html", locals())


def page_finale(request):
    """ Appelle la fonction de matching et affiche le résultat """
    nombre_films = 5
    form_nombre_choix = ChoixNombreFilms(request.GET, request.FILES)
    if form_nombre_choix.is_valid():
        nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')
    NotationFilmsFormSet = formset_factory(NotationFilms, extra=nombre_films, max_num=10)
    films_choisis = []
    if request.method == "POST":
        formset = NotationFilmsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')
                films_choisis.append([titre, note])
            lien = sqlite3.connect("base_noms_film.db")
            liste_titres = []
            for film in films_choisis:
                liste_titres.append(film[0])
            curseur = lien.cursor()
            # S'il y a moins de 5 films  rentrés par l'utilisateur :
            liste_titres = [elem for elem in liste_titres if elem!=None]
            # Si la liste est vide, on renvoie le formulaire
            if not liste_titres:
                return render(request, "NetfleX/block_avis.html", locals())
            # on récupère les Id des films choisis par l'utilisateur
            # Le tuple pose problème s'il n'y a qu'un film dans la liste
            if len(liste_titres) != 1:
                curseur.execute("SELECT movieId FROM noms_film WHERE title IN {}".format(
                    str(tuple(liste_titres))))
            else:
                liste_titres = liste_titres + liste_titres
                curseur.execute("SELECT movieId FROM noms_film WHERE title IN {}".format(
                    str(tuple(liste_titres))))
            liste_movieId = curseur.fetchall()
            utilisateur = []
            for i in range(len(liste_movieId)):
                utilisateur.append(
                    [int(liste_movieId[i][0]), films_choisis[i][1]])
            film_recommande = [1]
            # Meilleure corrélation en fonction des films et des notes de l'utilisateur
            film_recommande.append(str(meilleure_correlation(utilisateur)))
            curseur.execute("SELECT title FROM noms_film WHERE movieId IN {}".format(
                str(tuple(film_recommande))))  # on récupère son titre
            titre_recommande = curseur.fetchall()[0][0]
            return render(request, "NetfleX/page_finale.html", locals())
    return render(request, "NetfleX/block_avis.html", locals())


def changement_nombre_films(request):
    """ Changement du nombre de films à noter pour la recommandation """

    if request.method == 'POST':
        form_nombre_choix = ChoixNombreFilms(request.POST, request.FILES)
        if form_nombre_choix.is_valid():
            nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')
            return render(request, "NetfleX/block_avis.html", locals())
    
    else:
        form_nombre_choix = ChoixNombreFilms()

    return render(request, "NetfleX/changer_nombre_films.html", locals())


def contact(request):
    """ Page Contact """
    return render(request, "NetfleX/page_contact.html", locals())


def sources(request):
    """ Page Sources """
    return render(request, "NetfleX/page_source.html", locals())
