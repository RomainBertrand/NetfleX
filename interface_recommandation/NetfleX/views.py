"""
Fichier qui gère l'affichage, créé les variables nécessaires pour les fichiers html.
"""

import sqlite3
from django.shortcuts import render
from django.forms import formset_factory
from NetfleX.etude_donnees_base import meilleure_correlation, conseil_film
from NetfleX.lecture_csv import init_tags_films
from .forms import NotationFilms, ChoixNombreFilms, ChoixFilm


def creation_liste_films() -> list:
    """ Création de la liste de films proposés à partir de la base de données """
    lien = sqlite3.connect("base_noms_film.db")
    curseur = lien.cursor()
    curseur.execute("SELECT DISTINCT title FROM noms_film")
    liste_movies = curseur.fetchall()
    i = 0
    for movie in liste_movies:
        liste_movies[i] = str(movie[0])
        i += 1
    return liste_movies


def manage_notations(request):  # ->HttpResponse
    """ Gère le formulaire de demande de films et de notes """
    liste_movies = creation_liste_films()
    nombre_films = 5
    form_nombre_choix = ChoixNombreFilms(request.GET, request.FILES)
    if form_nombre_choix.is_valid():
        nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')
        print(nombre_films)
    # on créé une formSet factory issue de la classe NotationFilms
    NotationFilmsFormSet = formset_factory(
        NotationFilms, extra=nombre_films, max_num=10)
    films_choisis = []  # liste de titre et de notes correspondant aux films choisis
    if request.method == 'POST':
        formset = NotationFilmsFormSet(request.POST, request.FILES)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')
                films_choisis.append([titre, note])
            return page_finale(request)
            #return render(request, "NetfleX/page_finale.html", locals())
    else:
        formset = NotationFilmsFormSet()
    return render(request, "NetfleX/block_avis.html", locals())


def home(request):  # ->HttpResponse
    """ Page d'accueil """
    return render(request, "NetfleX/page_accueil.html", locals())


def reaffiche_formulaire():
    """Réafficher le formulaire si l'une des propositions n'est pas un film de la base de données"""
    nombre_films = 5
    NotationFilmsFormSet = formset_factory(
        NotationFilms, extra=nombre_films, max_num=10)
    formset = NotationFilmsFormSet()
    message = "Veuillez choisir uniquement des films dans la liste"
    return formset, message


def page_finale(request):  # ->HttpResponse
    """ Appelle la fonction de matching et affiche le résultat """

    # Coix du nombre de films à noter
    nombre_films = 5
    form_nombre_choix = ChoixNombreFilms(request.GET, request.FILES)
    if form_nombre_choix.is_valid():
        nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')

    NotationFilmsFormSet = formset_factory(
        NotationFilms, extra=nombre_films, max_num=10)
    films_choisis = []
    if request.method == "POST":
        formset = NotationFilmsFormSet(request.POST, request.FILES)
        # print(request.POST)
        if formset.is_valid():
            for film_form in formset:
                titre = film_form.cleaned_data.get('titre')
                note = film_form.cleaned_data.get('note')

                # Si film déjà choisi
                deja_choisi = False
                for elem in films_choisis:
                    if elem[0] == titre:
                        message_meme_choix = """Vous semblez avoir choisi deux fois le même film.
                            Seul le premier sélectionné sera pris en compte. """
                        deja_choisi = True
                if not deja_choisi and titre is not None:
                    films_choisis.append([titre, note])

            lien = sqlite3.connect("base_noms_film.db")
            liste_titres = []
            for film in films_choisis:
                liste_titres.append(film[0])
            curseur = lien.cursor()
            # S'il y a moins de 5 films  rentrés par l'utilisateur :
            liste_titres = [elem for elem in liste_titres if elem is not None]
            # Si la liste est vide, on renvoie le formulaire
            if not liste_titres:
                return render(request, "NetfleX/block_avis.html", locals())
            # on récupère les Id des films choisis par l'utilisateur
            # Le tuple pose problème s'il n'y a qu'un film dans la liste
            enlever_virgule = False
            if len(liste_titres) == 1:
                enlever_virgule = True
            liste_titres = str(tuple(liste_titres))
            if enlever_virgule:
                #liste_titres = liste_titres + liste_titres
                liste_titres = list(liste_titres)
                liste_titres.pop(-2)
                string_titres = ""
                for character in liste_titres:
                    string_titres += character
                liste_titres = string_titres
            curseur.execute(
                "SELECT movieId FROM noms_film WHERE title IN {}".format(liste_titres))
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
        # if not formset.is_valid():
         #   formset, message = reaffiche_formulaire()
    return render(request, "NetfleX/block_avis.html", locals())


