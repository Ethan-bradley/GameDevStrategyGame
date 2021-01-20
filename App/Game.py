from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, ResetTurn
from .GameEconModel import Country
from .TradeModel import Trade
from django.core.files import File
from .HexList import HexList
from django.db.models.fields import *


class GameEngine():
	def __init__(self, num_players, nameListInput):
		self.nameList = nameListInput
		self.EconEngines = []
		for i in range(0,num_players):
			self.EconEngines.append(Country())
			self.EconEngines[i].run_turn(20)
		self.TradeEngine = Trade(self.EconEngines,self.nameList)

	def start_capital(self, g):
		all_players = Player.objects.filter(game=g)
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.apply_hex_number(g, p, country)

	def run_engine(self, g):
		#Resetting model variables
		all_players = Player.objects.filter(game=g)
		self.set_vars(g, all_players)
		for p in all_players:
			f = ResetTurn(instance=p)
			pla = f.save(commit=False)
			pla.ready = False
			pla.save()
		all_armies = Army.objects.filter(game=g)
		for a in all_armies:
			a.moved = False
		#Running engine
		for e in self.EconEngines:
			e.run_turn(1)
			e.save_GoodsPerCapita('default_graph.png')
		self.TradeEngine.conductTrade()
		print('running engine')
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.apply_hex_number(g, p, country)
		return [self.EconEngines, self.TradeEngine]

	def get_country(self, index):
		return self.EconEngines[index]

	def get_country_by_name(self, name):
		index = self.nameList.index(name)
		country = self.get_country(index)
		return country

	def get_country_index(self, name):
		index = self.nameList.index(name)
		return index

	def get_trade(self, index, var):
		if var == 0:
			return self.TradeEngine
		elif var == 1:
			return self.TradeEngine.currencyReserves[index]
		elif var == 2:
			return self.TradeEngine.exchangeRates[index]
		elif var == 3:
			return self.TradeEngine.Tariffs[index]

	def set_vars(self, g, all_players):
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.calculate_differences(g, p, country)
			self.get_hex_numbers(g, p, country)
			country.IncomeTax = p.IncomeTax
			country.CorporateTax = p.CorporateTax
			country.GovGoods = p.Education + p.Military
			country.EducationSpend = p.Education/(p.Education + p.Military)
			country.MoneyPrinting = p.MoneyPrinting
			#country.Bonds = p.Bonds
			country.GovWelfare = p.Welfare
			#Tarriffs
			tar = Tariff.objects.filter(game=g, curr_player=p)[0]
			k = IndTariff.objects.filter(controller=tar)
			count = 0
			for t in k:
				self.TradeEngine.Tariffs[index][count] = t.tariffAm
				count += 1

			#Graphs:
			country.save_GoodsPerCapita('.'+p.GoodsPerCapita.url)
			a = country.save_graphs('./media/graphs',p.name)
			print(a[1])
			with open('.'+p.GoodsPerCapita.url, 'rb') as f:
				p.GoodsPerCapita = File(f)
				p.save()

			with open(a[1]+'.png', 'rb') as f:
				p.Inflation = File(f)
				p.save()

			with open(a[2]+'.png', 'rb') as f:
				p.RealGDP = File(f)
				p.save()

			with open(a[3]+'.png', 'rb') as f:
				p.Employment = File(f)
				p.save()
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
		p.Welfare = 0.7 + BalanceList[2]
		e.Wages = 0.4 + BalanceList[9]
		e.population_growth = 0.02 + BalanceList[10]
		p.save()

	def get_hex_numbers(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		total_population = 0
		total_capital = 0
		for h in hex_list:
			total_population += h.population
			total_capital += h.capital
		e.Population = total_population
		e.capital = total_capital

	def apply_hex_number(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		centers = []
		for h in range(0, len(hex_list)):
			if hex_list[h].center:
				centers.append(h)
		#print(centers)
		capital_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.capital, len(hex_list))
		population_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.Population, len(hex_list))
		for h in range(0, len(hex_list)):
			print(capital_list[h])
			hex_list[h].capital = int(capital_list[h])
			hex_list[h].population = int(population_list[h])
			hex_list[h].save()
			print(hex_list[h].capital)

	def printTradeAms(self):
		countryNames = self.nameList
		currencyChangeReserves = self.TradeEngine.currencyChangeReserves 
		string = ""
		for i in range(0,len(currencyChangeReserves)):
			string += "Trade Portfolio of "+countryNames[i]+"\n"
		for j in range(0,len(currencyChangeReserves[0])):
			if i == j:
				continue
		string += "Exports to "+countryNames[j]+": "+str(currencyChangeReserves[i][j])+"\n"
		return string

	def printCurrencyReserves(self):
		countryNames = self.nameList
		currencyReserves = self.TradeEngine.currencyReserves 
		string = ""
		for i in range(0,len(currencyReserves)):
			string += "Trade Portfolio of "+countryNames[i]+"\n"
		for j in range(0,len(currencyReserves[0])):
			if i == j:
				continue
		string += "Exports to "+countryNames[j]+": "+str(currencyReserves[i][j])+"\n"
		return string

	def printCurrencyExchange(self):
		countryNames = self.nameList
		currencyRates = self.TradeEngine.currencyRates 
		string = ""
		for i in range(0,len(currencyRates)):
			string += "Currency Exchange of "+countryNames[i]+"\n"
		for j in range(0,len(currencyRates[0])):
			if i == j:
				continue
			string += "Your dollar can buy "+str(currencyRates[i][j])+" of "+countryNames[j]+"\n"
		return string