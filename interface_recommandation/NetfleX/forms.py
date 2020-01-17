"""
Classe MoviesRatings, qui contient un champ pour le title du movie et un autre pour la rating
"""

import sqlite3
from django import forms


def create_list_movies():
    """ Création de la liste de movies proposés à partir de la base de données """
    link = sqlite3.connect("base_noms_film.db")
    cursor = link.cursor()
    cursor.execute("SELECT DISTINCT title FROM noms_film")
    list_movies = cursor.fetchall()
    i = 0
    for movie in list_movies:
        list_movies[i] = str(movie[0])
        i += 1
    return list_movies


class MoviesRatings(forms.Form):
    """
    Le title est un charfield pour que l'user puisse taper ce qu'il veut.
    De plus, on passe la liste des titles de movies en arguent du form html
    """
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_movie'}))
    rating = forms.IntegerField(max_value=5, min_value=0, required=True)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        list_movies = create_list_movies()

        if title not in list_movies:
            raise forms.ValidationError(
                'Veuillez sélectionner un movie dans la liste')


class ChoiceMovieNumber(forms.Form):
    """
    Formulaire pour choisir le nombre de movies sur lequel se base la recommandation
    """
    movie_number = forms.IntegerField(max_value=10, min_value=1)


class MovieChoice(forms.Form):
    """
    Formulaire pour choisir le movie sur lequel se base le advice
    """
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_movie'}))
    movie_advice_likes = forms.BooleanField(required=False)
    movie_advice_hates = forms.BooleanField(required=False)
    movie_number = forms.IntegerField(max_value=10, min_value=1)

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        movie_advice_likes = cleaned_data.get('movie_advice_likes')
        movie_advice_hates = cleaned_data.get('movie_advice_hates')

        list_movies = create_list_movies()

        if title not in list_movies:
            raise forms.ValidationError(
                'Veuillez sélectionner un movie dans la liste')

        if (movie_advice_likes and movie_advice_hates):
            raise forms.ValidationError(
                'On ne peut pas likesr et détester un même movie!')
        if not movie_advice_likes and not movie_advice_hates:
            raise forms.ValidationError('Veuillez choisir une option')
