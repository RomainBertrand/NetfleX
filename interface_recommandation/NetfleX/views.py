# -*- coding: utf-8 -*-
"""Manage the display and the variables needed by the html files

Functions:
create_list_movies -- Create the list of all the movies in the database
manage_form -- Ensure that the form from the recommendation page is valid
change_movie_number -- Manage the number of movies the Netlex' user wants to rate
manage_notations - Manage the form for the recommendation page
movie_list_to_string -- Transform a list of film titles into a readable format for sqlite
final_page -- Display of the final page, before and after the submitting of the form
tags_for_movie_list -- Return a list of tags corresponding to a list of movies
table_of_tags_for_chosen_movies -- Manage the tags needed for the displayed table of the advice page
advice -- Display of the advice page, before and after the submitting of the form
home -- Display of the Home page
contact -- Display of the Contact page
sources -- Display of the Sources page
"""

import sqlite3
from django.shortcuts import render
from django.forms import formset_factory
from NetfleX.etude_donnees_base import meilleure_correlation, advice_movie
from NetfleX.lecture_csv import init_tags_movies
from .forms import MoviesRatings, ChoiceMovieNumber, MovieChoice


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


def manage_form(request, movie_number: int, from_final_page: bool) -> (bool, list, formset_factory, str):
    """Ensures the form is valid. Otherwise, returns a blanck form. Then calls the form page.
    
    Returns:
    formset_is_valid (bool): Whether the formset is valid or not
    movies_chosen (list): list of the distinct movies selected (empty if no movies were chosen)
    formset (formset_factory): the formset filled by the user (an empty one if no formset were filled)
    same_choice_message (str or None): A string if the same movie was picked more than once
    """
    # On créé une formSet factory issue de la classe MoviesRatings
    notation_movie_formset = formset_factory(
        MoviesRatings, extra=movie_number, max_num=10)
    movies_chosen = []
    formset_is_valid = False
    same_choice_message = False
    if request.method == "POST":
        formset = notation_movie_formset(request.POST, request.FILES)
        formset_is_valid = formset.is_valid()
        if formset_is_valid:
            for movie_form in formset:
                title = movie_form.cleaned_data.get('title')
                rating = movie_form.cleaned_data.get('rating')
                # Si movie déjà choisi
                already_chosen = False
                for elem in movies_chosen:
                    if elem[0] == title:
                        same_choice_message = """Vous semblez avoir choisi deux fois le même film.
                            Seul le premier sélectionné sera pris en compte. """
                        already_chosen = True
                if not already_chosen and title is not None:
                    movies_chosen.append([title, rating])
    return formset_is_valid, movies_chosen, formset if request.method == "POST" else notation_movie_formset, same_choice_message if from_final_page else None


def change_movie_number(request):  # ->HttpResponse
    """ Changement du nombre de films à noter pour la recommandation 
    
    Returns:
    render (HttpResponse): an html page which enables the user to change the number of movies
    """
    if request.method == 'POST':
        form_choice_number = ChoiceMovieNumber(request.POST, request.FILES)
        if form_choice_number.is_valid():
            movie_number = form_choice_number.cleaned_data.get('movie_number')
            return render(request, "NetfleX/recommendation.html", locals())
    else:
        form_choice_number = ChoiceMovieNumber()
    return render(request, "NetfleX/change_movie_number.html", locals())


def manage_notations(request):  # ->HttpResponse
    """ Gère le formulaire de demande de movies et de ratings 
    
    Returns:
    render (HttpResponse): an html page (either the final page if the form is correct, or the form page otherwise
    """
    list_movies = create_list_movies()
    movie_number = 5
    form_choice_number = ChoiceMovieNumber(request.GET, request.FILES)
    if form_choice_number.is_valid():
        movie_number = form_choice_number.cleaned_data.get('movie_number')
    formset_is_valid, movies_chosen, notation_movie_formset, same_choice_message = manage_form(
        request, movie_number, False)
    if formset_is_valid:
        return final_page(request)
    formset = notation_movie_formset
    return render(request, "NetfleX/recommendation.html", locals())


def movie_list_to_string(movies_chosen) -> (str, bool):
    """ Change list of movies in a readable string for sqlite 
    
    Returns:
    list_titles (list): list of strings which contain the movie names
    empty_formset (bool): whether the form is empty or not
    """
    list_titles = []
    for movie in movies_chosen:
        list_titles.append(movie[0])
    # S'il y a moins de 5 films rentrés par l'utilisateur :
    list_titles = [elem for elem in list_titles if elem is not None]
    # Si la liste est vide, on renvoie le formulaire
    if not list_titles:
        return [], True
    # on récupère les Id des movies choisis par l'user
    # Le tuple pose problème s'il n'y a qu'un film dans la liste
    remove_comma = False
    if len(list_titles) == 1:
        remove_comma = True
    list_titles = str(tuple(list_titles))
    if remove_comma:
        # list_titles = list_titles + list_titles
        list_titles = list(list_titles)
        list_titles.pop(-2)
        string_titles = ""
        for character in list_titles:
            string_titles += character
        list_titles = string_titles
    return list_titles, False


