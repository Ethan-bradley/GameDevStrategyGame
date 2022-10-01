from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, modelformset_factory
from .Game import GameEngine
from .models import Post
from .models import Game, Player, Building, IndTariff, Tariff, Hexes, Army, Policy, PolicyGroup, Country, PlayerProduct, Product, MapInterface, Notification, GraphInterface, GraphCountryInterface
from .forms import BuildingForm, NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, HexForm, ArmyForm, GovernmentSpendingForm, PolicyForm, PolicyFormSet, AddProductForm, AddPlayerProductForm, MapInterfaceForm, GraphInterfaceForm, GraphCountryInterfaceForm
from django.views.generic.edit import CreateView
from django.apps import apps
import json
from .HexList import HexList
from .HexList2 import HexList2
from .PolicyList import PolicyList
from django.db.models.fields import *
import plotly.graph_objects as go
import plotly.express as px
from .budgetgraph import budget_graph
from .helper import add_players, add_neutral
from django.db import reset_queries
import math

def home(request):
	context = {
		'posts': Post.objects.all()
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
    context = {
        'games': Game.objects.all()
    }
    return render(request, 'App/lobby.html', context)

@login_required
def new_game(request):
    if request.method == 'POST':
        form = NewGameForm(request.POST)
        player_form = JoinGameForm(request.POST)
        if form.is_valid():
            pf = player_form.save(commit=False)
            #Creates the game object
            f = form.save(commit=False)
            f.host = request.user
            if f.num_players <= 5 and f.num_players != -1:
                if pf.country.large:
                    messages.warning(request, f'Choose another country. This country is not available for the 5 person map.')
                    return redirect('app-new_game')
                f.GameEngine = GameEngine(6, ['UK','Germany','France','Spain','Italy','Neutral'])
            else:
                #f.GameEngine = GameEngine(15, ['UK','Germany','France','Spain','Italy','Poland','Sweden','Egypt','Algeria','Turkey','Ukraine','Russia','Iran','Saudi Arabia','Neutral'])
                f.board_size = 14
            f.curr_num_players = 1
            if f.num_players > 5 or f.num_players == -1:
                #job = q.enqueue(create_countries, 'http://heroku.com', on_success=organize_countries)
                f.GameEngine = GameEngine(15,['UK', 'Germany', 'France', 'Spain', 'Italy', 'Poland', 'Sweden', 'Egypt','Algeria', 'Turkey', 'Ukraine', 'Russia', 'Iran', 'Saudi Arabia', 'Neutral'])
            f.save()
            #Saves game name in temporary variable
            g = f.name
            gameList = Game.objects.all()
            for k in gameList:
                if str(k.name) == g:
                    temp = k
            #Creates a player associated with this user and game and makes them the host.
            pf.host = True
            pf.user = request.user
            pf.game = temp
            pf.color = pf.country.color
            pf.save()
            curr_player = Player.objects.filter(name=pf.name, game=temp)[0]
            #Creates Map Interface
            MapInterface.objects.create(game=temp,controller=curr_player)
            GraphInterface.objects.create(game=temp,controller=curr_player)
            if f.num_players <= 5 and f.num_players != -1:
                GraphCountryInterface.objects.create(game=temp,controller=curr_player, country=curr_player.country)
            else:
                GraphCountryInterface.objects.create(game=temp, controller=curr_player, country=curr_player.country, large=True)
            #Creates Hexes
            if f.num_players <= 5 and f.num_players != -1:
                h = HexList()
            else:
                h = HexList2()
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
            formt = AddPlayerProductForm(request.POST)
            formt = formt.save(commit=False)
            formt.curr_player = curr_player
            formt.game = temp
            formt.name = curr_player.name
            formt.save()
            #Adds an IndTariff object to each player's tariff object.
            productList = ['Food','Consumer Goods','Steel','Machinery','Iron','Wheat','Coal','Oil']
            for product in productList:
                iForm = AddProductForm(request.POST)
                itf = iForm.save(commit=False)
                itf.controller = PlayerProduct.objects.filter(game=temp, curr_player=curr_player.id)[0]
                itf.key = curr_player
                itf.name = product
                itf.save()
            #game_name = form.cleaned_data.get('game_name')
            #Uncomment for single-player games
            #temp.GameEngine.start_capital(temp)

            if temp.num_players == 1:
                add_players(temp, True)
            elif temp.num_players == -1:
                add_players(temp, False)
                #add_neutral(temp)
            #else:
            add_neutral(temp)
            #import pdb; pdb.set_trace();
            if temp.num_players == temp.curr_num_players and temp.num_players < 5 and temp.num_players != -1:
                temp.GameEngine.start_capital(temp)
                temp.GameEngine.run_start_trade(temp)
                temp.save()
            messages.success(request, f'New Game created!')
            return redirect('map', temp.name, temp.name, 'null', 'null')
            #return redirect('app-game', g=temp.name, player=curr_player.name)
        else:
            messages.warning(request, f'Choose another name. An existing game already has this name.')
            return redirect('app-new_game')
    else:
        form = NewGameForm(instance=request.user)
        player_form = JoinGameForm(instance=request.user)
    #import pdb; pdb.set_trace()
    context = {
        'form': form,
        'player_form': player_form
    }
    reset_queries()
    return render(request, 'App/new_game.html', context)

@login_required
def runNext(request, g):
    temp = Game.objects.filter(name=g)[0]
    temp.GameEngine.run_more_countries(15)
    temp.GameEngine.start_capital(temp)
    #temp.GameEngine.run_start_trade(temp)
    temp.save()

@login_required
def runNext2(request, g):
    temp = Game.objects.filter(name=g)[0]
    #temp.GameEngine.run_start_trade(temp, 1)
    temp.GameEngine.run_start_trade(temp, 4)
    temp.save()

@login_required
def runNext3(request, g):
    temp = Game.objects.filter(name=g)[0]
    temp.GameEngine.run_start_trade(temp, 3)
    temp.save()

@login_required
def joinGame(request, g):
    gameList = Game.objects.all()
    for k in gameList:
        if str(k) == g:
            temp = k
    p = Player.objects.filter(user=request.user, game=temp)
    if len(p) > 0:
        if len(p) > 1:
            p = Player.objects.filter(user=request.user, game=temp, robot=False)
            return redirect('map', temp.name, p[0].name, 'null', 'null')
            #return redirect('app-game', g=temp.name, player=temp.name)
        if temp.num_players == 1: 
            return redirect('map', temp.name, p[0].name, 'null', 'null')
            #return redirect('app-game', g=temp.name, player=temp.name)
        else:
            return redirect('map', temp.name, p[0].name, 'null', 'null')
            #return redirect('app-game', g=temp.name, player=p[0].name)
    if request.method == 'POST':
        form = JoinGameForm(request.POST)
        if form.is_valid():
            all_players = Player.objects.filter(game=temp)
            countryList = []
            for player in all_players:
                countryList.append(player.country)
            #Creates player object associated with this user and game.
            f = form.save(commit=False)
            if f.country in countryList:
                form = JoinGameForm(instance=request.user)
                messages.warning(request, f'A player in this game has already claimed that country.')
                return render(request, 'App/join_game.html', {'form': form})
            if f.name in Player.objects.all().values_list('name',flat=True):
                form = JoinGameForm(instance=request.user)
                messages.warning(request, f'A player already has that name.')
                return render(request, 'App/join_game.html', {'form': form})
            if temp.num_players <= 5 and f.country.large:
                messages.warning(request, f'Choose another country. This country is not available for the 5 person map.')
                return render(request, 'App/join_game.html', {'form': form})
            f.host = False
            f.user = request.user
            f.game = temp
            f.color = f.country.color
            f.save()
            curr_player = Player.objects.filter(name=f.name, game=temp)[0]
            #Creates Map Interface
            MapInterface.objects.create(game=temp,controller=curr_player)
            GraphInterface.objects.create(game=temp,controller=curr_player)
            GraphCountryInterface.objects.create(game=temp,controller=curr_player, country=curr_player.country)
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
            #Gets list of players before adding this player for adding tarriff forms
            player_list = Player.objects.filter(game=temp).exclude(id=curr_player.id)
            #Adds existing players TariffObjects to this player:
            control = Tariff.objects.filter(game=temp, curr_player=curr_player)[0]
            for p in player_list:
                itf = IndTariff(controller=control, key=p, tariffAm=0)
                itf.save()
            #Adds an IndTariff object related to this player to each existing player's tariff object.
            tariffList = Tariff.objects.filter(game=temp)
            for p in tariffList:
                if p.curr_player.game == temp:
                    itf = IndTariff(controller=p, key=curr_player, tariffAm=0)
                    itf.save()
            formt = AddPlayerProductForm(request.POST)
            formt = formt.save(commit=False)
            formt.curr_player = curr_player
            formt.game = temp
            formt.name = curr_player.name
            formt.save()
            #Adds an IndTariff object to each player's tariff object.
            productList = ['Food','Consumer Goods','Steel','Machinery','Iron','Wheat','Coal','Oil']
            for product in productList:
                iForm = AddProductForm(request.POST)
                itf = iForm.save(commit=False)
                itf.controller = PlayerProduct.objects.filter(game=temp, curr_player=curr_player.id)[0]
                itf.key = curr_player
                itf.name = product
                itf.save()
            temp.curr_num_players += 1
            temp.save()
            #Remove this if game isn't 2 player
            #temp.GameEngine.start_capital(temp)
            if temp.num_players == temp.curr_num_players:
                temp.GameEngine.start_capital(temp)
                temp.GameEngine.run_start_trade(temp)
            messages.success(request, f'Successfully Joined a Game!')
            return redirect('map', temp.name, curr_player.name, 'null', 'null')
            #return redirect('app-game', g=temp.name, player=curr_player.name)
    else:
        form = JoinGameForm(instance=request.user)
    return render(request, 'App/join_game.html', {'form': form})

def runArmy(request, g):
    g = Game.objects.filter(name=g)[0]
    g.GameEngine.game_combat(g)
    g.save()

def fixVars(request, g):
    g = Game.objects.filter(name=g)[0]
    g.GameEngine.fix_variables()
    g.save()
#loads the army map
@login_required
def map(request, g, p, l, lprev):
    reset_queries()
    #Col used for storing the map colors in a 2d array
    col = []
    #one side of 2d side
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    player = p
    size = g.board_size
    #Finds total size of all armies of this player.
    total_armies = Army.objects.filter(game=g, controller=p)
    total_size = 0
    for army in total_armies:
        total_size += army.size
    #Loads the army form on post
    t = MapInterface.objects.filter(game=g,controller=p)[0]
    if request.method == 'POST':
        if 'mode' in request.POST:
            mi2 = MapInterfaceForm(request.POST, instance=t)
            if mi2.is_valid():
                mi2.save()
                return redirect('map', gtemp, ptemp, 'null', 'null')
        else:
             #Runs ready form for whether ready for moving onto next turn
            ready = NextTurn(request.POST, instance=player)
            if ready.is_valid():
                ready.save()
            messages.success(request, f'Turn succesfully submitted!')
            #Runs game run_engine function if player is host and all players are ready
            if player.host:
                all_players = Player.objects.filter(game=g)
                ready_next_round = True
                #import pdb; pdb.set_trace();
                if g.num_players > 1 and g.num_players < 6:
                    for p in all_players:
                        if p.robot == False and not p.ready:
                            ready_next_round = False
                else:
                    if not player.ready:
                        ready_next_round = False
                if ready_next_round:
                    for i in range(0,g.years_per_turn - 1):
                        g.GameEngine.run_engine(g, False)
                    temp = g.GameEngine.run_engine(g)
                    g.save()
                    messages.success(request, f'Turn succesfully run!')
                    return redirect('map', gtemp, ptemp, 'null', 'null')
            #Processes building form
            if 'building_type' in request.POST:
                buildingForm = BuildingForm(request.POST)
                if buildingForm.is_valid():
                    buildingFormTemp = buildingForm.save(commit=False)
                    buildingFormTemp.game = g
                    buildingFormTemp.player_controller = player
                    if buildingFormTemp.applyCost():
                        buildingFormTemp.save()
                        return redirect('map', gtemp, ptemp, 'null', 'null')
                    else:
                        messages.warning(request, f'You do not have enough resources to construct this building!')
                        return redirect('map', gtemp, ptemp, 'null', 'null')
            if l != 'null':
                h = Hexes.objects.filter(game=g, hexNum=l)[0]
                v = Army.objects.filter(game=g,location=h, controller=p)
                if len(v) > 0:
                    form = ArmyForm(request.POST, instance=v[0])
                else:
                    form = ArmyForm(request.POST)
            else:
                h = None
                form = ArmyForm(request.POST)
            if form.is_valid():
                f = form.save(commit=False)
                v = Army.objects.filter(game=g,location=f.location, controller=p)
                f.controller = p
                f.game = g
                s = f.size
                if s < 0:
                    messages.warning(request, f'You cannot have an army with negative size!')
                    return redirect('map', gtemp, ptemp, 'null', 'null')
                if f.location.controller != p:
                    messages.warning(request, f'You cannot build an army in another Players territory!')
                    return redirect('map', gtemp, ptemp, 'null', 'null')
                if h == None:
                    messages.warning(request, f'You have not specified a location for this army!')
                    return redirect('map', gtemp, ptemp, 'null', 'null')
                if f.naval and not h.water:
                    messages.warning(request, f'A naval force cannot be built on land!')
                    return redirect('map', gtemp, ptemp, 'null', 'null')
                if lprev == 'null':
                    if len(v) == 0:
                        if total_size + s > 1000000:
                            messages.warning(request, f'The total size of all your armies combined cannnot be more than 1m!')
                            return redirect('map', gtemp, ptemp, 'null', 'null')
                        if player.MilitaryAm - s >= 0:
                            player.MilitaryAm -= s
                            player.save()
                        else:
                             messages.warning(request, f'You do not have enough Military resources to build this Army!')
                             return redirect('map', gtemp, ptemp, 'null', 'null')
                        if player.MilitaryAm - s - (total_size + s)*0.1 < 0:
                            messages.warning(request, f'Building this army does not leave enough remaining for army maintenace, which puts you at risk of army rebellion.')

                    else:
                        if s == 0:
                            v[0].delete()
                            messages.success(request, f'Army succesfully disbanded!')
                            return redirect('map', gtemp, ptemp, 'null', 'null')
                        s = s - v[0].size
                        if total_size + s > 1000000:
                            messages.warning(request, f'The total size of all your armies combined cannnot be more than 1m!')
                            return redirect('map', gtemp, ptemp, 'null', 'null')
                        if player.MilitaryAm - s >= 0:
                            player.MilitaryAm -= s
                            player.save()
                        else:
                            f.size = v[0].size
                            messages.warning(request, f'You do not have enough military resources to expand this Army!')
                            return redirect('map', gtemp, ptemp, 'null', 'null')
                        if player.MilitaryAm - s - (total_size + s)*0.1 < 0:
                            messages.warning(request, f'Expanding this army does not leave enough remaining for army maintenace, which puts you at risk of army rebellion.')
                else:
                    player.MilitaryAm -= s
                    player.save()
                f.moved = True
                f.save()
    #Gets the different colors of the hexes and the stats of the hexes
    hexColor = Hexes.objects.filter(game=g)
    armies = Army.objects.filter(game=g)
    count = 0
    col.append([])
    info = [0 for i in range(0,g.board_size*g.board_size)]
    row = 0
    #import pdb; pdb.set_trace()
    for hC in hexColor:
        col[row].append(hC.color)
        a = Army.objects.filter(game=g, location=hC)
        buildings = Building.objects.filter(game=g, location=hC)
        army_size = ""
        army_name = ""
        #Adds the building's symbol to the hex display text.
        for building in buildings:
            army_name += building.getSymbol() + ' '
        #Adds the armies name and size to the hex display text.
        if not a:
            a = ""
            army_size = "---"
        else:
            for army in a:
                army_size += (army.name+": "+str(army.size))
                if army.naval:
                    army_name += "[ ⚓"+army.name
                else:
                    army_name += "[ ⚔️"+army.name
                if army.moved == False:
                    army_name += " ✅"
                army_name += "] \n "
        #import pdb; pdb.set_trace()
        if hC.color != '#3262a8' and t.mode == "RE":
            color =  "#"+str(hex((10 + hC.iron*2 + hC.wheat*4)))[2]+str(hex((10 + hC.iron*2 + hC.wheat*4)))[2]+ str(hex(10+hC.wheat*4+hC.coal))[2] + str(hex(10+hC.wheat*4 + hC.coal))[2] + str(hex(10 + hC.coal*2 + hC.oil*2))[2] + str(hex(10 + hC.coal*2 + hC.oil*2))[2]
            print(color)
        else:
            color = hC.color
        info[hC.xLocation+hC.yLocation*g.board_size] = [str(hC.population)+'k', hC.capital, hC.controller.name, army_name, army_size, color, hC.iron, hC.wheat, hC.coal, hC.oil]
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
    #Map Mode Form
    mi = MapInterfaceForm(instance=t)
    #If lprev is not null an army is selected and it moves the army if it is a valid move.
    if lprev != 'null':
        h = Hexes.objects.filter(game=g, hexNum=lprev)[0]
        v = Army.objects.filter(game=g,location=h)
        
        h2 = Hexes.objects.filter(game=g, hexNum=l)[0]
        if len(v) == 0:
            return redirect('map', gtemp, ptemp, 'null', 'null')
        v = v[0]
        if v.moved:
            messages.warning(request, f'This army has already been moved!')
            return redirect('map', gtemp, ptemp, 'null', 'null')
        if v.naval and not h2.water:
            messages.warning(request, f'A naval force cannot move on land!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        #    return redirect('map', gtemp, ptemp, lprev, 'null')
        if calculate_distance(h.xLocation, h.yLocation, h2.xLocation, h2.yLocation) > v.max_movement:
            messages.warning(request, f'This army cannot move that far!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        f = ArmyForm(instance=v)
        form = f.save(commit=False)
        form.location = h2
        if h2 != h:
            form.moved = True

        form.save()
        return redirect('map', gtemp, ptemp, 'null', 'null')
    #If a tiles hasn't been selected load regular army form
    if l == 'null':
        f = ArmyForm()
        buildingForm = BuildingForm()
    else:
        #If a tiles has been selected, load that particular army if an army is on it, 
        #if not then load a basic Army form with that location defaulted into the form.
        h = Hexes.objects.filter(game=g, hexNum=l)[0]
        v = Army.objects.filter(game=g,location=h, controller=player)
        buildingForm = BuildingForm(initial={'location':h})
        if not v:
            if h.controller != player:
                messages.warning(request, f'You cannot build an army in another players territory!')
                return redirect('map', gtemp, ptemp, 'null', 'null')
            f = ArmyForm(initial={'location':h})
        else:
            v = v[0]
            print(v)
            f = ArmyForm(instance=v)
            if v.controller != p:
                messages.warning(request, f'You cannot move another players army!')
                f = ArmyForm()
                return redirect('map', gtemp, ptemp, 'null', 'null')
    next_turn = NextTurn(instance=player)
    militaryAm = player.MilitaryAm
    year = g.year
    context = {
        'country': player.country,
        'readyForm':next_turn,
        'money': player.money,
        'coal': player.coal,
        'iron': player.iron,
        'wheat': player.wheat,
        'oil':player.oil,
        'MilitaryAm':militaryAm,
        'ColorMap':json_list,
        'hi':'hello',
        'info':info_list,
        'CurrentYear':year,
        'form':f,
        'map_form':mi,
        'game':gtemp,
        'player':ptemp,
        'prevNum':l,
        'hexmap':hexmap,
        'maintenace':total_size*0.1,
        'resources':t.mode == "RE",
        'notifications': Notification.objects.filter(game=g, year__gt=year)[::-1],
        'board_size':g.board_size,
        'building_form':buildingForm
    }
    return render(request, 'App/map.html', context)

#Creates a jquery hexmap
def create_map(hex_list):
    message = ''
    last = hex_list[len(hex_list) - 1]
    for i in hex_list:
        message += '"'+str(i.hexNum)+'"' + ':{"n":"'+i.name+'","q":'+str(i.xLocation)+',"r":'+str(i.yLocation)+'}'
        if i != last:
            message += ',\n'
    return message

#Ignore functions below here
@login_required
def game(request, g, player):
    reset_queries()
    neutral_player2 = Player.objects.filter(name="Neutral")[0]
    neutral_player2.ready = True
    neutral_player2.save()
    def create_revenue_pie(country, player):
        data2 = {'Source':[country.money[0]*country.IncomeTax, country.money[4]*country.CorporateTax, country.TariffRevenue, country.Government_Savings*country.interest_rate],
        'Categories':['Income Tax','Corporate Tax','Tariffs','Interest']} 
        fig = px.pie(data2, values='Source', names='Categories', title="Revenues")
        fig.write_html("templates/App/graphs/"+player.name+"revenue.html")
    def create_expenditure_pie(country, player):
        data2 = {'Expenditure':[country.money[5]*country.GovGoods*country.EducationSpend, country.money[5]*country.GovGoods*(1-country.EducationSpend), country.money[5]*country.GovWelfare, country.money[8]*player.ScienceInvest, country.money[8]*player.InfrastructureInvest, country.GovDebt*country.interest_rate],
        'Categories':['Education','Military','Welfare','Science','Infrastructure','Interest']}
        fig = px.pie(data2, values='Expenditure', names='Categories', title="Expenditures")
        fig.write_html("templates/App/graphs/"+player.name+"expenditure.html")
    context = {}
    gtemp = g
    ptemp = player
    g = Game.objects.filter(name=g)[0]
    player = Player.objects.filter(name=player)[0]
    tar = Tariff.objects.filter(game=g, curr_player=player)[0]
    k = IndTariff.objects.filter(controller=tar)
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm','sanctionAm','moneySend','militarySend','nationalization'], extra=0)
    context = {}
    if request.method == 'POST':
        if 'form-0-tariffAm' in request.POST:
            #Submits the Tariff formset
            IndFormSet = IndFormSet(request.POST, queryset=IndTariff.objects.filter(controller=tar))
            for f in IndFormSet:
                if f.is_valid():
                    f.save()
            messages.success(request, f'Tarriffs succesfully submitted!')
            return redirect('app-game', g=g.name, player=str(player))
        else:
            #Government Spending Form
            govForm2 = GovernmentSpendingForm(request.POST, instance=player)
            if govForm2.is_valid():
                govForm2.save()
                player.projection_unloaded = False
                player.save()
            else:
                messages.warning(request, f'Error in Government Form')
                messages.warning(request, govForm2.errors['IncomeTax'])
                return redirect('app-game', g=g.name, player=str(player))
            #Runs ready form for whether ready for moving onto next turn
            ready = NextTurn(request.POST, instance=player)
            if ready.is_valid():
                ready.save()
            messages.success(request, f'Turn succesfully submitted!')
            #Runs game run_engine function if player is host and all players are ready
            if player.host:
                all_players = Player.objects.filter(game=g)
                ready_next_round = True
                if g.num_players > 1 and g.num_players < 6:
                    for p in all_players:
                        if not p.ready:
                            ready_next_round = False
                else:
                    if not player.ready:
                        ready_next_round = False
                if ready_next_round:
                    for i in range(0,g.years_per_turn - 1):
                        g.GameEngine.run_engine(g, False)
                    temp = g.GameEngine.run_engine(g)
                    g.save()
                    messages.success(request, f'Turn succesfully run!')
                    return redirect('app-game', g=g.name, player=str(player))
    #Creates the tariff formset and titles for it.
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm','sanctionAm','moneySend','militarySend','nationalization'], extra=0)
    titles = {}
    count = 1
    for f in k:
        titles[count] = f.key
        count += 1
    IFS = IndFormSet(queryset=IndTariff.objects.filter(controller=tar))
    #create_revenue_pie(player.get_country(),player)
    #create_expenditure_pie(player.get_country(),player)
    #budget_graph(player.get_country(), 17, "templates/App/graphs/"+player.name+"budgetgraph.html")
    govForm = GovernmentSpendingForm(instance=player)
    next_turn = NextTurn(instance=player)
    if player.projection_unloaded:
        player.projection_unloaded = False
        player.save()
    govSavings = player.money
    year = g.year
    
    context.update({
        'country': player.country,
        'indForms': IFS,
        'titles': titles,
        'test': {'a':'new', 'b':'new2'},
        'readyForm':next_turn,
        'game':gtemp,
        'player':ptemp,
        'govForm':govForm,
        'GovMoney':0,
        'GovSavings': govSavings,
        'GovDebt':0,
        'govBudget':"App/graphs/"+player.name+"expenditure.html",
        'govRevenue':"App/graphs/"+player.name+"revenue.html",
        'BudgetGraph':"App/graphs/"+player.name+"budgetgraph.html",
        'CurrentYear':year,
        'govSpending':round((player.ScienceInvest + player.InfrastructureInvest + player.Welfare + player.AdditionalWelfare + player.Education + player.Military)*100, 4),
        'notifications': Notification.objects.filter(game=g, year__gt=year)[::-1],
    })
    return render(request, 'App/game.html', context)

def trade(request, g, p):
    reset_queries()
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    player = p
    tar = Tariff.objects.filter(game=g, curr_player=player)[0]
    k = IndTariff.objects.filter(controller=tar)
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm','sanctionAm','moneySend','militarySend','nationalization'], extra=0)
    def create_trade_rate_graph(game, attribute, title2, country, start):
        data = {'Country': [],
        'Rate': [],
        'Year':[]
        }
        variable = getattr(game, attribute)
        for j in game.nameList:
            data['Rate'] += variable[country][j][start:]
            data['Year'] += [i for i in range(0,len(variable[country][j][start:]))]
            data['Country'] += [j for i in range(0,len(variable[country][j][start:]))]
        fig = px.line(data, x='Year', y='Rate',title=country+" "+title2, color="Country")
        fig.update_xaxes(title="Year")
        fig.update_yaxes(title=title2+" Amount")
        fig.write_html("templates/App/graphs/"+p.name+attribute+".html")
    t = GraphCountryInterface.objects.filter(game=g,controller=p)[0]
    data3 = []
    titles = []
    create_trade_rate_graph(g.GameEngine,"TarriffsArr","Tarriffs",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"SanctionsArr","Sanctions",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"ForeignAid","Foreign Aid",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"MilitaryAid","Military Aid",t.country.name,24)
    other_player = Player.objects.filter(country=t.country)[0]
    if request.method == 'POST':
        if 'form-0-tariffAm' in request.POST:
            #Submits the Tariff formset
            IndFormSet = IndFormSet(request.POST, queryset=IndTariff.objects.filter(controller=tar))
            for f in IndFormSet:
                if f.is_valid():
                    f.save()
            messages.success(request, f'Tarriffs succesfully submitted!')
            return redirect('app-trade', gtemp, ptemp)
        else:
            mi2 = GraphCountryInterfaceForm(request.POST, instance=t)
            if mi2.is_valid():
                mi2.save()
                return redirect('app-trade', gtemp, ptemp)
    else:
        mi = GraphCountryInterfaceForm(instance=t)
        #Creates the tariff formset and titles for it.
        IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm','sanctionAm','moneySend','militarySend','nationalization'], extra=0)
        tariff_titles = {}
        count = 1
        for f in k:
            #v = IndTariffForm(instance=f)
            tariff_titles[count] = f.key.country.name+": "+f.key.name
            count += 1
        IFS = IndFormSet(queryset=IndTariff.objects.filter(controller=tar))
    year = g.year
    context = {
        'indForms': IFS,
        'country': p.country,
        'tarriffgraph':"App/graphs/"+p.name+"TarriffsArr.html",
        'Sanctionsgraph':"App/graphs/"+p.name+"SanctionsArr.html",
        'ForeignAidgraph':"App/graphs/"+p.name+"ForeignAid.html",
        'MilitaryAidgraph':"App/graphs/"+p.name+"MilitaryAid.html",
        'game':gtemp,
        'player':ptemp,
        'notifications': Notification.objects.filter(game=g, year__gt=year)[::-1],
        'GraphInterface': mi,
        'data':data3,
        'tariff_titles':tariff_titles,
        'titles':titles,
    }
    reset_queries()
    return render(request, 'App/tradegraphs.html', context)

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
        'player':ptemp,
        'notifications': Notification.objects.filter(game=g)[::-1]
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

def delete(request, g, p):
    import os
    g = Game.objects.filter(name=g)[0]
    context = {
            'posts': Post.objects.all()
            #'posts': posts
        }
    try:
        p = Player.objects.filter(name=p)[0]
        all_players = Player.objects.filter(game=g)
        if p.host:
            for filename in os.listdir("templates/App/graphs"):
                for p in all_players:
                    if p.name in filename:
                        try:
                            os.remove(os.path.join("templates/App/graphs", filename))
                        except:
                            print("Error in removing files. File does not exist.")
            g.delete()
        else:

            messages.warning(request, f'Must be host in order to delete!')
            return render(request, 'App/home.html', context)
    except:
        g.delete()
    messages.success(request, f'Deletion of game was successfull!')
    return render(request, 'App/home.html', context)

#Calculates distance between two points
def calculate_distance(x1, y1, x2, y2):
    return abs(square(x2-x1) + square(y2-y1))

def square(x):
    return x*x

#Gets an item from a dictionary
from django.template.defaulttags import register
@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)