from django import forms
from .models import Game, Building, Tariff, Economic, IndTariff, Player, Hexes, Army, Policy, Faction, PlayerProduct, Product, MapInterface, GraphInterface, GraphCountryInterface, Country
from django.forms import ModelForm
from django.forms import formset_factory, BaseFormSet
from django.core.exceptions import ValidationError
from django.forms.widgets import TextInput

class NewGameForm(ModelForm):
    class Meta:
        model = Game
        fields = ['name','num_players','years_per_turn']

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
        dict2 = {}
        for field in fields:
            dict2[field] = TextInput(attrs={'type':'number','step': '0.01'})
        widgets = dict2

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

class GraphInterfaceForm(ModelForm):
    class Meta:
        model = GraphInterface
        fields = ['mode']

class GraphCountryInterfaceForm(ModelForm):
    class Meta:
        model = GraphCountryInterface
        fields = ['country']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get("instance")
        if instance:
            if instance.large:
                valid_countries = Country.objects.all()
            else:
                valid_countries = Country.objects.filter(large=instance.large)
        self.fields['country'].queryset = valid_countries

class ArmyForm(ModelForm):
    class Meta:
        model = Army
        fields = ['name','size','location','naval']

    def clean(self):
        super(ArmyForm, self).clean()
        s = self.cleaned_data.get('size')
        return self.cleaned_data

class BuildingForm(ModelForm):
    class Meta:
        model = Building
        fields = ['name','location','building_type']

    #Applies the cost of the building towards the player
    def applyCost(self, player):
        buildingDict = {'CoalMine':['iron',2], 'IronMine':['iron',3], 'OilWell':['money',3], 'Farm':['iron',1],'Military':['iron',2], 'Commercial':['wheat', 3]}
        modify = buildingDict[self.cleaned_data.get('building_type')]
        curr_am = getattr(player, modify[0])
        #Return False if the player doesn't have enough the required resource
        if curr_am - modify[1] < 0:
            return False
        else:
            setattr(player, modify[0], curr_am - modify[1])
            player.save()
            return True


class GovernmentSpendingForm(ModelForm):
    class Meta:
        model = Player
        fields = ['IncomeTax','CorporateTax','Welfare','Education','Military','InfrastructureInvest','MoneyPrinting','ScienceInvest','TheoreticalInvest','PracticalInvest','AppliedInvest','investment_restriction']
        dict2 = {}
        for field in fields:
            dict2[field] = TextInput(attrs={'type':'number','step': '0.01'})
        dict2['InfrastructureInvest'] = TextInput(attrs={'type':'number','step': '0.001'})
        widgets = dict2
        """widgets = {
        'IncomeTax': TextInput(attrs={'type':'number','min': '0', 'max': '1','step': '0.01'}),
        'CorporateTax': TextInput(attrs={'type':'number','min': '0', 'max': '1','step': '0.01'})

        }"""

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
        #total = w + e + m + ii + si + aw
        ti = self.cleaned_data.get('TheoreticalInvest')
        pi = self.cleaned_data.get('PracticalInvest')
        ai = self.cleaned_data.get('AppliedInvest')
        mp = self.cleaned_data.get('MoneyPrinting')

        if w + e + m + ii + si >= 1:
            self._errors['IncomeTax'] = self.error_class(['You cannot have negative numbers in spending plan.'])
            raise ValidationError('Education, Welfare, Science, Infrastructure, and Military values must in total not be more than 1.')

        if it <= 0 or ct <= 0 or w < 0 or e < 0 or m < 0 or ii < 0 or si < 0:
            self._errors['IncomeTax'] = self.error_class(['You cannot have negative numbers in spending plan.'])
            raise ValidationError('You cannot have negative numbers in spending plan.')

        if it >= 0.9 or ct >= 0.9:
            self._errors['IncomeTax'] = self.error_class(['You cannot have income or corporate taxes by more than 90%.'])
            raise ValidationError('You cannot have income or corporate taxes by more than 90%.')

        if ti + pi + ai != 1:
            self._errors['IncomeTax'] = self.error_class(['Theoretical, Practical, and Applied Invest must equal 1.'])
            raise ValidationError('Theoretical, Practical, and Applied Invest must equal 1.')
        if mp > 10000 or mp < -200:
            self._errors['IncomeTax'] = self.error_class(['Money Printing must be less than 10,000 or more than -200.'])
            raise ValidationError('Money Printing must be less than 10,000 or more than -200.')

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
    def clean(self):
        count = 0
        for form in self.forms:
            result = form.cleaned_data.get('applied')
            if result:
                count += 1
        if count > 1:
            raise ValidationError("Only one option in the formset may be clicked.")

