from django import forms
from .models import Game, Tariff, Economic, IndTariff
from django.forms import ModelForm

class NewGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name']

class IndTariffForm(ModelForm):
	class Meta:
		model = IndTariff
		fields = ['tariffAm']

class EconomyForm(ModelForm):
    class Meta:
        model = Economic
        fields = ['factory_num', 'welfare']