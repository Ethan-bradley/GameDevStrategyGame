from .Game import GameEngine
from .models import Post
from .models import Game, Player, IndTariff, Tariff, Hexes, Army, Policy, PolicyGroup, Country, PlayerProduct, Product, MapInterface, Notification, GraphInterface, Army
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, HexForm, ArmyForm, GovernmentSpendingForm, PolicyForm, PolicyFormSet, AddProductForm, AddPlayerProductForm, MapInterfaceForm, GraphInterfaceForm
from .PolicyList import PolicyList

def add_players(temp, type):
	if type:
		all_countries = Country.objects.filter(large=False)
	else:
		all_countries = Country.objects.all()
	for country in all_countries:
	    all_players = Player.objects.filter(game=temp)
	    countryList = []
	    form = JoinGameForm()
	    for player in all_players:
	        countryList.append(player.country)
	    #Creates player object associated with this user and game.
	    if country in countryList:
	    	continue
	    f = form.save(commit=False)
	    countryList2 = ''
	    f.country = country
	    f.host = False
	    f.name = country.name
	    f.user = temp.host
	    f.game = temp
	    f.color = f.country.color
	    f.robot = True
	    f.save()
	    curr_player = Player.objects.filter(name=f.name, game=temp)[0]
	    #Creates Map Interface
	    MapInterface.objects.create(game=temp,controller=curr_player)
	    GraphInterface.objects.create(game=temp,controller=curr_player)
	    #Creates Policies
	    p2 = PolicyList()
	    p2.add_policies(curr_player, temp)
	    #Adds control to related hexes
	    hex_list = Hexes.objects.filter(game=temp, start_country=curr_player.country)
	    for i in hex_list:
	        i.controller = curr_player
	        i.save()
	    #Creates Tariff object associated with player and game.
	    formt = AddTariffForm()
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
	    formt = AddPlayerProductForm()
	    formt = formt.save(commit=False)
	    formt.curr_player = curr_player
	    formt.game = temp
	    formt.name = curr_player.name
	    formt.save()
	    #Adds an IndTariff object to each player's tariff object.
	    productList = ['Food','Consumer Goods','Steel','Machinery','Iron','Wheat','Coal','Oil']
	    for product in productList:
	        iForm = AddProductForm()
	        itf = iForm.save(commit=False)
	        itf.controller = PlayerProduct.objects.filter(game=temp, curr_player=curr_player.id)[0]
	        itf.key = curr_player
	        itf.name = product
	        itf.save()
	    temp.save()
	    #Remove this if game isn't 2 player
	    #temp.GameEngine.start_capital(temp)
	#if type:
	#temp.GameEngine.start_capital(temp)
	#temp.save()
def add_neutral(temp):
    form = JoinGameForm()
    f = form.save(commit=False)
    countryList2 = ''
    f.country = Country.objects.filter(name="Neutral")[0]
    f.host = False
    f.name = "Neutral"
    f.user = temp.host
    f.game = temp
    f.color = f.country.color
    f.robot = True
    f.save()
    curr_player = Player.objects.filter(name=f.name, game=temp)[0]
    #Creates Map Interface
    MapInterface.objects.create(game=temp,controller=curr_player)
    GraphInterface.objects.create(game=temp,controller=curr_player)
    #Creates Policies
    p2 = PolicyList()
    p2.add_policies(curr_player, temp)
    #Adds control to related hexes
    hex_list = Hexes.objects.filter(game=temp, start_country=curr_player.country)
    for i in hex_list:
    	if i.water == False:
	        i.controller = curr_player
	        Army.objects.create(game=temp, size=1000, controller=curr_player, naval=False, location=i, name=i.name+" Army", moved=False, max_movement=2)
	        i.save()
    #Creates Tariff object associated with player and game.
    formt = AddTariffForm()
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
    formt = AddPlayerProductForm()
    formt = formt.save(commit=False)
    formt.curr_player = curr_player
    formt.game = temp
    formt.name = curr_player.name
    formt.save()
    #Adds an IndTariff object to each player's tariff object.
    productList = ['Food','Consumer Goods','Steel','Machinery','Iron','Wheat','Coal','Oil']
    for product in productList:
        iForm = AddProductForm()
        itf = iForm.save(commit=False)
        itf.controller = PlayerProduct.objects.filter(game=temp, curr_player=curr_player.id)[0]
        itf.key = curr_player
        itf.name = product
        itf.save()
    temp.save()
    #Remove this if game isn't 2 player
    #temp.GameEngine.start_capital(temp)