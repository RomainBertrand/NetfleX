from django import forms

class NotationFilms(forms.Form):
    titre = forms.CharField()
    note = forms.IntegerField()
    def afficheNote(self):
        return int(self.data.get('note'))
    def afficheTitre(self):
        return str(self.data.get('nomFilm'))
