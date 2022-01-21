from django import forms
from .models import Game, Tariff, Economic, IndTariff, Player, Hexes, Army, Policy, Faction, PlayerProduct, Product, MapInterface
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
        fields = ['name','country']

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
class AddPlayerProductForm(ModelForm):
    class Meta:
        model = PlayerProduct
        fields = []

class AddProductForm(ModelForm):
    class Meta:
        model = Product
        fields = []

class IndProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['exportRestriction','subsidy']

class IndTariffForm(ModelForm):
	class Meta:
		model = IndTariff
		fields = ['tariffAm','sanctionAm','moneySend','militarySend','nationalization']

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

class MapInterfaceForm(ModelForm):
    class Meta:
        model = MapInterface
        fields = ['mode']

class ArmyForm(ModelForm):
    class Meta:
        model = Army
        fields = ['name','size','location','naval']

    def clean(self):
        super(ArmyForm, self).clean()
        #c = self.cleaned_data.get('controller')
        s = self.cleaned_data.get('size')
        return self.cleaned_data

    """def save(self, excerpt=None, force_insert=False, force_update=False, commit=True):
        #object = super(Army, self).save(commit=commit)
        import pdb; pdb.set_trace()
        c = self.controller
        if self._state.adding is True:
            if c.get_country().Military - s >= 0:
                c.get_country().Military -= s;
            else:
                c.size = 1"""

            #self._errors['IncomeTax'] = self.error_class(['You cannot have negative numbers in spending plan.'])

class GovernmentSpendingForm(ModelForm):
    class Meta:
        model = Player
        fields = ['IncomeTax','CorporateTax','Welfare','AdditionalWelfare','Education','Military','InfrastructureInvest','MoneyPrinting','ScienceInvest','TheoreticalInvest','PracticalInvest','AppliedInvest','investment_restriction']

    def clean(self):
        super(GovernmentSpendingForm, self).clean()
        it = self.cleaned_data.get('IncomeTax')
        ct = self.cleaned_data.get('CorporateTax')
        w = self.cleaned_data.get('Welfare')
        aw = self.cleaned_data.get('AdditionalWelfare')
        e = self.cleaned_data.get('Education')
        m = self.cleaned_data.get('Military')
        ii = self.cleaned_data.get('InfrastructureInvest')
        si = self.cleaned_data.get('ScienceInvest')
        total = w + e + m + ii + si + aw
        ti = self.cleaned_data.get('TheoreticalInvest')
        pi = self.cleaned_data.get('PracticalInvest')
        ai = self.cleaned_data.get('AppliedInvest')

        if total > 1:
            self._errors['IncomeTax'] = self.error_class(['Spending must not be more than 1.'])
        if it < 0 or ct < 0 or w < 0 or e < 0 or m < 0 or ii < 0 or si < 0:
            self._errors['IncomeTax'] = self.error_class(['You cannot have negative numbers in spending plan.'])

        if ti + pi + ai != 1:
            self._errors['IncomeTax'] = self.error_class(['Theoretical, Practical, and Applied Invest must equal 1.'])

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

