from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes
from .forms import NewGameForm, IndTariffForm, JoinGameForm, AddIndTariffForm, AddTariffForm, NextTurn, ResetTurn
from .GameEconModel import Country
from .TradeModel import Trade
from django.core.files import File
from .HexList import HexList
from .ArmyCombat import ArmyCombat
from django.db.models.fields import *
import os
import matplotlib.pyplot as plt
import matplotlib


class GameEngine():
	def __init__(self, num_players, nameListInput):
		self.nameList = nameListInput
		self.EconEngines = []
		for i in range(0,num_players):
			self.EconEngines.append(Country())
			self.EconEngines[i].run_turn(20)
		self.TradeEngine = Trade(self.EconEngines,self.nameList)
		self.ArmyCombat = ArmyCombat()

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
		self.ArmyCombat.doCombat(g)
		#Running engine
		for e in self.EconEngines:
			e.run_turn(1)
			e.save_GoodsPerCapita('default_graph.png')
		self.TradeEngine.trade(self.EconEngines, [[0.0 for i in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))], [[0.0 for i in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))])
		print('running engine')
		self.create_compare_graph(self.EconEngines, self.nameList, 20, ['GoodsPerCapita','InflationTracker','ResentmentArr','EmploymentRate','ConsumptionArr','InterestRate','GoodsBalance'],'',g.name, g)
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

	def create_compare_graph(self, CountryList, CountryName, start, attribute_list, file_path, game_name, g):
		if (g.GoodsPerCapita.name != 'default_graph.png'):
			os.remove('.'+g.GoodsPerCapita.url)
			os.remove('.'+g.Inflation.url)
			os.remove('.'+g.Resentment.url)
			os.remove('.'+g.Employment.url)
			os.remove('.'+g.Consumption.url)
			os.remove('.'+g.InterestRate.url)
			os.remove('.'+g.GoodsBalance.url)
		a = []
		for j in range(0, len(attribute_list)):
			plt.title(attribute_list[j])
			for i in range(0,len(CountryList)):
				plt.plot(getattr(CountryList[i],attribute_list[j])[start:],label=CountryName[i])
				plt.ylabel(attribute_list[j])
				plt.xlabel('Years')
				plt.legend()
			plt.savefig(file_path+game_name+attribute_list[j])
			a.append(file_path+game_name+attribute_list[j])
			plt.clf()
		plt.close()

		with open(a[0] +'.png', 'rb') as f:
			g.GoodsPerCapita = File(f)
			g.save()
		os.remove(a[0] +'.png')

		with open(a[1] +'.png', 'rb') as f:
			g.Inflation = File(f)
			g.save()
		os.remove(a[1] +'.png')
		
		with open(a[2] +'.png', 'rb') as f:
			g.Resentment = File(f)
			g.save()
		os.remove(a[2] +'.png')

		with open(a[3] +'.png', 'rb') as f:
			g.Employment = File(f)
			g.save()
		os.remove(a[3] +'.png')

		with open(a[4] +'.png', 'rb') as f:
			g.Consumption = File(f)
			g.save()
		os.remove(a[4] +'.png')

		with open(a[5] +'.png', 'rb') as f:
			g.InterestRate = File(f)
			g.save()
		os.remove(a[5] +'.png')

		with open(a[6] +'.png', 'rb') as f:
			g.GoodsBalance = File(f)
			g.save()
		os.remove(a[6] +'.png')

	def set_vars(self, g, all_players):
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.calculate_differences(g, p, country)
			#self.get_hex_numbers(g, p, country)
			country.IncomeTax = p.IncomeTax
			country.CorporateTax = p.CorporateTax
			country.GovGoods = p.Education + p.Military
			if ((p.Education + p.Military) != 0):
				country.EducationSpend = p.Education/(p.Education + p.Military)
				country.MilitarySpend = p.Military/(p.Education + p.Military)
			else:
				country.EducationSpend = 0
			country.MoneyPrinting = p.MoneyPrinting
			country.BondWithdrawl = p.Bonds
			#country.Bonds = p.Bonds
			country.GovWelfare = p.Welfare + p.AdditionalWelfare
			#Investment
			total_gov_money = country.money[5]
			total_investor_money = country.money[4]*country.InvestmentRate

			country.GovernmentInvest = p.InfrastructureInvest + p.ScienceInvest
			total_money = country.money[5]*country.GovernmentInvest + total_investor_money
			country.InfrastructureInvest = ((total_gov_money*p.InfrastructureInvest)/total_money) + ((total_investor_money*0.1)/total_money)
			country.ScienceInvest = ((total_gov_money*p.ScienceInvest)/total_money) + ((total_investor_money*0.2)/total_money)
			#country.QuickInvestment = p.CapitalInvestment
			country.TheoreticalInvest = p.TheoreticalInvest
			country.PracticalInvest = p.PracticalInvest
			country.AppliedInvest = p.AppliedInvest

			#Tarriffs
			tar = Tariff.objects.filter(game=g, curr_player=p)[0]
			k = IndTariff.objects.filter(controller=tar)
			count = 0
			for t in k:
				self.TradeEngine.Tariffs[index][count] = t.tariffAm
				self.TradeEngine.Sanctions[index][count] = t.sanctionAm
				count += 1
			if (p.GoodsPerCapita.name != 'default_graph.png'):
				os.remove('.'+p.GoodsPerCapita.url)
				os.remove('.'+p.Inflation.url)
				os.remove('.'+p.RealGDP.url)
				os.remove('.'+p.Employment.url)
				os.remove('.'+p.GovBudget.url)
				os.remove('.'+p.tradeBalance.url)
				os.remove('.'+p.GDPPerCapita.url)
				os.remove('.'+p.InterestRate.url)
				os.remove('.'+p.Capital.url)
				os.remove('.'+p.GoodsProduction.url)
				os.remove('.'+p.GDP.url)
				os.remove('.'+p.GDPGrowth.url)
			#Graphs:
			#country.save_GoodsPerCapita('.'+p.GoodsPerCapita.url)
			a = country.save_graphs('',p.name)
			#print(a[1])
			
			with open(a[0]+'.png', 'rb') as f:
				p.GoodsPerCapita = File(f)
				p.save()
			os.remove(a[0]+'.png')

			
			with open(a[1]+'.png', 'rb') as f:
				p.Inflation = File(f)
				p.save()
			os.remove(a[1]+'.png')
			
			with open(a[2]+'.png', 'rb') as f:
				p.RealGDP = File(f)
				p.save()
			os.remove(a[2]+'.png')
			
			with open(a[3]+'.png', 'rb') as f:
				p.Employment = File(f)
				p.save()
			os.remove(a[3]+'.png')

			with open(a[4]+'.png', 'rb') as f:
				p.GovBudget = File(f)
				p.save()
			os.remove(a[4]+'.png')

			with open(a[5]+'.png', 'rb') as f:
				p.tradeBalance = File(f)
				p.save()
			os.remove(a[5]+'.png')

			with open(a[6]+'.png', 'rb') as f:
				p.GDPPerCapita = File(f)
				p.save()
			os.remove(a[6]+'.png')

			with open(a[7]+'.png', 'rb') as f:
				p.InterestRate = File(f)
				p.save()
			os.remove(a[7]+'.png')

			with open(a[8]+'.png', 'rb') as f:
				p.Capital = File(f)
				p.save()
			os.remove(a[8]+'.png')

			with open(a[9]+'.png', 'rb') as f:
				p.GoodsProduction = File(f)
				p.save()
			os.remove(a[9]+'.png')

			with open(a[10]+'.png', 'rb') as f:
				p.GDP = File(f)
				p.save()
			os.remove(a[10]+'.png')

			with open(a[11]+'.png', 'rb') as f:
				p.GDPGrowth = File(f)
				p.save()
			os.remove(a[11]+'.png')
			
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
		p.Welfare = BalanceList[2]
		e.Wages = 0.4 + BalanceList[9]
		e.population_growth = 0.02 + BalanceList[10]
		p.save()

	def get_hex_numbers(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		total_population = 0
		total_capital = 0
		total_iron = 0.5
		total_wheat = 0.5
		total_coal = 0.5
		total_oil = 0.5
		for h in hex_list:
			total_population += h.population
			total_capital += h.capital
			total_iron += h.iron
			total_wheat += h.wheat
			total_coal += h.coal
			total_oil += h.oil
		e.Population = total_population
		e.capital = total_capital
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

		#e.lastPopulation = e.Population
		for h in range(0, len(hex_list)):
			print(capital_list[h])
			hex_list[h].capital += int(capital_list[h])
			hex_list[h].population += int(population_list[h])
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
			string += "Currency Reserves of "+countryNames[i]+"\n"
		for j in range(0,len(currencyReserves[0])):
			if i == j:
				continue
		string += "Exports to "+countryNames[j]+": "+str(currencyReserves[i][j])+"\n"
		return string

	def printCurrencyExchange(self):
		countryNames = self.nameList
		currencyRates = self.TradeEngine.exchangeRates 
		string = ""
		for i in range(0,len(currencyRates)):
			string += " "+countryNames[i]
			string += ": "+str(currencyRates[i])+"\n"
		return string