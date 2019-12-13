from django import forms

class NotationFilms(forms.Form):
    nomFilm = forms.CharField()
    note = forms.IntegerField()

