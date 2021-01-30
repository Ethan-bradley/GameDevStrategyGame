class Trade():
	def __init__(self, CountryListInput, CountryNameInput):
		self.CountryList = CountryListInput
		self.CountryName = CountryListInput
		self.Tariffs = []
		self.currencyReserves = []
		self.exchangeRates = []
		self.currencyChangeReserves = []
		for i in self.CountryList:
			self.Tariffs.append([0 for j in self.CountryList])
			self.currencyReserves.append([0 for j in self.CountryList])
			self.exchangeRates.append([1 for j in self.CountryList])
			self.currencyChangeReserves = [[1 for j in self.CountryList] for i in self.CountryList]

	def conductTrade(self, CountryList2):
		self.currencyChangeReserves = [[1 for j in self.CountryList] for i in self.CountryList]
		self.trade(CountryList2, self.Tariffs, self.currencyReserves, self.currencyChangeReserves, self.exchangeRates)
		#printTradeAms(self.CountryName,currencyChangeReserves)
		#printCurrencyExchange(self.CountryName,exchangeRates)

	def trade(self, Country, Tariffs, CurrencyReserves, currencyChangeReserves, exchangeRates):
		prev = []
		for i in range(0,len(Country)):
			prev.append(Country[i].goods[0]+Country[i].goods[1]+Country[i].goods[2])
		for i in range(0,len(Country)):
			HouseDifferenceArray = []
			CapitalDifferenceArray = []
			RawDifferenceArray = []
		for j in range(0, len(Country)):
		  if (i == j):
		    HouseDifferenceArray.append(0)
		    CapitalDifferenceArray.append(0)
		    RawDifferenceArray.append(0)
		    continue
		  for k in range(0, len(Country[i].HousePrices)):
		    #print(Country[j].HousePrices[k]*exchangeRates[i][j]*(1 + Tariffs[j][i]))
		    if (Country[i].HousePrices[k] > Country[j].HousePrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j])):
		      print('trading Houses')
		      HouseDifferenceArray.append(((Country[j].HousePrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j]))/Country[i].HousePrices[k])*0.5)
		    else:
		      HouseDifferenceArray.append(0)
		    if (Country[i].CapitalPrices[k] > Country[j].CapitalPrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j])):
		      print('trading Capital')
		      CapitalDifferenceArray.append(((Country[j].CapitalPrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j]))/Country[i].CapitalPrices[k])*0.5)
		    else:
		      CapitalDifferenceArray.append(0)
		    if (Country[i].RawPrices[k] > Country[j].RawPrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j])):
		      RawDifferenceArray.append(((Country[j].RawPrices[k]*exchangeRates[j][i]*(1 + Tariffs[i][j]))/Country[i].RawPrices[k])*0.5)
		    else:
		      RawDifferenceArray.append(0)
		for v in range(0,2):
		  self.tradeSum(Country, HouseDifferenceArray[v::2],i, 0, v, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves)
		  self.tradeSum(Country, CapitalDifferenceArray[v::2],i, 1, v, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves)
		  self.tradeSum(Country, RawDifferenceArray[v::2],i, 1, v, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves)
		for i in range(0,len(Country)):
		  Country[i].tradeBalance = prev[i] - (Country[i].goods[0]+Country[i].goods[1]+Country[i].goods[2])

	def tradeSum(self, Country, DifferenceArray, to, goodIndex, k, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves):
		total = sum(DifferenceArray)
		if total == 0:
			return
		#print("Difference Array len: "+str(len(DifferenceArray)))
		#print(DifferenceArray)
		for i in range(0, len(DifferenceArray)):
			if i == to:
			  continue
			am = (DifferenceArray[i]/total)*DifferenceArray[i]
			self.dotrade(am, Country, to, i, goodIndex, k, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves)

	def dotrade(self, difference, Country, to, fro, goodIndex, k, Tariffs, exchangeRates, currencyChangeReserves, CurrencyReserves):
		goodAm = Country[fro].goods[goodIndex]*difference*Country[fro].HouseProduction[k]
		Country[to].goods[goodIndex] += goodAm
		#Country[to].tradeBalance -= goodAm
		Country[fro].goods[goodIndex] -= goodAm
		#Country[fro].tradeBalance += goodAm
		Country[to].money[goodIndex] -= Country[to].HousePrices[k]*(1-Tariffs[to][fro])
		CurrencyReserves[fro][to] += Country[to].HousePrices[k]*(1-Tariffs[to][fro])
		currencyChangeReserves[fro][to] += Country[to].HousePrices[k]*(1-Tariffs[to][fro])
		Country[to].money[5] += Country[to].HousePrices[k]*Tariffs[to][fro]
		self.calculateExchangeRates(exchangeRates, currencyChangeReserves)

	def calculateExchangeRates(self, exchangeRates, currencyChangeReserves):
		for i in range(0,len(currencyChangeReserves)):
			for j in range(0,len(currencyChangeReserves[i])):
				if currencyChangeReserves[j] != 0:
					exchangeRates[i][j] = currencyChangeReserves[i][j]/currencyChangeReserves[j][i]
