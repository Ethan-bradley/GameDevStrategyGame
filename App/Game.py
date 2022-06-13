from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes, PlayerProduct, Product, Notification
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
import math

class GameEngine():
	def __init__(self, num_players, nameListInput):
		self.nameList = nameListInput
		self.EconEngines = []
		temp = 0
		if num_players > 7:
			for i in range(0,num_players):
				self.EconEngines.append(Country())
			temp = num_players - 7
			num_players2 = 7
			for i in range(0,num_players2):
				self.EconEngines[i].run_turn(13)
		else:
			for i in range(0,num_players):
				self.EconEngines.append(Country())
				self.EconEngines[i].run_turn(13)
		self.TradeEngine = Trade(self.EconEngines,self.nameList)
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
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			#self.apply_hex_number(g, p, country)
			self.start_hex_number(g, p, country)

	def run_engine(self, g, graphs=True):
		#Resetting model variables
		all_players = Player.objects.filter(game=g)
		if graphs:
			self.set_vars(g, all_players)
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
		all_armies = Army.objects.filter(game=g)
		for a in all_armies:
			a.moved = False
		self.ArmyCombat.doCombat(g)
		#Running engine
		for e in self.EconEngines:
			e.run_turn(1)
			#e.save_GoodsPerCapita('default_graph.png')
		self.TradeEngine.trade(self.EconEngines, [[0.0 for i in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))], [[0.0 for i in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))])
		print('running engine')
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.apply_hex_number(g, p, country)
		if graphs:
			pass
			#self.create_graphs(g, all_players)
			#self.create_compare_graph(self.EconEngines, self.nameList, 17, ['GoodsPerCapita','InflationTracker','ResentmentArr','EmploymentRate','ConsumptionArr','InterestRate','GoodsBalance','ScienceArr'],'',g.name, g)
		return [self.EconEngines, self.TradeEngine]
	def run_graphs(self, g):
		all_players = Player.objects.filter(game=g)
		#self.create_graphs(g, all_players)
		self.create_compare_graph(self.EconEngines, self.nameList, 17, ['GoodsPerCapita','InflationTracker','ResentmentArr','EmploymentRate','ConsumptionArr','InterestRate','GoodsBalance','ScienceArr'],'',g.name, g)
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
		if (os.path.exists('.'+g.GoodsPerCapita.url) and g.GoodsPerCapita.name != 'default_graph.png'):
			os.remove('.'+g.GoodsPerCapita.url)
			os.remove('.'+g.Inflation.url)
			os.remove('.'+g.Resentment.url)
			os.remove('.'+g.Employment.url)
			os.remove('.'+g.Consumption.url)
			os.remove('.'+g.InterestRate.url)
			os.remove('.'+g.GoodsBalance.url)
			os.remove('.'+g.ScienceArr.url)
		a = []
		matplotlib.use('Agg')
		for j in range(0, len(attribute_list)):
			plt.clf()
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

		with open(a[7] +'.png', 'rb') as f:
			g.ScienceArr = File(f)
			g.save()
		os.remove(a[7] +'.png')

	def set_vars(self, g, all_players):
		transfer_array = [[0 for j in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))]
		military_transfer = [[0 for j in range(0,len(self.EconEngines))] for i in range(0,len(self.EconEngines))]
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			self.calculate_differences(g, p, country)
			self.get_hex_numbers(g, p, country)
			prev_revenue = country.IncomeTax*country.money[0] + country.CorporateTax*country.money[4]
			diff = country.money[5] - prev_revenue

			country.IncomeTax = p.IncomeTax
			country.CorporateTax = p.CorporateTax
			#country.GovGoods = p.Education + p.Military
			revenue = p.IncomeTax*country.money[0] + p.CorporateTax*country.money[4] + diff
			country.MoneyPrinting = p.MoneyPrinting
			#import pdb; pdb.set_trace();
			welfare = ((p.Welfare + p.AdditionalWelfare)*country.money[8])/revenue
			gov_invest = ((p.InfrastructureInvest + p.ScienceInvest)*country.money[8])/revenue
			gov_goods = ((p.Education + p.Military)*country.money[8])/revenue
			if welfare + gov_invest + gov_goods > 1:
				country.BondWithdrawl = (welfare + gov_invest + gov_goods - 1)*country.money[5]
				if country.BondWithdrawl > country.money[1]*0.5:
					#Country is Bankrupt if this occurs.
					country.BondWithdrawl = country.money[1]*0.5
				welfare = ((p.Welfare + p.AdditionalWelfare)*country.money[8])/(country.money[5]+country.BondWithdrawl)
				gov_invest = ((p.InfrastructureInvest + p.ScienceInvest)*country.money[8])/(country.money[5]+country.BondWithdrawl)
				gov_goods = ((p.Education + p.Military)*country.money[8])/(country.money[5]+country.BondWithdrawl)

			if ((p.Education + p.Military) != 0):
				country.EducationSpend = p.Education/(p.Education + p.Military)
				country.MilitarySpend = p.Military/(p.Education + p.Military)
			else:
				country.EducationSpend = 0

			country.GovGoods = gov_goods
			#country.BondWithdrawl = p.Bonds
			#country.Bonds = p.Bonds
			#country.GovWelfare = p.Welfare + p.AdditionalWelfare
			country.GovWelfare = welfare
			#Investment
			total_gov_money = revenue + country.BondWithdrawl
			total_investor_money = country.money[4]*country.InvestmentRate

			country.GovernmentInvest = gov_invest #p.InfrastructureInvest + p.ScienceInvest
			total_money = revenue*country.GovernmentInvest + total_investor_money
			country.InfrastructureInvest = ((total_gov_money*((p.InfrastructureInvest*country.money[8])/revenue))/total_money) + ((total_investor_money*0.1)/total_money)
			country.ScienceInvest = ((total_gov_money*((p.ScienceInvest*country.money[8])/revenue))/total_money) + ((total_investor_money*0.05)/total_money)
			#country.QuickInvestment = p.CapitalInvestment
			#import pdb; pdb.set_trace();
			total_money = ((total_gov_money*((p.ScienceInvest*country.money[8])/revenue))) + ((total_investor_money*0.05))
			#Money one side invests*share + money other side / total
			country.TheoreticalInvest = ((total_gov_money*p.TheoreticalInvest*((p.ScienceInvest*country.money[8])/revenue)) + ((total_investor_money*0.05*0.1)))/total_money
			country.PracticalInvest = ((total_gov_money*p.PracticalInvest*((p.ScienceInvest*country.money[8])/revenue)) + ((total_investor_money*0.05*0.3)))/total_money
			country.AppliedInvest = ((total_gov_money*p.AppliedInvest*((p.ScienceInvest*country.money[8])/revenue)) + ((total_investor_money*0.05*0.6)))/total_money

			self.TradeEngine.investment_restrictions[index] = p.investment_restriction
			#Rebellions
			if country.Resentment > 0.05:
				self.rebel(g, p, country.Resentment)
			#Tarriffs
			#import pdb; pdb.set_trace()
			#try:
			tar = Tariff.objects.filter(game=g, curr_player=p)
			if len(tar) != 0:
				tar = tar[0]
				k = IndTariff.objects.filter(controller=tar)

				count = 0
				for t in k:
					count = self.TradeEngine.CountryName.index(t.key.country.name)
					#Save data to array
					self.TarriffsArr[t.key.country.name][p.country.name].append(t.tariffAm)
					self.SanctionsArr[t.key.country.name][p.country.name].append(t.sanctionAm)
					self.ForeignAid[t.key.country.name][p.country.name].append(t.moneySend)
					self.MilitaryAid[t.key.country.name][p.country.name].append(t.militarySend)
					#save data to engines.
					self.TradeEngine.Tariffs[index][count] = t.tariffAm
					self.TradeEngine.Sanctions[index][count] = t.sanctionAm
					transfer_array[index][count] = t.moneySend
					military_transfer[index][count] = t.militarySend
					#import pdb; pdb.set_trace()
					self.TradeEngine.foreign_investment[index][count] = self.TradeEngine.foreign_investment[count][index]*t.nationalization
					count += 1
			#Append variables
			self.append_variable_list(self.var_list, self.variable_list, index, p)
			#Product subsidies/restrictions
			productP = PlayerProduct.objects.filter(game=g, curr_player=all_players[index])
			if len(productP) != 0:
				productP = productP[0]
				products = Product.objects.filter(controller=productP)
				country_index = self.nameList.index(p.country.name)
				for product in products:
					if product.name in country.HouseProducts:
						index = country.HouseProducts.index(product.name)
						self.TradeEngine.restrictions[country_index]['HouseProduction'][index] = product.exportRestriction
						country.HouseScience[index] = product.subsidy
					if product.name in country.CapitalGoods:
						index = country.CapitalGoods.index(product.name)
						self.TradeEngine.restrictions[country_index]['CapitalProduction'][index] = product.exportRestriction
						country.CapitalScience[index] = product.subsidy
					if product.name in country.RawGoods:
						index = country.RawGoods.index(product.name)
						self.TradeEngine.restrictions[country_index]['RawProduction'][index] = product.exportRestriction
						country.RawScience[index] = product.subsidy
			#except:
			#	print("Index out of range error!")

		self.TradeEngine.trade_money(self.EconEngines, transfer_array)
		self.TradeEngine.trade_military_goods(self.EconEngines, military_transfer)

	def save_variable_list(self, var_list, player_num):
		for i in var_list:
			setattr(self,i,[[0.02 for i in range(0,20)] for i in range(player_num)])
	def append_variable_list(self, var_list, variable_list, index, player):
		for i in range(0,len(var_list)):
			getattr(self,var_list[i])[index].append(getattr(player, variable_list[i]))

	def create_graphs(self, g, all_players):
		for p in all_players:
			index = self.nameList.index(p.country.name)
			country = self.get_country(index)
			if not p.robot:
				if (os.path.exists('.'+p.GoodsPerCapita.url) and p.GoodsPerCapita.name != 'default_graph.png'):
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

		#e.lastPopulation = e.Population
		for h in range(0, len(hex_list)):
			print(capital_list[h])
			if not math.isnan(int(capital_list[h])):
				hex_list[h].capital += int(capital_list[h])
			if not math.isnan(int(population_list[h])):
				hex_list[h].population += int(population_list[h])
			hex_list[h].save()
			print(hex_list[h].capital)

	def start_hex_number(self, g, p, e):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		centers = []
		for h in range(0, len(hex_list)):
			if hex_list[h].center:
				centers.append(h)
		#print(centers)
		capital_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.capital, len(hex_list))
		population_list = e.create_distribution([0 for j in range(0, len(centers))], centers, e.Population, len(hex_list))

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
	#Causes a province to rebel.
	def rebel(self, g, p, res):
		hex_list = Hexes.objects.filter(game=g, controller=p, water=False)
		if p.name != "Neutral" and (len(hex_list) > 0):
			neutral_player = Player.objects.filter(game=g,name="Neutral")[0]
			self.switch_hex(hex_list[0], neutral_player, g)
			Army.objects.create(game=g, size=hex_list[0].population*res*100,controller=neutral_player, naval=False, location=hex_list[0], name=hex_list[0].name+" Rebel Army")
			message2 = "In "+p.name+"'s territory a rebel army of size "+str(round(hex_list[0].population*res*100,0))+" rose up in "+hex_list[0].name
			turn = g.GameEngine.get_country_by_name("UK").time - 17
			Notification.objects.create(game=g, message=message2,year=turn)

	#Switches control of a hex between two players (doesn't work yet)
	def switch_hex(self, h, player_to, g):
		loser = h.controller
		#import pdb; pdb.set_trace()
		#g.GameEngine.modify_country_by_name(loser.country.name, 'Population', loser.get_country().add_population(loser.get_country().pop_matrix,-h.population*0.8))
		loser_country = loser.get_country()
		loser.get_country().add_population(loser.get_country().pop_matrix,-h.population*0.8)
		subtract = ((h.population*0.8)/loser_country.pop_matrix.sum())
		loser_country.money[0] -= loser_country.money[0]*subtract
		loser_country.money[1] -= loser_country.money[1]*subtract
		loser_country.money[2] -= loser_country.money[2]*subtract
		loser_country.money[3] -= loser_country.money[3]*subtract
		loser_country.money[4] -= loser_country.money[4]*subtract
		loser_country.money[5] -= loser_country.money[5]*subtract
		g.save()
		g.GameEngine.modify_country_by_name(loser.country.name, 'capital', loser.get_country().capital - h.capital*0.9)
		g.save()
		#loser.get_country().Population -= 
		#loser.get_country().capital -= 
		h.controller = player_to
		h.color = player_to.country.color
		#g.GameEngine.modify_country_by_name(player_to.country.name, 'Population', player_to.get_country().add_population(loser.get_country().pop_matrix, h.population*0.8))
		player_to.get_country().add_population(loser.get_country().pop_matrix, h.population*0.75)
		g.save()
		g.GameEngine.modify_country_by_name(player_to.country.name, 'capital', player_to.get_country().capital + h.capital*0.8)
		#player_to.get_country().Population += h.population*0.75
		#player_to.get_country().capital += h.capital*0.75
		g.save()

		h.save()
		player_to.save()
		loser.save()
