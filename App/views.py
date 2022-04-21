from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory, modelformset_factory
from .Game import GameEngine
from .models import Post
from .models import Game, Player, IndTariff, Tariff, Hexes, Army, Policy, PolicyGroup, Country, PlayerProduct, Product, MapInterface, Notification, GraphInterface, GraphCountryInterface
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, HexForm, ArmyForm, GovernmentSpendingForm, PolicyForm, PolicyFormSet, AddProductForm, AddPlayerProductForm, MapInterfaceForm, GraphInterfaceForm, GraphCountryInterfaceForm
from django.views.generic.edit import CreateView
from django.apps import apps
import json
from .HexList import HexList
from .HexList2 import HexList2
from .PolicyList import PolicyList
from django.db.models.fields import *
#from django.db.models import Q
#import django
import plotly.graph_objects as go
import plotly.express as px
from .budgetgraph import budget_graph
from .helper import add_players, add_neutral
from django.db import reset_queries
#import django_rq
#from rq import Queue
#from worker import conn
#import tracemalloc

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
    #tracemalloc.start()
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
            return redirect('app-game', g=temp.name, player=curr_player.name)
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
            return redirect('app-game', g=temp.name, player=temp.name)
        if temp.num_players == 1: 
            return redirect('app-game', g=temp.name, player=temp.name)
        else:
            return redirect('app-game', g=temp.name, player=p[0].name)
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
                    """iForm = AddIndTariffForm(request.POST)
                    itf = iForm.save(commit=False)
                    itf.controller = p
                    itf.key = curr_player
                    itf.save()"""
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
    ProductFormSet = modelformset_factory(Product, fields=['exportRestriction','subsidy'], extra=0)
    context = {}
    if request.method == 'POST':
        #import pdb; pdb.set_trace();
        if 'form-0-tariffAm' in request.POST:
            #Submits the Tariff formset
            IndFormSet = IndFormSet(request.POST, queryset=IndTariff.objects.filter(controller=tar))
            for f in IndFormSet:
                if f.is_valid():
                    f.save()
            messages.success(request, f'Tarriffs succesfully submitted!')
            return redirect('app-game', g=g.name, player=str(player))
        else:
            ProductFormSet = ProductFormSet(request.POST, queryset=Product.objects.filter(controller=PlayerProduct.objects.filter(game=g, curr_player=player.id)[0]))
            for f in ProductFormSet:
                if f.is_valid():
                    f.save()
            #Government Spending Form
            govForm2 = GovernmentSpendingForm(request.POST, instance=player)
            if govForm2.is_valid():
                govForm2.save()
                projection(gtemp, ptemp, context)
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
                    #g.GameEngine = temp[0]
                    messages.success(request, f'Turn succesfully run!')
                    return redirect('app-game', g=g.name, player=str(player))
    #Creates the tariff formset and titles for it.
    IndFormSet = modelformset_factory(IndTariff, fields=['tariffAm','sanctionAm','moneySend','militarySend','nationalization'], extra=0)
    ProductFormSet = modelformset_factory(Product, fields=['exportRestriction','subsidy'], extra=0)
    titles = {}
    count = 1
    for f in k:
        #v = IndTariffForm(instance=f)
        titles[count] = f.key
        count += 1
    IFS = IndFormSet(queryset=IndTariff.objects.filter(controller=tar))
    PFS = ProductFormSet(queryset=Product.objects.filter(controller=PlayerProduct.objects.filter(game=g, curr_player=player.id)[0]))
    products = Product.objects.filter(controller=PlayerProduct.objects.filter(game=g, curr_player=player.id)[0])
    product_title = {}
    count = 1
    for i in products:
        product_title[count] = i.name
        count += 1
    #for i in IFS:
    #    print(i.label)
    create_revenue_pie(player.get_country(),player)
    create_expenditure_pie(player.get_country(),player)
    budget_graph(player.get_country(), 17, "templates/App/graphs/"+player.name+"budgetgraph.html")
    govForm = GovernmentSpendingForm(instance=player)
    next_turn = NextTurn(instance=player)
    if player.projection_unloaded:
        projection(gtemp, ptemp, context)
        player.projection_unloaded = False
        player.save()
    else:
        projection(gtemp, ptemp, context, False)
    govDebt = round(player.get_country().Government_SavingsArr[player.get_country().time - 1] - player.get_country().GovDebtArr[
        player.get_country().time - 1], 2)
    
    context.update({
        'country': player.country,
        'indForms': IFS,
        'PFS':PFS,
        'titles': titles,
        'product_title':product_title,
        'test': {'a':'new', 'b':'new2'},
        'readyForm':next_turn,
        'game':gtemp,
        'player':ptemp,
        'govForm':govForm,
        'GovMoney':round(player.get_country().money[5],2),
        'GovSavings': govDebt,
        'GovDebt':round(govDebt/player.get_country().money[8], 2),
        'CurrencyReserves':g.GameEngine.printCurrencyExchange(),
        'graph':player.GoodsPerCapita,
        'govBudget':"App/graphs/"+player.name+"expenditure.html",
        'govRevenue':"App/graphs/"+player.name+"revenue.html",
        'BudgetGraph':"App/graphs/"+player.name+"budgetgraph.html",
        'CurrentYear':player.get_country().time - 18,
        'govRevenueGDP':round((player.get_country().money[5]/player.get_country().money[8])*100,1),
        'govSpending':round((player.ScienceInvest + player.InfrastructureInvest + player.Welfare + player.AdditionalWelfare + player.Education + player.Military)*100, 4),
        'govBalance': round(((player.get_country().money[5]/player.get_country().money[8]) - (player.ScienceInvest + player.InfrastructureInvest + player.Welfare + player.AdditionalWelfare + player.Education + player.Military))*100, 1),
        'notifications': Notification.objects.filter(game=g, year__gt=player.get_country().time - 23)[::-1],
    })
    return render(request, 'App/game.html', context)

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
    #import pdb; pdb.set_trace()
    t = MapInterface.objects.filter(game=g,controller=p)[0]
    if request.method == 'POST':
        if 'mode' in request.POST:
            mi2 = MapInterfaceForm(request.POST, instance=t)
            if mi2.is_valid():
                mi2.save()
                return redirect('map', gtemp, ptemp, 'null', 'null')
        else:
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
                #if l != 'null':
                    #f.Hexes = l
                #Creates player object associated with this user and game.
                #f = form.save(commit=False)
                #v = Army.objects.filter(game=g,location=f.location)
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
                        #country = p.get_country()
                        if total_size + s > 1000000:
                            messages.warning(request, f'The total size of all your armies combined cannnot be more than 1m!')
                            return redirect('map', gtemp, ptemp, 'null', 'null')
                        if p.get_country().Military - s >= 0:
                            g.GameEngine.modify_country_by_name(p.country.name, 'Military', p.get_country().Military - s)
                            g.save()
                        else:
                            f.size = 1
                        if p.get_country().Military - s - (total_size + s)*0.1 < 0:
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
                        if p.get_country().Military - s >= 0:
                            g.GameEngine.modify_country_by_name(p.country.name, 'Military', p.get_country().Military - s)
                            g.save()
                        else:
                            f.size = v[0].size
                        if p.get_country().Military - s - (total_size + s)*0.1 < 0:
                            messages.warning(request, f'Building this army does not leave enough remaining for army maintenace, which puts you at risk of army rebellion.')
                else:
                    p.modify_country('Military', p.get_country().Military - s)
                    g.save()
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
        army_size = ""
        army_name = ""
        if not a:
            a = ""
        else:
            for army in a:
                army_size += (army.name+": "+str(army.size))
                army_name += "["+army.name
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
        #if not v.naval and h2.water:
        #    messages.warning(request, f'A land force cannot move on water!')
        #    return redirect('map', gtemp, ptemp, lprev, 'null')
        if calculate_distance(h.xLocation, h.yLocation, h2.xLocation, h2.yLocation) > v.max_movement:
            messages.warning(request, f'This army cannot move that far!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        f = ArmyForm(instance=v)
        form = f.save(commit=False)
        form.location = h2
        #import pdb; pdb.set_trace()
        """s = form.size
        if s < 0:
            messages.warning(request, f'No negative armies!')
            return redirect('map', gtemp, ptemp, lprev, 'null')
        if p.get_country().Military - s >= 0:
            p.get_country().Military -= s;
            p.save()
        else:
            f.size = 1"""
        #p.save()
        if h2 != h:
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
        'country': player.country,
        'MilitaryAm':p.get_country().Military,
        'ColorMap':json_list,
        'hi':'hello',
        'info':info_list,
        'CurrentYear':player.get_country().time - 18,
        'form':f,
        'map_form':mi,
        'game':gtemp,
        'player':ptemp,
        'prevNum':l,
        'hexmap':hexmap,
        'maintenace':total_size*0.1,
        'resources':t.mode == "RE",
        'notifications': Notification.objects.filter(game=g, year__gt=player.get_country().time - 23)[::-1],
        'board_size':g.board_size
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
    reset_queries()
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    #if not os.path.exists('.'+g.GoodsPerCapita.url):
    #g.GameEngine.run_graphs(g)
    def create_wage_graph(country,p):
        fig = px.bar(x=country.HouseProducts + country.CapitalGoods + country.RawGoods + ['Education','Military','Researchers','Entrepreneurs'],y=country.create_wage_array(),title="Wages")
        fig.update_xaxes(title="Jobs")
        fig.update_yaxes(title="Pay")
        fig.write_html("templates/App/graphs/"+p.name+"wage.html")
    def create_job_graph(country, p):
        fig = px.bar(x=country.HouseProducts + country.CapitalGoods + country.RawGoods + ['Education','Military','Researchers','Entrepreneurs'],y=[sum(country.pop_matrix[i][20:70]) for i in range(0, len(country.pop_matrix))],title="Jobs")
        fig.update_xaxes(title="Jobs")
        fig.update_yaxes(title="Workers")
        fig.write_html("templates/App/graphs/"+p.name+"jobs.html")
    def create_prices_graph(country, p):
        fig = px.bar(x=country.HouseProducts + country.CapitalGoods + country.RawGoods,y=country.HousePrices + country.CapitalPrices + country.RawPrices,title="Prices")
        fig.update_xaxes(title="Products")
        fig.update_yaxes(title="Price")
        fig.write_html("templates/App/graphs/"+p.name+"prices.html")
    create_wage_graph(p.get_country(),p)
    create_job_graph(p.get_country(),p)
    #create_prices_graph(p.get_country(), p)
    t = GraphInterface.objects.filter(game=g,controller=p)[0]
    if request.method == 'POST':
        mi2 = GraphInterfaceForm(request.POST, instance=t)
        if mi2.is_valid():
            mi2.save()
            return redirect('app-graph', gtemp, ptemp)
    else:
        mi = GraphInterfaceForm(instance=t)
    def create_single_graph(country,start, var):
        data = getattr(country, var)[start:]
        labels = [i for i in range(0,len(data))]
        return data, labels
    capital, labels = create_single_graph(p.get_country(),17, 'CapitalArr')
    GoodsProduction, labels = create_single_graph(p.get_country(),17,'GoodsTotal')
    GDP, labels = create_single_graph(p.get_country(),17,'GDP')
    growth, labels = create_single_graph(p.get_country(),17,'RealGDPGrowth')
    print(labels)
    time = p.get_country().time - 18
    other = time - 2
    context = {
        'country': p.country,
        'GoodsPerCapita':p.GoodsPerCapita,
        'Inflation':p.Inflation,
        'RealGDP':p.RealGDP,
        'Employment':p.Employment,
        'tradeBalance':p.tradeBalance,
        'GDPPerCapita':p.GDPPerCapita,
        'InterestRate':p.InterestRate,
        'CurrentYear':time,
        'Capital':p.Capital,
        'GoodsProduction':p.GoodsProduction,
        'GDP':p.GDP,
        'GDPGrowth':p.GDPGrowth,
        'game':gtemp,
        'player':ptemp,
        'wageGraph':'App/graphs/'+p.name+'wage.html',
        'jobGraph':'App/graphs/'+p.name+'jobs.html',
        'pricesGraph':'App/graphs/'+p.name+'prices.html',
        'notifications': Notification.objects.filter(game=g, year__gt=other)[::-1],
        'GraphInterface': mi,
        'capital':capital,
        'labels':labels,
        'GoodsProduction':GoodsProduction,
        'GDP':GDP,
        'growth':growth
    }
    gamegraph(gtemp, ptemp, context, t, g)
    reset_queries()
    return render(request, 'App/graphs.html', context)

def gamegraph(g, p, context, graphmode, game):
    def create_compare_graph(attribute,title,trade,countries,start,  graph_dict={}, game=None, econattr=True):
        data = {'Country': [],
        title: [],
        'Year':[]
        }
        graph_dict['data'].append([])
        graph_dict['colors'].append([])
        graph_dict['line_titles'].append([])
        last_index = len(graph_dict['data']) - 1
        for j in range(0, len(trade.exchangeRateArr)):
            if hasattr(countries[j], attribute) and isinstance(getattr(countries[j], attribute), list):
                arr = getattr(countries[j], attribute)[start:]
            else:
                #import pdb; pdb.set_trace()
                arr = getattr(game, attribute)[j][start:]
                if len(arr) == 0:
                    continue
            data[title] += arr
            data['Year'] += [i for i in range(0,len(arr))]
            data['Country'] += [trade.CountryName[j] for i in range(0,len(arr))]
            graph_dict['data'][last_index].append(arr)
        graph_dict['line_titles'][last_index] = [trade.CountryName[i] for i in range(0,len(trade.CountryName))]
        graph_dict['colors'][last_index] = ['rgb('+str(color1)+','+str(color1*50 % 255)+','+str(255 - color1)+')' for color1 in range(0,255,int(255/len(countries)))]
        if econattr:
            #fig = px.line(data,x='Year', y=title,title=title, color="Country")
            #fig.update_xaxes(title="Year")
            #fig.update_yaxes(title=title)
            graph_dict['title'].append(title)
        else:
            graph_dict['title'].append(attribute)
        #if econattr:
        #fig.write_html("templates/App/"+title+".html")
    graph_dict = {
    'title':[],
    'data':[],
    'colors':[],
    'line_titles':[]
    }
    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    create_compare_graph("ScienceArr", "Science", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("UnemploymentArr", "Unemployment", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("EducationArr2", "Education", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("InfrastructureArr", "Infrastructure", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("PopulationArr", "Population", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("GDPPerCapita", "Real_GDP_Per_Capita_in_$US", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("CapitalArr", "Capital", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("GoodsPerCapita", "GoodsPerCapita", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("InflationTracker", "Inflation", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("ResentmentArr", "Resentment", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("EmploymentRate", "Employment", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("GoodsBalance", "TradeBalance", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("InterestRate", "Interest_Rate", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph("ConsumptionArr", "Consumption_Per_Capita", g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict)
    create_compare_graph(graphmode.mode, graphmode.get_mode_display(), g.GameEngine.TradeEngine, g.GameEngine.TradeEngine.CountryList, 17,graph_dict, game.GameEngine, False)
    
    context.update({
        'GoodsPerCapita':g.GoodsPerCapita,
        'Inflation':g.Inflation,
        'Resentment':g.Resentment,
        'Employment':g.Employment,
        'GoodsBalance':g.GoodsBalance,
        'InterestRate':g.InterestRate,
        'Consumption':g.Consumption,
        'game':gtemp,
        'player':ptemp,
        'notifications': Notification.objects.filter(game=g, year__gt=p.get_country().time - 23)[::-1],
        'budgetGraph': 'templates/App/budget2.html',
        'graphs': graph_dict['title'],
        'graph_dict': graph_dict,
    })
    #return render(request, 'App/gamegraphs.html', context)

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
    def create_exchange_rate_graph(trade, start):
        data = {'Country': [],
        'Exchange Rate': [],
        'Year':[]
        }
        for j in range(0, len(trade.exchangeRateArr)):
            data['Exchange Rate'] += trade.exchangeRateArr[j][start:]
            data['Year'] += [i for i in range(0,len(trade.exchangeRateArr[j][start:]))]
            data['Country'] += [trade.CountryName[j] for i in range(0,len(trade.exchangeRateArr[j][start:]))]
        fig = px.line(data, x='Year', y='Exchange Rate',title="Exchange Rates", color="Country")
        fig.update_xaxes(title="Year")
        fig.update_yaxes(title="Amount")
        fig.write_html("templates/App/exchange.html")
    def create_foreign_investment_pie(index, trade, title, data3):
        #matplotlib.rcParams.update({'font.size': 8})
        data = {'investment':trade.foreign_investment[index],
        'countries':trade.CountryName}
        fig = px.pie(data,values='investment',names='countries', title="Foreign Investment Abroad")
        fig.write_html("templates/App/foreign_investment.html")

        arr = []
        for i in range(0,len(trade.foreign_investment)):
            arr.append(trade.foreign_investment[i][index])
        data2 = {'investment':arr,
        'countries':trade.CountryName} 
        fig = px.pie(data2,values='investment',names='countries', title="Foreign Investment Domestically")
        fig.write_html("templates/App/foreign_investment_domestic.html")
        title.append("Foreign investment as % of GDP: "+str((sum(trade.foreign_investment[index])/trade.CountryList[index].money[8])*100))
        title.append("Foreign Inflows as % of GDP: "+str((trade.sum_foreign_investment(index, trade.foreign_investment)/trade.CountryList[index].money[8])*100))
        title.append("Domestic foreign investment as % of GDP: "+str((sum(arr)/trade.CountryList[index].money[8])*100))
        title.append("Domestic outflows due to foreign investment as % of GDP: "+str(((sum(arr)*trade.CountryList[index].interest_rate)/trade.CountryList[index].money[8])*100))
    def create_trade_rate_graph(game, attribute, title2, country, start):
        data = {'Country': [],
        'Rate': [],
        'Year':[]
        }
        variable = getattr(game, attribute)
        #import pdb; pdb.set_trace();
        for j in game.nameList:
            data['Rate'] += variable[country][j][start:]
            data['Year'] += [i for i in range(0,len(variable[country][j][start:]))]
            data['Country'] += [j for i in range(0,len(variable[country][j][start:]))]
        fig = px.line(data, x='Year', y='Rate',title=country+" "+title2, color="Country")
        fig.update_xaxes(title="Year")
        fig.update_yaxes(title=title2+" Amount")
        fig.write_html("templates/App/graphs/"+p.name+attribute+".html")
    t = GraphCountryInterface.objects.filter(game=g,controller=p)[0]
    create_exchange_rate_graph(g.GameEngine.TradeEngine,4)
    data3 = []
    titles = []
    create_foreign_investment_pie(g.GameEngine.TradeEngine.CountryName.index(p.country.name), g.GameEngine.TradeEngine, titles, data3)
    create_trade_rate_graph(g.GameEngine,"TarriffsArr","Tarriffs",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"SanctionsArr","Sanctions",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"ForeignAid","Foreign Aid",t.country.name,24)
    create_trade_rate_graph(g.GameEngine,"MilitaryAid","Military Aid",t.country.name,24)
    other_player = Player.objects.filter(country=t.country)[0]
    budget_graph(other_player.get_country(), 17, "templates/App/graphs/"+p.name+"tradebudgetgraph.html")
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
    context = {
        'indForms': IFS,
        'country': p.country,
        'tarriffgraph':"App/graphs/"+p.name+"TarriffsArr.html",
        'Sanctionsgraph':"App/graphs/"+p.name+"SanctionsArr.html",
        'ForeignAidgraph':"App/graphs/"+p.name+"ForeignAid.html",
        'MilitaryAidgraph':"App/graphs/"+p.name+"MilitaryAid.html",
        'Budgetgraph':"App/graphs/"+p.name+"tradebudgetgraph.html",
        'goodsBalance':g.GoodsBalance,
        'tradeBalance':p.tradeBalance,
        'game':gtemp,
        'player':ptemp,
        'notifications': Notification.objects.filter(game=g, year__gt=player.get_country().time - 23)[::-1],
        'GraphInterface': mi,
        'data':data3,
        'tariff_titles':tariff_titles,
        'titles':titles,
    }
    reset_queries()
    return render(request, 'App/tradegraphs.html', context)
    #return render(request, 'App/trade.html')

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

    """snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics("lineno")

    for stat in top_stats[:10]:
        print(stat)"""
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

def projection(g, p, context, run=True):
    import copy
    def create_graph(attribute,title,country,start):
        arr = getattr(country, attribute)[start:]
        fig = px.line(y=arr,title=title)
        fig.update_xaxes(title="Year")
        fig.update_yaxes(title=title)
        fig.add_vline(x=p.get_country().time - 18)
        fig.write_html("templates/App/graphs/"+p.name+title+".html")
    def create_single_graph(country,start, var):
        data = getattr(country, var)[start:]
        labels = [i for i in range(0,len(data))]
        return data, labels

    gtemp = g
    ptemp = p
    g = Game.objects.filter(name=g)[0]
    p = Player.objects.filter(name=p)[0]
    if True:
        new_country = copy.deepcopy(p.get_country())
        country = new_country
        #Set variables for new_country
        new_country.IncomeTax = p.IncomeTax
        new_country.CorporateTax = p.CorporateTax
        new_country.MoneyPrinting = p.MoneyPrinting
        welfare = ((p.Welfare + p.AdditionalWelfare)*new_country.money[8])/new_country.money[5]
        gov_invest = ((p.InfrastructureInvest + p.ScienceInvest)*new_country.money[8])/new_country.money[5]
        gov_goods = ((p.Education + p.Military)*new_country.money[8])/new_country.money[5]
        if welfare + gov_invest + gov_goods > 1:
            country.BondWithdrawl = (welfare + gov_invest + gov_goods - 1)*country.money[5]
            if country.BondWithdrawl > country.money[1]*0.5:
                #Country is Bankrupt if this occurs.
                country.BondWithdrawl = country.money[1]*0.5
            welfare = ((p.Welfare + p.AdditionalWelfare)*new_country.money[8])/(new_country.money[5]+new_country.BondWithdrawl)
            gov_invest = ((p.InfrastructureInvest + p.ScienceInvest)*new_country.money[8])/(new_country.money[5]+new_country.BondWithdrawl)
            gov_goods = ((p.Education + p.Military)*new_country.money[8])/(new_country.money[5]+new_country.BondWithdrawl)

        if ((p.Education + p.Military) != 0):
            new_country.EducationSpend = p.Education/(p.Education + p.Military)
            new_country.MilitarySpend = p.Military/(p.Education + p.Military)
        else:
            new_country.EducationSpend = 0

        new_country.GovGoods = gov_goods
        #country.BondWithdrawl = p.Bonds
        #country.Bonds = p.Bonds
        #country.GovWelfare = p.Welfare + p.AdditionalWelfare
        new_country.GovWelfare = welfare
        #Investment
        total_gov_money = new_country.money[5] + new_country.BondWithdrawl
        total_investor_money = new_country.money[4]*new_country.InvestmentRate

        country.GovernmentInvest = gov_invest #p.InfrastructureInvest + p.ScienceInvest
        total_money = country.money[5]*country.GovernmentInvest + total_investor_money
        new_country.InfrastructureInvest = ((total_gov_money*((p.InfrastructureInvest*new_country.money[8])/new_country.money[5]))/total_money) + ((total_investor_money*0.1)/total_money)
        new_country.ScienceInvest = ((total_gov_money*((p.ScienceInvest*new_country.money[8])/new_country.money[5]))/total_money) + ((total_investor_money*0.05)/total_money)
        #country.QuickInvestment = p.CapitalInvestment
        new_country.TheoreticalInvest = p.TheoreticalInvest
        new_country.PracticalInvest = p.PracticalInvest
        new_country.AppliedInvest = p.AppliedInvest

        new_country.run_turn(5)
        create_graph('InflationTracker','Inflation',new_country,17)
        create_graph('UnemploymentArr','Unemployment',new_country,17)
        create_graph('GoodsPerCapita','GoodsPerCapita',new_country,17)
        create_graph('GDPPerCapita','RealGDPPerCapita',new_country,17)
        create_graph('ConsumptionArr','ConsumptionPerCapita',new_country,17)
        budget_graph(new_country, 17, "templates/App/graphs/"+p.name+"budgetgraphprojections.html", True)
        inflation, labels = create_single_graph(new_country,17, 'InflationTracker')
        unemployment, labels = create_single_graph(new_country,17,'UnemploymentArr')
        GoodsPerCapita, labels = create_single_graph(new_country,17,'GoodsPerCapita')
        GDPPerCapita, labels = create_single_graph(new_country,17,'GDPPerCapita')
        Consumption, labels = create_single_graph(new_country,17,'ConsumptionArr')
    context.update({
        'unemployment_graph': unemployment,
        'inflation_graph': inflation,
        'goodspercapita_graph': GoodsPerCapita,
        'gdppercapita_graph': GDPPerCapita,
        'consumptionpercapita_graph': Consumption,
        'game':gtemp,
        'player':ptemp,
        'notifications': Notification.objects.filter(game=g)[::-1],
        'labels':labels,
        'curr_year': new_country.time - 23,
        'budget_projections': "App/graphs/"+p.name+"budgetgraphprojections.html",
        #'posts': posts
    })

    #return render(request, 'App/projection.html', context)

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

#Switches control of a hex between two players (doesn't work yet)
def switch_hex(hex_num, player_to):
    h = Hexes.objects.filter(hexNum=hex_num)[0]
    f = HexForm(request.POST, instance=h)
    if f.is_valid():
        f.save(commit=False)
        f.controller = player_to
        f.color = player_to.color