def changement_nombre_films(request):  # ->HttpResponse
    """ Changement du nombre de films à noter pour la recommandation """
    if request.method == 'POST':
        form_nombre_choix = ChoixNombreFilms(request.POST, request.FILES)
        if form_nombre_choix.is_valid():
            nombre_films = form_nombre_choix.cleaned_data.get('nombre_films')
            return render(request, "NetfleX/block_avis.html", locals())
    else:
        form_nombre_choix = ChoixNombreFilms()
    return render(request, "NetfleX/changer_nombre_films.html", locals())


def tags_pour_liste_de_films(liste_id_films: list) -> dict:
    """ Retourne une liste de tags correspondants aux films de la liste """

    dico_tags_films = init_tags_films()

    tags_films_choisis = {}
    for film in liste_id_films:
        tags_films_choisis[str(film)] = (dico_tags_films[str(film)])

    return tags_films_choisis


def conseil(request):  # ->HttpResponse
    """ Conseils de films basés sur le choix d'un film """

    # Pour avoir les propositions issues de la bdd
    liste_movies = creation_liste_films()

    if request.method == 'POST':
        aime_ou_deteste = ChoixFilm(request.POST, request.FILES)
        if aime_ou_deteste.is_valid():
            lien = sqlite3.connect("base_noms_film.db")
            curseur = lien.cursor()

            titre = aime_ou_deteste.cleaned_data.get('titre')
            titre = [titre, titre]
            curseur.execute(
                "SELECT movieId FROM noms_film WHERE title IN {}".format(str(tuple(titre))))
            id_titre = int(curseur.fetchall()[0][0])
            aime = aime_ou_deteste.cleaned_data.get('film_conseil_aime')
            nombre_films = aime_ou_deteste.cleaned_data.get('nombre_films')
            print(aime)
            numeros_films_possibles = conseil_film(
                id_titre, aime, nombre_films)
            films_possibles = []

            for film in numeros_films_possibles:
                film = [str(film), str(film)]
                curseur.execute("SELECT DISTINCT title FROM noms_film WHERE movieId IN {}".format(
                    str(tuple(film))))  # on récupère son titre
                films_possibles.append(curseur.fetchall()[0][0])
            print(films_possibles)
            if not films_possibles:
                films_possibles = ["""Désolé, nous ne sommes pas en mesure de vous conseiller,
                    votre avis n'est pas commun par nos utilisateurs..."""]

            tags_films_choisis = tags_pour_liste_de_films(
                numeros_films_possibles)

            # Création de la liste des tags
            liste_tags = set()
            for elem in tags_films_choisis.values():
                for tag in elem:
                    liste_tags.add(tag)
            print(liste_tags)

            # Création d'une liste (nom du film, [tags associés])
            film_avec_tag = []
            # tableau tag : pour le tableau de l'affichage html
            # [[False for tag in tags_films_choisis[num_film]] for num_film in numeros_films_possibles]
            tableau_tags = []
            for ind, num_film in enumerate(numeros_films_possibles):
                film_avec_tag.append(
                    [films_possibles[ind], tags_films_choisis[str(num_film)]])
                # [(films_possibles[ind], True)]
                tableau_film_courant = [films_possibles[ind]]
                for tag in liste_tags:
                    if tag in tags_films_choisis[str(num_film)]:
                        tableau_film_courant.append(True)  # ((True, False))
                    else:
                        tableau_film_courant.append(False)
                tableau_tags.append(tableau_film_courant)

            print(tableau_tags)

            return render(request, "NetfleX/conseil.html", locals())
    else:
        aime_ou_deteste = ChoixFilm()
    return render(request, "NetfleX/conseil.html", locals())


def contact(request):  # ->HttpResponse
    """ Page Contact """
    return render(request, "NetfleX/page_contact.html", locals())


def sources(request):  # ->HttpResponse
    """ Page Sources """
    return render(request, "NetfleX/page_source.html", locals())
