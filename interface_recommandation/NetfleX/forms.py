"""
Classe NotationFilms, qui contient un champ pour le titre du film et un autre pour la note
"""

import sqlite3
from django import forms


def creation_liste_films():
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


class NotationFilms(forms.Form):
    """
    Le titre est un charfield pour que l'utilisateur puisse taper ce qu'il veut.
    De plus, on passe la liste des titres de films en arguent du form html
    """
    titre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_film'}))
    note = forms.IntegerField(max_value=5, min_value=0, required=True)

    def clean(self):
        cleaned_data = super().clean()
        titre = cleaned_data.get('titre')

        liste_movies = creation_liste_films()

        if titre not in liste_movies:
            raise forms.ValidationError('Veuillez sélectionner un film dans la liste')


class ChoixNombreFilms(forms.Form):
    """
    Formulaire pour choisir le nombre de films sur lequel se base la recommandation
    """
    nombre_films = forms.IntegerField(max_value=10, min_value=1)


class ChoixFilm(forms.Form):
    """
    Formulaire pour choisir le film sur lequel se base le conseil
    """
    titre = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_film'}))
    film_conseil_aime = forms.BooleanField(required=False)
    film_conseil_deteste = forms.BooleanField(required=False)
    nombre_films = forms.IntegerField(max_value=10, min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        titre = cleaned_data.get('titre')
        film_conseil_aime = cleaned_data.get('film_conseil_aime')
        film_conseil_deteste = cleaned_data.get('film_conseil_deteste')

        liste_movies = creation_liste_films()

        if titre not in liste_movies:
            raise forms.ValidationError('Veuillez sélectionner un film dans la liste')

        if (film_conseil_aime and film_conseil_deteste):
            raise forms.ValidationError('On ne peut pas aimer et détester un même film!')
        if not film_conseil_aime and not film_conseil_deteste:
            raise forms.ValidationError('Veuillez choisir une option')