"""
Classe NotationFilms, qui contient un champ pour le titre du film et un autre pour la note
"""

from django import forms


class NotationFilms(forms.Form):
    """
    le tire est un charfield pour que l'utilisateur puisse taper ce qu'il veut.
    De plus, on passe la liste des titres de films en arguent du form html
    """
    titre = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'list': 'Films', 'class': 'form_film'}))
    note = forms.IntegerField(max_value=5, min_value=0)
