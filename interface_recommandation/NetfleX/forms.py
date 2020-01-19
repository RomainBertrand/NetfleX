"""Definition of all the classes needed to create the various forms of NetfleX

All classes inherits from forms.Form, a Django-predefined class for forms.

Classes:
MoviesRatings --  For a form that ask for a movie and its rating
ChoiceMovieNumber -- To choose the number of films you want to rate for your recommendation
MovieChoice -- For the form on the advice page

Functions:
create_list_movies -- list of all the movies that are in the database
"""

import sqlite3
from django import forms

LIST_OF_ALL_TAGS = ["Documentary", "Drama", "Adventure", "Fantasy", "War", "Crime", "Children", "Romance", "Comedy",
                    "Western", "Horror", "Thriller", "Film-Noir", "Sci-Fi", "Action", "IMAX", "Musical", "Animation", "Mystery", "No"]

def create_list_movies() -> list:
    """Create the list of all the movies of the database
    
    Returns:
    list_movies (list): List of all the movies of the database
    """

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
    """A form made of the title of a film and its rating

    Attributes:
    title (forms.CharField): Title of a film from the database. Required
    rating (forms.IntegerField): Rating of the film. (max_value: 5, min_value: 0). Required

    Methods:
    clean -- Rules for the form validation.
    """

    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_movie'}))
    rating = forms.IntegerField(max_value=5, min_value=0, required=True)

    def clean(self):
        """Personalized rules of validation for the form: ensure that title is in the database"""

        cleaned_data = super().clean()
        title = cleaned_data.get('title')

        list_movies = create_list_movies()

        if title not in list_movies:
            raise forms.ValidationError(
                'Veuillez sélectionner un film dans la liste')


class ChoiceMovieNumber(forms.Form):
    """A form for choosing the number of MoviesRatings forms NetfleX' user wants to fill

    Attributes:
    movie_number (forms.IntegerField): The number of films that will be used for the recommendation. (max_value: 10, min_value: 1, default: 5) Required
    """
    movie_number = forms.IntegerField(max_value=10, min_value=1, initial=5)


class MovieChoice(forms.Form):
    """Collect information needed to give advice of movies

    Attributes:
    title (forms.CharField): Title of the chosen film. Required
    movie_advice_likes (forms.BooleanField): True if NetfeX' user likes the chosen film. Not required
    movie_advice_hates (forms.BooleanField): True if NetfeX' user hates the chosen film. Not required
    movie_number (forms.IntegerField): Number of movies displayed as advice. (max_value: 10, min_value: 1, default: 5) Required
    movie_tag (forms.ChoiceField): Tag of the movies NetfleX' user would like to see. (choices: LIST_OF_ALL_TAGS, default: "No") Not required

    Methods:
    clean -- Rules for the form validation.
    """
    title = forms.CharField(max_length=100, required=True, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_movie'}))
    movie_advice_likes = forms.BooleanField(required=False)
    movie_advice_hates = forms.BooleanField(required=False)
    movie_number = forms.IntegerField(max_value=10, min_value=1, initial=5)


    list_of_tuple = [(LIST_OF_ALL_TAGS[i], LIST_OF_ALL_TAGS[i]) for i in range(len(LIST_OF_ALL_TAGS))]
    LIST_OF_ALL_TAGS = list_of_tuple

    movie_tag = forms.ChoiceField(choices=LIST_OF_ALL_TAGS, widget=forms.Select(), initial="No", required=False)

    def clean(self):
        """Personalized rules of validation for the form
        
        Ensure that title is in the database.
        Ensure that the movie is not liked and hated at the same time
        """
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        movie_advice_likes = cleaned_data.get('movie_advice_likes')
        movie_advice_hates = cleaned_data.get('movie_advice_hates')

        list_movies = create_list_movies()

        if title not in list_movies:
            raise forms.ValidationError(
                'Veuillez sélectionner un film dans la liste')

        if (movie_advice_likes and movie_advice_hates):
            raise forms.ValidationError(
                'On ne peut pas aimer et détester un même film!')
        if not movie_advice_likes and not movie_advice_hates:
            raise forms.ValidationError('Veuillez choisir une option')
