from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes, PlayerProduct, Product, Notification, Building
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, ResetTurn
from django.core.files import File
from .HexList import HexList
from .ArmyCombat import ArmyCombat
from django.db.models.fields import *
import os
import math

class GameEngine():
	def __init__(self, num_players, nameListInput):
		self.nameList = nameListInput
		self.EconEngines = []
		temp = 0
		if num_players > 7:
			temp = num_players - 7
			num_players2 = 7
		self.ArmyCombat = ArmyCombat()
		self.var_list = ['Welfare','Education','Military','Infrastructure','Science']
		self.variable_list = ['Welfare','Education','Military','InfrastructureInvest','ScienceInvest']
		self.save_variable_list(self.var_list, num_players)
		countries = self.nameList
		self.TarriffsArr = {i:{k:[0 for i in range(0,20)] for k in countries} for i in countries}
		#import pdb; pdb.set_trace()
		self.SanctionsArr = {i:{k:[0 for i in range(0,20)] for k in countries} for i in countries}
		self.ForeignAid = {i:{k:[0 for i in range(0,20)] for k in countries} for i in countries}
		self.MilitaryAid = {i:{k:[0 for i in range(0,20)] for k in countries} for i in countries}
		self.endGame = False
		self.conquerer_win = 7
		self.gold_win = 20
		self.dom_win = 5
	def run_more_countries(self, num_players):
		if num_players > 5:
			for i in range(7,num_players):
				self.EconEngines[i].run_turn(13)
	def run_start_trade(self, g, turn_num=7):
		self.run_engine(g)
		for i in range(0,turn_num-2):
			self.run_engine(g, False)
		self.run_engine(g)
	def start_capital(self, g):
		all_players = Player.objects.filter(game=g)
		for p in all_players:
			self.start_hex_number(g, p)

	def run_engine(self, g, graphs=True):
		#Resetting model variables
		if self.endGame:
			return
		all_players = Player.objects.filter(game=g)
		if g.num_players > 1:
			for p in all_players:
				f = ResetTurn(instance=p)
				pla = f.save(commit=False)
				pla.ready = False
				pla.projection_unloaded = True
				pla.save()
				
			neutral_player2 = Player.objects.filter(name="Neutral")[0]
			neutral_player2.ready = True
			neutral_player2.save()
		else:
			p = Player.objects.filter(user=g.host)[0]
			print(p.name)
			f = ResetTurn(instance=p)
			pla = f.save(commit=False)
			pla.ready = False
			pla.save()
		all_buildings = Building.objects.filter(game=g)
		for building in all_buildings:
			building.addResources()
		self.ArmyCombat.doCombat(g)
		all_armies = Army.objects.filter(game=g)
		for army in all_armies:
			army.moved = False
			army.save()
		g.year += 1
		g.save()
		print('running engine')
		for player in all_players:
			self.add_resources(player)
			self.check_win(player, g)
		return
	
	def check_win(self, player, g):
		hexlist = Hexes.objects.filter(controller=player, water=False)
		if len(hexlist) >= self.conquerer_win or player.gold >= self.gold_win or player.NationsDefeated >= self.dom_win:
			g.gameEnd = True
			g.winner = player.name
			g.save()

	def add_resources(self, p):
		hexlist = Hexes.objects.filter(controller=p)
		for hex2 in hexlist:
			p.money += hex2.capital
			p.coal += hex2.coal
			p.iron += hex2.iron
			p.wheat += hex2.wheat
			p.oil += hex2.oil
		p.save()

	def game_combat(self, g):
		self.ArmyCombat.doCombat(g)

	def get_country(self, index):
		return self.EconEngines[index]

	def get_country_by_name(self, name):
		index = self.nameList.index(name)
		country = self.get_country(index)
		return country

	def get_country_index(self, name):
		index = self.nameList.index(name)
		return index

	def modify_country_by_name(self, name, attr, set_am):
		index = self.nameList.index(name)
		country = self.get_country(index)
		setattr(country, attr, set_am)
		if getattr(country, attr) < 1:
			setattr(country, attr, set_am)

	def get_trade(self, index, var):
		if var == 0:
			return self.TradeEngine
		elif var == 1:
			return self.TradeEngine.currencyReserves[index]
		elif var == 2:
			return self.TradeEngine.exchangeRates[index]
		elif var == 3:
			return self.TradeEngine.Tariffs[index]
			#except:
			#	print("Index out of range error!")

		self.TradeEngine.trade_money(self.EconEngines, transfer_array)
		self.TradeEngine.trade_military_goods(self.EconEngines, military_transfer)

	def save_variable_list(self, var_list, player_num):
		for i in var_list:
			#change to 17
			setattr(self,i,[[0.02 for i in range(0,20)] for i in range(player_num)])
	def append_variable_list(self, var_list, variable_list, index, player):
		for i in range(0,len(var_list)):
			getattr(self,var_list[i])[index].append(getattr(player, variable_list[i]))
		
			
	def calculate_differences(self, g, p, e):
	    #g = Game.objects.filter(name=g)[0]
	    #p = Player.objects.filter(name=p)[0]
		policy_list = PolicyGroup.objects.filter(game=g, player=p)
		BalanceList = [0.0 for i in range(11)]
		for pg in policy_list:
			p2 = Policy.objects.filter(policy_group=pg, applied=True)
			if len(p2) <= 0:
				continue
			p2 = p2[0]
			all_fields = p2._meta.get_fields() #_meta.fields
			count = 0
			for a in all_fields:
				if isinstance(a, FloatField):
					n = a.name
					BalanceList[count] += getattr(p2, n)
					count += 1
		#print(BalanceList[0])
		e.SavingsRate = 0.3 + BalanceList[0]
		#print(BalanceList[1])
		e.ConsumptionRate = 0.5 + BalanceList[1]
		#print(BalanceList[2])
		#p.Welfare = BalanceList[2]
		e.Wages = 0.4 + BalanceList[9]
		e.population_growth = 0.02 + BalanceList[10]
		p.save()

	def get_hex_numbers(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		total_population = 0
		total_capital = 0
		total_iron = 0.01
		total_wheat = 0.01
		total_coal = 0.01
		total_oil = 0.01
		for h in hex_list:
			total_population += h.population
			total_capital += h.capital
			total_iron += h.iron
			total_wheat += h.wheat
			total_coal += h.coal
			total_oil += h.oil
		#e.Population = total_population
		#e.capital = total_capital
		e.RawResources[0] = total_iron
		e.RawResources[1] = total_wheat
		e.RawResources[2] = total_coal
		e.RawResources[3] = total_oil
		p.save()


	def apply_hex_number(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		centers = []
		for h in range(0, len(hex_list)):
			if hex_list[h].center:
				centers.append(h)
		#print(centers)
		capital_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.capital - e.lastcapital, len(hex_list))
		population_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.Population - e.lastPopulation, len(hex_list))

		for h in range(0, len(hex_list)):
			print(capital_list[h])
			if not math.isnan(capital_list[h]):
				hex_list[h].capital += int(capital_list[h])
			if not math.isnan(population_list[h]):
				hex_list[h].population += int(population_list[h])
			hex_list[h].save()
			print(hex_list[h].capital)

	def start_hex_number(self, g, p):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		centers = []
		for h in range(0, len(hex_list)):
			if hex_list[h].center:
				centers.append(h)
		capital_list = [0 for j in range(0, len(hex_list))]
		population_list = [0 for j in range(0, len(hex_list))]

		for h in range(0, len(hex_list)):
			hex_list[h].capital += int(capital_list[h])
			hex_list[h].population += int(population_list[h])
			hex_list[h].save()

	#Switches control of a hex between two players (doesn't work yet)
	def switch_hex(self, h, player_to, g):
		loser = h.controller
		h.controller = player_to
		h.color = player_to.country.color
		h.save()
		for building in buildings:
			building.controller = player_to
			building.save()
		player_to.save()
		loser.save()
