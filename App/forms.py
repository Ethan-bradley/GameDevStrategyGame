from django import forms
from .models import Game, Tariff, Economic, IndTariff, Player, Hexes, Army, Policy, Faction
from django.forms import ModelForm
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError

class NewGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name','num_players']

    def clean(self):
        super(NewGameForm, self).clean()
        n = self.cleaned_data.get('name')
        game_list = Game.objects.all()
        for g in game_list:
            if g.name == n:
                self._errors['name'] = self.error_class(['Choose another name. A game already has this name.'])
        return self.cleaned_data

class JoinGameForm(ModelForm):
    """def __init__(game, *args, **kwargs):
        self.g = game
        super(JoinGameForm, self).__init__(*args, **kwargs)"""

    class Meta:
        model = Player
        fields = ['name','country', 'color']

    """def clean(self):
        super(GovernmentSpendingForm, self).clean()
        n = self.cleaned_data.get('name')
        player_list = Player.objects.filter(game=self.g)
        for p in player_list:
            if p.name == n:
                self._errors['name'] = self.error_class(['Choose another name. A player in this game already has this name.'])
            if p.country.name == c.name:
                self._errors['country'] = self.error_class(['Choose another country. A player in this game has already claimed this country.'])
        return self.cleaned_data"""

class NextTurn(ModelForm):
    class Meta:
        model = Player
        fields = ['ready']

class ResetTurn(ModelForm):
    class Meta:
        model = Player
        fields = []

class AddIndTariffForm(ModelForm):
    class Meta:
        model = IndTariff
        fields = []

class AddTariffForm(ModelForm):
    class Meta:
        model = Tariff
        fields = []

"""class WaitGameForm(ModelForm):
    class Meta:
        model = Player
        fields = ['ready']"""

class IndTariffForm(ModelForm):
	class Meta:
		model = IndTariff
		fields = ['tariffAm']

class EconomyForm(ModelForm):
    class Meta:
        model = Economic
        fields = ['factory_num', 'welfare']

class HexFormTemp(ModelForm):
    class Meta:
        model = Hexes
        fields = ['game', 'controller']

class HexForm(ModelForm):
    class Meta:
        model = Hexes
        fields = []

class ArmyForm(ModelForm):
    class Meta:
        model = Army
        fields = ['name','size','location','naval']

class GovernmentSpendingForm(ModelForm):
    class Meta:
        model = Player
        fields = ['IncomeTax','CorporateTax','Welfare','Education','Military','Bonds','MoneyPrinting']
    def clean(self):
        super(GovernmentSpendingForm, self).clean()
        it = self.cleaned_data.get('IncomeTax')
        ct = self.cleaned_data.get('CorporateTax')
        w = self.cleaned_data.get('Welfare')
        e = self.cleaned_data.get('Education')
        m = self.cleaned_data.get('Military')
        total = w + e + m
        if total > 1:
            self._errors['IncomeTax'] = self.error_class(['Spending must add up to 1.'])
        return self.cleaned_data

class PolicyForm(ModelForm):
    class Meta:
        model = Policy
        fields = ['applied']

class PolicyCreateForm(ModelForm):
    class Meta:
        model = Policy
        fields = []

class CreateFactionForm(ModelForm):
    class Meta:
        model = Faction
        fields = ['name']

class PolicyFormSet(BaseFormSet):
    #def __init__(self, *args, **kwargs):
    #    super(BaseFormSet, self).__init__(*args, **kwargs)

    def clean(self):
        count = 0
        for form in self.forms:
            result = form.cleaned_data.get('applied')
            if result:
                count += 1
        if count > 1:
            raise ValidationError("Only one option in the formset may be clicked.")

