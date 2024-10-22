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
from NetfleX.study_database import best_correlation, advice_movie
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
    """Ensure the form is valid. Otherwise, return a blanck form. Then call the form page.

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file
    movie_number (int): number of movies in the form
    from_final_page (bool): whether the function is called from the final page or not

    Returns:
    formset_is_valid (bool): Whether the formset is valid or not
    movies_chosen (list): list of the distinct movies selected (empty if no movies were chosen)
    formset (formset_factory): the formset filled by the user (empty if no formset were filled)
    same_choice_message (str or None): A string if the same movie was picked more than once
    """
    # Creation of a formSet factory from the class MoviesRatings
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
                # If movie is already chosen:
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
    """Change the number of movies the user will pick for the recommendation

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

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
    """Handle the form of movies and ratings

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

    Returns:
    render (HttpResponse): an html page; final page if the form is correct, form page otherwise
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


def movie_list_to_string(movies_chosen: list) -> (str, bool):
    """Change a list of movies in a readable string for sqlite3

    Parameters:
    movies_chosen (list): list of movies chosen by the user when he fills the form

    Returns:
    list_titles (list): list of strings which contain the movie names
    empty_formset (bool): whether the form is empty or not
    """
    list_titles = []
    for movie in movies_chosen:
        list_titles.append(movie[0])
    # If there is less than 5 films chosen by NetfleX' user:
    list_titles = [elem for elem in list_titles if elem is not None]
    # If the list is empty, a blank form is displayed again
    if not list_titles:
        return [], True
    # We take the ids of the movies chosen by NetfleX' user
    # A tuple of length 1 is problematic because it ends with a comma
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
    """Call the matching function and wait for the response

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

    Returns:
    render (HttpResponse): if form is valid, shows the movie recommended. Otherwise, the form page.
    """
    # Choice of the number of movies to rate
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
        # Best correlation depending on what was chosen by NetfleX' user
        recommended_movie.append(str(best_correlation(user)))
        # We ask for its title:
        cursor.execute("SELECT title FROM noms_film WHERE movieId IN {}".format(
            str(tuple(recommended_movie))))
        recommended_title = cursor.fetchall()[0][0]
        return render(request, "NetfleX/final_page.html", locals())
    return render(request, "NetfleX/recommendation.html", locals())


def tags_for_movie_list(list_movie_ids: list) -> dict:
    """Return a list of tags corresponding to movies of list_movie_ids

    Parameters:
    list_movie_ids (list): list of id of movies for which we need the tag

    Returns:
    tags_movies_chosen (dictionnary): Keys: movie_id (int), values: movie_tags (list of string)
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


def table_of_tags_for_chosen_movies(tags_movies_chosen: dict, id_possible_movies: list, possible_movies: list) -> (list, list):
    """A table of tags for a given movie

    Parameters:
    tags_movies_chosen (dict): for each movie, a list of its tags
    id_possible_movies (list): list of the id of the movies we will recommend
    possible_movies (list): list of movies we will recommend to the user

    Returns:
    tags_list (set): list of all the tags for the movie
    tags_table (list): two-dim list: tags_table[i][j] == True if movie i and tag j are linked
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
    for ind, num_movie in enumerate(id_possible_movies):
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
    """Give a list of movies you may like based on the rating of one movie

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

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
            id_possible_movies = advice_movie(
                id_title, likes, movie_tag, movie_number)
            possible_movies = []

            for movie in id_possible_movies:
                movie = [str(movie), str(movie)]
                # We ask for its title:
                cursor.execute("SELECT DISTINCT title FROM noms_film WHERE movieId IN {}".format(
                    str(tuple(movie))))
                possible_movies.append(cursor.fetchall()[0][0])

            if possible_movies:
                tags_movies_chosen = tags_for_movie_list(
                    id_possible_movies)

                tags_list, tags_table = table_of_tags_for_chosen_movies(
                    tags_movies_chosen, id_possible_movies, possible_movies)
            else:
                no_possible_movies = True

            return render(request, "NetfleX/advice.html", locals())
    else:
        loves_or_hates = MovieChoice()
    return render(request, "NetfleX/advice.html", locals())


def home(request):  # ->HttpResponse
    """Home Page

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

    Returns:
    render (HttpResponse): Shows the home page
    """
    return render(request, "NetfleX/home.html", locals())


def contact(request):  # ->HttpResponse
    """Contact Page

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

    Returns:
    render (HttpResponse): Shows the contact page
    """
    return render(request, "NetfleX/contact.html", locals())


def sources(request):  # ->HttpResponse
    """Sources Page

    Parameters:
    request (HttpRequest): a Django object that pass data from the HTML to the Python file

    Returns:
    render (HttpResponse): Shows the sources page
    """
    return render(request, "NetfleX/source.html", locals())