def final_page(request):  # ->HttpResponse
    """ Appelle la fonction de matching et affiche le résultat 

    Returns:
    render (HttpResponse): if the form is valid, prints out the movie recommended. Otherwise, shows the form page.
    """
    # Choix du nombre de movies à ratingr
    movie_number = 5
    formset_is_valid, movies_chosen, formset, same_choice_message = manage_form(
        request, movie_number, True)
    if formset_is_valid:
        link = sqlite3.connect("base_noms_film.db")
        cursor = link.cursor()
        list_titles, empty_formset = movie_list_to_string(movies_chosen)
        if empty_formset:
            return render(request, "NetfleX/recommendation.html", locals())
        cursor.execute(
            "SELECT movieId FROM noms_film WHERE title IN {}".format(list_titles))
        list_movie_id = cursor.fetchall()
        user = []
        for i in range(len(list_movie_id)):
            user.append(
                [int(list_movie_id[i][0]), movies_chosen[i][1]])
        recommended_movie = [1]
        # Meilleure corrélation en fonction des movies et des ratings de l'user
        recommended_movie.append(str(meilleure_correlation(user)))
        cursor.execute("SELECT title FROM noms_film WHERE movieId IN {}".format(
            str(tuple(recommended_movie))))  # on récupère son title
        recommended_title = cursor.fetchall()[0][0]
        return render(request, "NetfleX/final_page.html", locals())
    return render(request, "NetfleX/recommendation.html", locals())


def tags_for_movie_list(list_movie_ids: list) -> dict:
    """ Return a list of tags corresponding to movies of list_movie_ids 

    Returns:
    tags_movies_chosen (dictionnary): Keys: id of movies (int), values: tags of this movie (lsit of string)
    """
    dictionnary_tags_movies, _ = init_tags_movies()

    tags_movies_chosen = {}
    for movie in list_movie_ids:
        tags_from_database = (dictionnary_tags_movies[str(movie)])
        if tags_from_database:
            tags_movies_chosen[str(movie)] = tags_from_database
        else:
            tags_movies_chosen[str(movie)] = None
    return tags_movies_chosen


def table_of_tags_for_chosen_movies(tags_movies_chosen: dict, number_possible_movies: list, possible_movies: list) -> (list, list):
    """A table of tags for a given movie
    Returns:
    tags_list (set): list of all the tags for the movie
    tags_table (list): two-dimensions list : tags_table[i][j] == True if the movie i is linked to the tag j
    """
    # List of useful tags
    tags_list = set()
    for elem in tags_movies_chosen.values():
        for tag in elem:
            tags_list.add(tag)

    # List (movie name, [associated tags])
    movie_with_tag = []
    # tags_table[i][j] == True if the tag j is linked to the movie i
    tags_table = []
    for ind, num_movie in enumerate(number_possible_movies):
        movie_with_tag.append(
            [possible_movies[ind], tags_movies_chosen[str(num_movie)]])
        table_current_movie = [possible_movies[ind]]
        for tag in tags_list:
            if tag in tags_movies_chosen[str(num_movie)]:
                table_current_movie.append(True)
            else:
                table_current_movie.append(False)
        tags_table.append(table_current_movie)

    return tags_list, tags_table


def advice(request):  # ->HttpResponse
    """ Give a list of movies you may like based on the rating of one movie 

    Returns:
    render (HttpResponse): enables the user to see movies liked by people with the same taste as his
    """

    # In order to have access to the database
    list_movies = create_list_movies()

    if request.method == 'POST':
        # loves_or_hates is the form created
        loves_or_hates = MovieChoice(request.POST, request.FILES)
        if loves_or_hates.is_valid():
            link = sqlite3.connect("base_noms_film.db")
            cursor = link.cursor()

            # Extracting data from the form
            title = loves_or_hates.cleaned_data.get('title')
            # To have a readable title for the cursor:
            title = [title, title]
            cursor.execute(
                "SELECT movieId FROM noms_film WHERE title IN {}".format(str(tuple(title))))
            id_title = int(cursor.fetchall()[0][0])
            likes = loves_or_hates.cleaned_data.get('movie_advice_likes')
            movie_number = loves_or_hates.cleaned_data.get('movie_number')
            movie_tag = loves_or_hates.cleaned_data.get('movie_tag')
            # Ids of movies
            number_possible_movies = advice_movie(
                id_title, likes, movie_tag, movie_number)
            possible_movies = []

            for movie in number_possible_movies:
                movie = [str(movie), str(movie)]
                cursor.execute("SELECT DISTINCT title FROM noms_film WHERE movieId IN {}".format(
                    str(tuple(movie))))  # on récupère son title
                possible_movies.append(cursor.fetchall()[0][0])

            if possible_movies:
                tags_movies_chosen = tags_for_movie_list(
                    number_possible_movies)

                tags_list, tags_table = table_of_tags_for_chosen_movies(
                    tags_movies_chosen, number_possible_movies, possible_movies)
            else:
                no_possible_movies = True

            return render(request, "NetfleX/advice.html", locals())
    else:
        loves_or_hates = MovieChoice()
    return render(request, "NetfleX/advice.html", locals())


def home(request):  # ->HttpResponse
    """ Page d'accueil """
    return render(request, "NetfleX/home.html", locals())


def contact(request):  # ->HttpResponse
    """ Page Contact """
    return render(request, "NetfleX/contact.html", locals())


def sources(request):  # ->HttpResponse
    """ Page Sources """
    return render(request, "NetfleX/source.html", locals())
