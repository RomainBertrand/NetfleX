from django import forms

import sqlite3

class NotationFilms(forms.Form):
    titre = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'list':'Films', 'class':'form_film'}))
    note = forms.IntegerField(max_value=5, min_value=0)
