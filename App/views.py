from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, modelformset_factory
from .Game import GameEngine
from .models import Post
from .models import Game, Player, IndTariff, Tariff, Hexes, Army, Policy, PolicyGroup, Country
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, HexForm, ArmyForm, GovernmentSpendingForm, PolicyForm, PolicyFormSet
from django.views.generic.edit import CreateView
from django.apps import apps
import json
from .HexList import HexList
from .PolicyList import PolicyList
from django.db.models.fields import *

def home(request):
	#import pdb; pdb.set_trace()
	context = {
		'posts': Post.objects.all()
		#'posts': posts
	}
	return render(request, 'App/home.html', context)

def account(request):
	return render(request, 'Users/profile.html')

def dashboard(request):
	return render(request, 'dashboard.html')

def help(request):
	return render(request, 'Help.html')

def login(request):
	return render(request, 'Login.html')

def lobby(request):
    #import pdb; pdb.set_trace()
    context = {
        'games': Game.objects.all()
        #'posts': posts
    }
    return render(request, 'App/lobby.html', context)

@login_required
def new_game(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        player_form = JoinGameForm(request.POST)
        if form.is_valid():
            #Creates the game object
            f = form.save(commit=False)
            f.host = request.user
            f.GameEngine = GameEngine(5, ['UK','Germany','France','Spain','Italy'])
            f.curr_num_players = 1
            f.save()
            #Saves game name in temporary variable
            g = f.name
            gameList = Game.objects.all()
            for k in gameList:
                if str(k.name) == g:
                    temp = k
            #Creates a player associated with this user and game and makes them the host.
            pf = player_form.save(commit=False)
            pf.host = True
            pf.user = request.user
            pf.game = temp
            pf.color = pf.country.color
            pf.save()
            curr_player = Player.objects.filter(name=pf.name, game=temp)[0]
            #Creates Hexes
            h = HexList()
            h.apply(temp, curr_player)
            hex_list = Hexes.objects.filter(game=temp, start_country=curr_player.country)
            for i in hex_list:
                i.controller = curr_player
                i.save()
            #Creates Policies
            p2 = PolicyList()
            p2.add_policies(curr_player, temp, request)
            #Creates tariff form associated with user.
            formt = AddTariffForm(request.POST)
            formt = formt.save(commit=False)
            formt.curr_player = curr_player
            formt.game = temp
            formt.name = curr_player.name
            formt.save()
            #Adds an IndTariff object to each player's tariff object.
            tariffList = Tariff.objects.filter(game=temp)
            for p in tariffList:
                iForm = AddIndTariffForm(request.POST)
                itf = iForm.save(commit=False)
                itf.controller = p
                itf.key = curr_player
                itf.save()
            #game_name = form.cleaned_data.get('game_name')
            #Uncomment for single-player games
            #temp.GameEngine.start_capital(temp)
            messages.success(request, f'New Game created!')
            return redirect('app-game', g=temp.name, player=curr_player.name)
        else:
            messages.success(request, f'Choose another name. An existing game already has this name.')
            return redirect('app-new_game')
    else:
        form = NewGameForm(instance=request.user)
        player_form = JoinGameForm(instance=request.user)
    #import pdb; pdb.set_trace()
    context = {
        'form': form,
        'player_form': player_form
    }
    return render(request, 'App/new_game.html', context)

@login_required
def joinGame(request, g):
    gameList = Game.objects.all()
    for k in gameList:
        if str(k) == g:
            temp = k
    p = Player.objects.filter(user=request.user, game=temp)
    if len(p) > 0:
        return redirect('app-game', g=temp.name, player=p[0].name)

    if request.method == 'POST':
        form = JoinGameForm(request.POST)
        if form.is_valid():
            #Creates player object associated with this user and game.
            f = form.save(commit=False)
            f.host = False 
            f.user = request.user
            f.game = temp
            f.color = f.country.color
            f.save()
            curr_player = Player.objects.filter(name=f.name, game=temp)[0]
            #Creates Policies
            p2 = PolicyList()
            p2.add_policies(curr_player, temp, request)
            #Adds control to related hexes
            hex_list = Hexes.objects.filter(game=temp, start_country=curr_player.country)
            for i in hex_list:
                i.controller = curr_player
                i.save()
            #Creates Tariff object associated with player and game.
            formt = AddTariffForm(request.POST)
            formt = formt.save(commit=False)
            formt.curr_player = curr_player
            formt.name = curr_player.name
            formt.game = temp
            formt.save()
            #Adds an IndTariff object to each player's tariff object.
            tariffList = Tariff.objects.filter(game=temp)
            for p in tariffList:
                if p.curr_player.game == temp:
                    itf = IndTariff(controller=p, key=curr_player, tariffAm=0)
                    itf.save()
                    """iForm = AddIndTariffForm(request.POST)
                    itf = iForm.save(commit=False)
                    itf.controller = p
                    itf.key = curr_player
                    itf.save()"""
            temp.curr_num_players += 1
            temp.save()
            #Remove this if game isn't 2 player
            #temp.GameEngine.start_capital(temp)
            if temp.num_players == temp.curr_num_players:
                temp.GameEngine.start_capital(temp)
            messages.success(request, f'Successfully Joined a Game!')
            return redirect('app-game', g=temp.name, player=curr_player.name)
    else:
        form = JoinGameForm(instance=request.user)
    return render(request, 'App/join_game.html', {'form': form})

"""def game(request, g, player):
    g = Game.objects.filter(name=g)[0]
    player = Player.objects.filter(name=player)[0]
    tar = Tariff.objects.filter(game=g, curr_player=player)[0]
    k = IndTariff.objects.filter(controller=tar)
    if request.method == 'POST':
        for f in k:
            v = IndTariffForm(request.POST, instance=f)
            if v.is_valid():
                v.save()
        messages.success(request, f'Tariffs Successfully submitted!')
        #return redirect('app-lobby')
    indForms = []
    players = []
    IndFormSet = formset_factory(IndTariffForm)
    for f in k:
        v = IndTariffForm(instance=f)
        indForms.append((v, f.key))
    context = {
        'indForms': indForms
    }
    return render(request, 'App/Game.html', context)"""
@login_required
def game(request, g, player):
    gtemp = g
    ptemp = player
    g = Game.objects.filter(name=g)[0]
    player = Player.objects.filter(name=player)[0]
    tar = Tariff.objects.filter(game=g, curr_player=player)[0]
    k = IndTariff.objects.filter(controller=tar)
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm'], extra=0)
    context = {}
    if request.method == 'POST':
        #Submits the Tariff formset
        IndFormSet = IndFormSet(request.POST, queryset=IndTariff.objects.filter(controller=tar))
        for f in IndFormSet:
            if f.is_valid():
                f.save()
        #Government Spending Form
        govForm2 = GovernmentSpendingForm(request.POST, instance=player)
        if govForm2.is_valid():
            govForm2.save()
        else:
            messages.warning(request, f'Government spending total must not be more than 1')
        #Runs ready form for whether ready for moving onto next turn
        ready = NextTurn(request.POST, instance=player)
        if ready.is_valid():
            ready.save()
        messages.success(request, f'Turn succesfully submitted!')
        #Runs game run_engine function if player is host and all players are ready
        if player.host:
            all_players = Player.objects.filter(game=g)
            ready_next_round = True
            for p in all_players:
                if not p.ready:
                    ready_next_round = False
            if ready_next_round:
                temp = g.GameEngine.run_engine(g)
                g.save()
                #g.GameEngine = temp[0]
                messages.success(request, f'Turn succesfully run!')
                return redirect('app-game', g=g.name, player=str(player))
    #Creates the tariff formset and titles for it.
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm'], extra=0)
    titles = {}
    count = 1
    for f in k:
        #v = IndTariffForm(instance=f)
        titles[count] = f.key
        count += 1
    IFS = IndFormSet(queryset=IndTariff.objects.filter(controller=tar))
    #for i in IFS:
    #    print(i.label)
    govForm = GovernmentSpendingForm(instance=player)
    next_turn = NextTurn(instance=player)
    context = {
        'indForms': IFS,
        'titles': titles,
        'test': {'a':'new', 'b':'new2'},
        'readyForm':next_turn,
        'game':gtemp,
        'player':ptemp,
        'govForm':govForm,
        'GovMoney':player.get_country().money[5],
        'GovSavings':player.get_country().Government_Savings,
        'GovDebt':player.get_country().Bonds,
        'CurrencyReserves':g.GameEngine.printCurrencyReserves(),
        'graph':player.GoodsPerCapita,
        'govBudget':player.GovBudget
    }
    return render(request, 'App/game.html', context)

#loads the army map
@login_required
def map(request, g, p, l, lprev):
    #Col used for storing the map colors in a 2d array
    col = []
    #one side of 2d side
    size = 5
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    #Loads the army form on post
    if request.method == 'POST':
        #v = Army.objects.filter(game=g,location=f.location)
        form = ArmyForm(request.POST)
        if form.is_valid():
            f = form.save(commit=False)
            #if l != 'null':
                #f.Hexes = l
            #Creates player object associated with this user and game.
            #f = form.save(commit=False)
            #v = Army.objects.filter(game=g,location=f.location)
            f.controller = p
            f.game = g
            f.save()
    #Gets the different colors of the hexes and the stats of the hexes
    hexColor = Hexes.objects.filter(game=g)
    armies = Army.objects.filter(game=g)
    count = 0
    col.append([])
    info = [0 for i in range(0,25)]
    row = 0
    for hC in hexColor:
        col[row].append(hC.color)
        a = Army.objects.filter(game=g, location=hC)
        army_size = 0
        if not a:
            a = ""
        else:
            army_size = a[0].size
            a = a[0].name
        info[hC.xLocation+hC.yLocation*5] = [hC.population, hC.capital, hC.controller.name, a, army_size, hC.color]
        count += 1
        if count >= size:
            count = 0
            row += 1
            col.append([])
    #Creates the map jquery script
    hexmap = create_map(hexColor)

    #Stores col and info in json
    json_list = json.dumps(col)
    info_list = json.dumps(info)
    #If lprev is not null an army is selected and it moves the army if it is a valid move.
    if lprev != 'null':
        h = Hexes.objects.filter(game=g, hexNum=lprev)[0]
        v = Army.objects.filter(game=g,location=h)
        h2 = Hexes.objects.filter(game=g, hexNum=l)[0]
        v = v[0]
        if v.moved:
            messages.warning(request, f'This army has already been moved!')
            return redirect('map', gtemp, ptemp, 'null', 'null')
        if v.naval and not h2.water:
            messages.warning(request, f'A naval force cannot move on land!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        if not v.naval and h2.water:
            messages.warning(request, f'A land force cannot move on water!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        if calculate_distance(h.xLocation, h.yLocation, h2.xLocation, h2.yLocation) > v.max_movement:
            messages.warning(request, f'This army cannot move that far!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        f = ArmyForm(instance=v)
        form = f.save(commit=False)
        form.location = h2
        form.moved = True
        form.save()
        return redirect('map', gtemp, ptemp, 'null', 'null')
    #data = serializers.serialize("json", <col>)
    #If a tiles hasn't been selected load regular army form
    if l == 'null':
        f = ArmyForm()
    else:
        #If a tiles has been selected, load that particular army if an army is on it, 
        #if not then load a basic Army form with that location defaulted into the form.
        h = Hexes.objects.filter(game=g, hexNum=l)[0]
        v = Army.objects.filter(game=g,location=h)
        if not v:
            f = ArmyForm(initial={'location':h})
        else:
            v = v[0]
            print(v)
            f = ArmyForm(instance=v)
            if v.controller != p:
                messages.warning(request, f'You cannot move another players army!')
                f = ArmyForm()
                return redirect('map', gtemp, ptemp, 'null', 'null')
    context = {
        'ColorMap':json_list,
        'hi':'hello',
        'info':info_list,
        'form':f,
        'game':gtemp,
        'player':ptemp,
        'prevNum':l,
        'hexmap':hexmap
    }
    return render(request, 'App/map.html', context)

#Creates a jquery hexmap
def create_map(hex_list):
    message = ''#'"hexes": { \n'
    last = hex_list[len(hex_list) - 1]
    for i in hex_list:
        message += '"'+str(i.hexNum)+'"' + ':{"n":"'+i.name+'","q":'+str(i.xLocation)+',"r":'+str(i.yLocation)+'}'
        if i != last:
            message += ',\n'
    return message

def graph(request, g, p):
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    context = {
        'GoodsPerCapita':p.GoodsPerCapita,
        'Inflation':p.Inflation,
        'RealGDP':p.RealGDP,
        'Employment':p.Employment,
        'tradeBalance':p.tradeBalance,
        'GDPPerCapita':p.GDPPerCapita,
        'InterestRate':p.InterestRate,
        'Capital':p.Capital,
        'GoodsProduction':p.GoodsProduction,
        'GDP':p.GDP,
        'GDPGrowth':p.GDPGrowth,
        'game':gtemp,
        'player':ptemp
    }
    return render(request, 'App/graphs.html', context)

def policies(request, g, p):
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    policy_list = PolicyGroup.objects.filter(game=g, player=p)
    titles = {}
    group_titles = {}
    Effects = {}
    counter = 1
    PFS = []
    PolicyFormArray = []
    for pg in policy_list:
        #PolicyFormSet = modelformset_factory(Policy, fields=['applied'], extra=0)
        PolicyFormArray.append(modelformset_factory(Policy, fields=['applied'], extra=0))
    if request.method == 'POST':
        #Submits the Tariff formset
        for pg in policy_list:
            PolicyFormSet2 = PolicyFormArray[counter - 1](request.POST, queryset=Policy.objects.filter(policy_group=pg), prefix='Policy'+str(counter))
            ap = 0
            for f in PolicyFormSet2:
                if f.is_valid():
                    f2 = f.save(commit=False)
                    if f2.applied == True:
                        ap += 1
            if ap > 1:
                messages.warning(request, f'You cannot select more than one of the same policy type!')
                return redirect('app-policies', gtemp, ptemp)
            else:
                PolicyFormSet2.save()
            counter += 1
    count = 1
    counter = 1
    for pg in policy_list:
        #PolicyFormSet = modelformset_factory(Policy, fields=['applied'], extra=0)
        t = {}
        ef = {}
        titles[counter] = t
        Effects[counter] = ef
        group_titles[counter] = pg.name
        k = Policy.objects.filter(policy_group=pg)
        for f in k:
            #v = IndTariffForm(instance=f)
            ef_list = {}
            t[count] = f.name
            ef[count] = ef_list
            count += 1
            #Gets the effects of a policy
            all_fields = f._meta.get_fields() #_meta.fields
            c = 1
            for a in all_fields:
                if isinstance(a, FloatField):
                    n = a.name
                    value = getattr(f, n)
                    print(value)
                    if value > 0.00001 or value < -0.00001:
                        ef_list[c] = str(n) + ": " + str(value)
                        c += 1
        PFS.append(PolicyFormArray[counter - 1](queryset=Policy.objects.filter(policy_group=pg), prefix='Policy'+str(counter)))
        count = 1
        counter += 1

    context = {
        'group_titles':group_titles,
        'titles':titles,
        'effects':Effects,
        'policyForms':PFS,
        'game':gtemp,
        'player':ptemp
    }
    return render(request, 'App/policies.html', context)

#Returns the politics page
def Politics(request, g, p):
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    policy_list = PolicyGroup.objects.filter(game=g, player=p)
    form = CreateFactionForm()

    context = {
        'group_titles':group_titles,
        'titles':titles,
        'game':gtemp,
        'player':ptemp
    }
    return render(request, 'App/policies.html', context)

#Calculates distance between two points
def calculate_distance(x1,y1,x2,y2):
    return abs(square(x2-x1) + square(y2-y1))

def square(x):
    return x*x

#Gets an item from a dictionary
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

#Switches control of a hex between two players (doesn't work yet)
def switch_hex(hex_num, player_to):
    h = Hexes.objects.filter(hexNum=hex_num)[0]
    f = HexForm(request.POST, instance=h)
    if f.is_valid():
        f.save(commit=False)
        f.controller = player_to
        f.color = player_to.color