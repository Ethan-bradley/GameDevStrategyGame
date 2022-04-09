import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from scipy.stats import norm
import statistics as stat
import math
import warnings

#RUN THIS CELL to start

#RUN THIS CELL to start

#RUN THIS CELL to start

class Country():

  def __init__(self):
    #Stats Tracking Variables
    self.GDP = [];
    self.Savings = [];
    self.InflationTracker = [];
    self.Investment = [];
    self.GDPGrowth = [];
    self.RealGDPGrowth = [];
    self.GoodsTotal = [];
    self.GDPPerCapita = [];
    self.GoodsPerCapita = [];
    self.EmploymentRate = [];
    self.AppliedArr = [];
    self.CapitalArr = []
    self.ScienceArr = []
    self.InterestRate = []
    self.PopulationArr = []
    self.Household_SavingsArr = []
    self.Corporate_SavingsArr = []
    self.PercentNPL = []
    self.GoodsBalance = []
    self.InfrastructureArray = []
    self.ConsumptionArr = []
    self.PhillipsArr = [0,0,0,0,0];
    self.capitalChange2 = 2
    self.ResentmentArr = []
    self.UnemploymentArr = []
    self.CorporateTaxArr = []
    self.IncomeTaxArr = []
    self.InfrastructureArr = []
    self.WelfareArr = []
    self.EducationArr = []
    self.MilitaryArr = []
    self.ScienceBudgetArr = []
    self.pos_interest_payments = []
    self.neg_interest_payments = []
    #Tracking Variables
    self.Unemployment = 0
    self.Bonds = 0
    self.TariffRevenue = 0
    self.TransportRevenue = 0
    self.BondWithdrawl = 0
    self.MoneyPrinting = 200
    self.money = np.array([10,10,10,15,10,10,0,0,10,self.MoneyPrinting])
    self.names = ['Households','Savings','Consumption','Investment','Corporations','Government','Imports','Exports','GDP','CentralBank']
    self.goods = np.array([10,10,10,10,10])
    self.namesGoods = ['Households','Corporations','Governments','Raw','Exports']
    self.last_capital2 = 18
    #Different Products, Capital Demand + Raw Demand must add up to 1.
    self.HouseProducts = ['Food','Consumer Goods']
    self.HouseDemand = [0.1,0.9]
    self.HouseProduction = [0.1,0.9]
    self.HouseLabor = [0.1,0.9]
    self.HousePrices = [0,0]
    self.HouseCapital = [10,10]
    self.HouseEducation = [0.5,1]
    self.CapitalGoods = ['Steel','Machinery']
    self.CapitalEducation = [2,3]
    self.CapitalDemand = [0.2,0.4]
    self.CapitalProduction = [0.2,0.4]
    self.CapitalLabor = [0.3,0.7]
    self.CapitalPrices = [0,0]
    self.CapitalCapital = [10,10]
    self.RawGoods = ['Iron','Wheat','Coal','Oil']
    self.RawEducation = [1,0.5,1,3]
    self.RawDemand = [0.15, 0.05, 0.15, 0.05]
    self.RawProduction = [0.375,0.125,0.375,0.125]
    self.RawLabor = [0.3,0.2,0.3,0.2]
    self.RawPrices = [0,0,0,0]
    self.RawCapital = [10,10,10,10]
    self.RawResources = [0.01,0.01,0.01,0.01]
    self.GovCapital = [10,10]
    self.GovernmentGoods = [1,1]

    self.Jobs = [0.1,0.1,0.1,0.1,0.1,0.1]
    self.goodsInd = [2,2,2,2,2,2]
    #Capital in each Hex
    self.HexCapital = [0 for i in range(0,100)]
    self.Raw = 20
    self.capital_destruction = 0.95

    #Initialization variables (Allowed to change).
    #Economic variables
    self.ConsumptionRate = 0.5
    self.SavingsRate = 0.3
    self.InvestmentRate = 0.5
    self.Wages = 0.4
    self.CorporateDebtRate = 0.9
    self.PersonalDebtRate = 1 - self.CorporateDebtRate
    self.RawInvestment = 0.2
    
    #Resentment
    self.Resentment = 0
    #Other
    self.tradeBalance = 0

    #Government taxes and spending.
    self.IncomeTax = 0.2
    self.CorporateTax = 0.1
    self.GovGoods = 0.3
    self.GovWelfare = 0.7
    self.GovernmentInvest = 0
    self.PersonalWithdrawls = 0
    self.CorporateInterest = 0
    self.CorporateWithdrawls = 0
    self.Bonds = 0
    self.Government_Savings = 0
    self.Education_Divisor = 1600
    self.MilitarySpend = 0.01
    
    #Money Printing
    self.MoneyPrinting = 100

    #Population Related vars
    self.Population = 25474
    self.Population_growth = 1.02
    self.Population_death = 1.02
    self.Population_birth = 1.04
    self.Geniuses = 5

    self.InvestmentCorps = 10
    self.ConsumptionCorps = 5
    self.RawCorps = 5
    self.ScienceRate = 10
    self.Invest_Left = self.ScienceRate*self.Population
    self.TotalInvest = 0

    self.Corporate_Cummalative_Loans = 0.0
    self.ConsumerPrice = 1

    #InterestRate vars
    self.interest_rate = 0

    #Employment
    self.employment = 0
    self.retirement_age = 70

    self.capital = 10
    self.employment_per_capital = 0.2
    self.last_capital = 9

    self.lastcapital = 0
    self.lastPopulation = 0

    self.Phillips = 0

    #Education
    self.Education = 9
    self.EducationSpend = 0.99
    self.run_first()

    #Centers and hexes
    self.centers = [10,20,40]
    self.hexNum = 50

    #Savings
    self.Corporate_Savings = 0
    self.Household_Savings = 0

    #Researcher numbers
    self.Researcher_Percentage = 0.01
    self.Innovators_Percentage = 0.01

    self.Military = 0
    self.Infrastructure = 0
    self.Infrastructure_Real = 0

    #Science related
    self.scienceDivisor = 100
    self.ScienceEff = 0.004

    #ScienceArrays
    self.HouseScience = [0.125, 0.125]
    self.CapitalScience = [0.125, 0.125]
    self.RawScience = [0.125, 0.125, 0.125, 0.125]

    #ScienceArraysCummulated
    self.HouseScienceAm = [10, 10]
    self.CapitalScienceAm = [10, 10]
    self.RawScienceAm = [10, 10, 10, 10]

    #Runs demography
    self.setup_demography()

    #Variables, var_list is the name of array, variable_list is variable name.
    #They should be the same.
    self.var_list = ['EducationArr2','Government_SavingsArr','TarriffRevenuArr','GovDebtArr','Income_Tax','Corporate_Tax','MoneyPrintingArr','Iron','Wheat','Coal','Oil','Food','ConsumerGoods','Steel','Machinery']
    self.variable_list = ['Education','Government_Savings','TariffRevenue','GovDebt','IncomeTax','CorporateTax','MoneyPrinting','RawPrices0#','RawPrices1#','RawPrices2#','RawPrices3#','HousePrices0#','HousePrices1#','CapitalPrices0#','CapitalPrices1#']
    self.save_variable_list(self.var_list)
    
  def save_variable_list(self, var_list):
    for i in var_list:
      setattr(self,i,[])
  def append_variable_list(self, var_list, variable_list):
    for i in range(0,len(var_list)):
      if variable_list[i][len(variable_list[i])-1] == '#':
        getattr(self,var_list[i]).append(getattr(self, variable_list[i][0:len(variable_list[i])-2])[int(variable_list[i][len(variable_list[i])-2])])
      else:
        getattr(self,var_list[i]).append(getattr(self, variable_list[i]))
  def run_first(self):
    #Stats:
    #GDP
    self.money[1] += 10
    print("Total Savings"+str(self.money[1]))
    #GDP = money[2]+money[3]+money[5]
    print('GDP: '+str(self.money[8]))

    #M0
    self.M0 = self.money[0]+self.money[1]+self.money[2]+self.money[3]+self.money[4]+self.money[5]
    print('M0: '+str(self.M0))

    #Calculates Inflation
    #ConsumerPrice = money[2]/goods[2] + money[3]/goods[1]
    self.lastConsumerPrice = self.ConsumerPrice
    self.ConsumerPrice = self.money[2]/self.goods[0] + self.money[3]/((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.goods[1])
    self.Inflation = (self.ConsumerPrice/self.lastConsumerPrice - 1)*100
    print('Inflation: '+str(self.Inflation))
    
    #Savings:
    if self.Inflation >= 0:
      self.SavingsRate += -0.01*self.SavingsRate*self.SavingsRate*self.Inflation
    else:
      self.SavingsRate += -0.02*(self.SavingsRate-1)*(self.SavingsRate-1)*self.Inflation

    #Interest Rates:
    self.interest_rate = -0.5*np.exp(-(self.money[1]/(self.money[3]/(self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods)))))+1
    self.interest = self.interest_rate*self.Corporate_Cummalative_Loans
    self.Corporate_Cummalative_Loans += (self.interest_rate*self.money[1]*self.CorporateDebtRate - self.interest)
    self.GovDebt = 0
    print("Interest_Rate: "+str(self.interest_rate))
    print("Interest: "+str(self.interest))

    #Investment Cell
    self.ScienceInvest = 0.05
    self.TheoreticalInvest = 0.1
    self.PracticalInvest = 0.3
    self.AppliedInvest = 0.6
    self.InfrastructureInvest = 0.1
    self.QuickInvestment = 0.85

    self.InvestmentDirString = ['Theoretical','Practical','Applied','Infrastructure','QuickInvestment']
    self.InvestmentDirection = [self.ScienceInvest*self.TheoreticalInvest,self.ScienceInvest*self.PracticalInvest,self.ScienceInvest*self.AppliedInvest,self.InfrastructureInvest,self.QuickInvestment]
    self.Geniuses = 5
    self.time = 0
    self.Researchers = 10
    self.Innovators = 10

    #Update Investment:
    self.Theoretical = (-20*self.time*np.exp(-(1/(self.Geniuses+self.time))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[0])*self.goods[1])+20*self.time)/self.goods[1]
    self.Practical = (-self.Theoretical*np.exp(-(1/(self.Researchers))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[1])*self.goods[1])+self.Theoretical)/self.goods[1]
    self.Applied = (-self.Theoretical*np.exp(-(1/(self.Innovators))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[2])*self.goods[1])+self.Theoretical)/self.goods[1]

    self.StructuralUnemployment = 0

    #Science:
    self.ScienceDivHouse = [1,1]


  def run_turn(self, num):
    for i in range(0,num):
      self.TariffRevenue = 0
      self.TransportRevenue = 0
      self.lastcapital = self.capital
      self.lastPopulation = self.Population
      #Values matrix
      self.transG1 = np.zeros((5,5))
      #Transformation Matrix
      #self.GovernmentInvest
      self.ConsumptionRate = 1 - self.SavingsRate - self.IncomeTax
      self.trans1 = np.array([[0,self.PersonalWithdrawls,0,0,self.Wages,self.GovWelfare,0,0,0,0],
                        [self.SavingsRate,0,0,0,1-self.Wages-self.CorporateTax-self.InvestmentRate+(self.interest/self.money[4]),0,0,0,0,1],
                        [self.ConsumptionRate,1 - self.CorporateDebtRate,0,0,0,0,0,0,0,0],
                        [0,self.CorporateDebtRate,0,0,self.InvestmentRate,self.GovernmentInvest,0,0,0,0],
                        [0,self.CorporateWithdrawls,1,1,0,self.GovGoods,0,0,0,0],
                        [self.IncomeTax,self.Bonds,0,0,self.CorporateTax,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0],
                        [0,0,1,1,0,1,0,0,0,0],
                        [0,0,0,0,0,0,0,0,0,0]])
      self.Employable = self.Population - self.StructuralUnemployment*self.Population
      #Initialization for values matrix
      #self.transG1[0][0] = 0
      #self.transG1[2][2] = 0
      #self.transG1[1][1] = (-self.Employable*self.ScienceRate*np.exp((-4/(self.Employable*self.ScienceRate))*self.capital)+self.ScienceRate*self.Employable)/self.goods[1] #(-ScienceRate*np.exp((-Invest_Left*(money[3]/(money[2]+money[3]+money[5]*GovGoods))*QuickInvestment)*goods[1])+ScienceRate)/goods[1] + 1
      #self.transG1[0][1] = self.money[2]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods)
      #self.transG1[2][1] = self.money[5]*self.GovGoods/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods)
      #(-Population*ScienceRate*np.exp((-4/(Population*ScienceRate))*capital)+ScienceRate)/goods[1]
      self.Infrastructure_Real = (((self.money[3]*self.InvestmentDirection[3])/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[3]*self.goods[1] - self.ScienceRate)*0.0003
      self.Infrastructure = min(0.1,self.Infrastructure_Real)
      
      #self.Infrastructure = 0.1
      self.run_demography()
      Total = 1
      #Total = (-self.Employable*self.ScienceRate*np.exp((-4/(self.Employable*self.ScienceRate))*self.capital)+self.ScienceRate*self.Employable)*(0.9+self.Infrastructure)
      self.calculateProduction(self.capitalChange2) #self.capital - self.last_capital2
      #print(Total)
      #if self.goods[0] >= 0.1:
      #  self.goods[0] *= ((self.money[2]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*Total)/self.goods[0]
      #if self.goods[1] > 0.1:
      #  self.goods[1] *= ((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*Total)/self.goods[1]
      print("Goods 2: ", self.goods[2])
      #print("Total: ", Total)
      print("Money: ", self.money[5]*self.GovGoods/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))
      #if self.goods[2] != 0:
        #self.goods[2] *= ((self.money[5]*self.GovGoods/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*Total)/self.goods[2]
      #self.goods[3] *= ((self.money[3]*self.RawInvestment/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*Total)
      #Run each cycle, creates transformation matrix
      if self.money[1] < 0:
        self.money[1] = 5
      if self.money[3] < 0:
        self.money[3] = 5
      if self.money[4] < 0:
        self.money[4] = 5
      
      #Runs money matrix with trans1
      self.money = np.dot(self.trans1,self.money)

      if self.money[3] < 0:
        self.money[3] = 5
      if self.money[1] < 0:
        self.money[1] = 5
      if self.money[4] < 0:
        self.money[4] = 5
      #self.goods = np.dot(self.transG1,self.goods)

      #Calculates Inflation
      #ConsumerPrice = money[2]/goods[2] + money[3]/goods[1]
      self.lastConsumerPrice = self.ConsumerPrice
      self.ConsumerPrice = self.money[2]/self.goods[0] + self.money[3]/((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.goods[1])
      self.Inflation = (self.ConsumerPrice/self.lastConsumerPrice - 1)*100
      if self.Inflation < -50 and self.time < 20:
        self.Inflation = -50
      if self.Inflation > 100 and self.time < 20:
        self.Inflation = 100
      print('Inflation: '+str(self.Inflation))

      #Savings
      self.Corporate_Savings += (1-self.Wages-self.CorporateTax-self.InvestmentRate+(self.interest/self.money[4]))*self.money[4]
      self.Household_Savings += self.SavingsRate*self.money[0]
      if not (self.money[5] < 0 or 1-self.GovWelfare-self.GovGoods-self.GovernmentInvest < 0):
        if self.GovDebt > 1:
          self.GovDebt -= (1-self.GovWelfare-self.GovGoods-self.GovernmentInvest)*self.money[5]
        else:
          self.Government_Savings += (1-self.GovWelfare-self.GovGoods-self.GovernmentInvest)*self.money[5]
      self.Government_Savings *= (1+self.interest_rate)
      self.pos_interest_payments.append(self.Government_Savings*self.interest_rate)
      #Population adding:
      self.Population = self.pop_matrix.sum()#self.Population*self.Population_growth
      
      #Structural Unemployment and Education
      self.Education = (self.GovernmentGoods[0]*self.EducationSpend)/self.Education_Divisor
      self.Military += (self.GovernmentGoods[1]*self.MilitarySpend)
      #print(goods[2]/(goods[0]+goods[1]+goods[2]))
      #1 - (self.employment)/self.Population
      print("Unemployment:"+str(self.Unemployment))
      Education_Unemployment = (self.ScienceRate - self.Education*0.02)*0.003
      if Education_Unemployment < 0:
        Education_Unemployment = 0
      if len(self.InflationTracker) > 15:
        inflation_expectation = max(min(sum(self.InflationTracker[-8:])/8, 20), -1.5)
        variation = stat.stdev(self.InflationTracker[8:])
        print("Variation: ",variation, " Inflation Expectation: ",inflation_expectation)
        avg_inflation = sum(self.InflationTracker[-3:])/3
        NewPhillips = min(np.exp(-(variation / 10)*(self.Inflation - inflation_expectation - 1)) + 1, 6)
        
        oldPhillps = self.Phillips
        self.Phillips = NewPhillips #sum(self.PhillipsArr[-4:])/4
        

        if self.Phillips > oldPhillps + 0.25:
          self.Phillips = oldPhillps + 0.25
        elif self.Phillips < oldPhillps - 0.25:
          self.Phillips = oldPhillps - 0.25

        if self.time > 25 and abs(oldPhillps - self.PhillipsArr[len(self.PhillipsArr) - 3]) <= 0.1:
          self.Phillips = oldPhillps
      else:
        self.Phillips = 0
      self.PhillipsArr.append(self.Phillips)
      self.StructuralUnemployment = Education_Unemployment + self.Phillips/100
      if self.StructuralUnemployment < 0:
        self.StructuralUnemployment = 0
      self.Unemployment = self.StructuralUnemployment
      print(self.StructuralUnemployment)
      #Stats:
      print("New Year \n")
      #print((-Population*ScienceRate*np.exp((-4/(Population*ScienceRate))*employment*ScienceRate)+ScienceRate*Population)/goods[1])
      #print(ScienceRate)
      #GDP
      #self.money[1]
      print("Total Savings"+str(self.money[1]))
      #GDP = money[2]+money[3]+money[5]
      print('GDP: '+str(self.money[8]))

      #M0
      self.M0 = self.money[0]+self.money[1]+self.money[2]+self.money[3]+self.money[4]+self.money[5]
      print('M0: '+str(self.M0))

      #Money Printing
      self.money[9] += self.MoneyPrinting
      
      #Savings:
      if self.Inflation >= 0:
        change = -0.01*self.SavingsRate*self.SavingsRate*self.Inflation
        if change < 0.1 and change > -0.1:
          self.SavingsRate += change
      else:
        change = -0.02*(self.SavingsRate-1)*(self.SavingsRate-1)*self.Inflation
        if change < 0.1 and change > -0.1:
          self.SavingsRate += change
      if self.SavingsRate >= (0.9 - self.IncomeTax):
        self.SavingsRate = 0.9 - self.IncomeTax

      #Interest Rates:
      self.investment_good_price = self.money[3]/self.goods[1]
      self.interest_rate = (self.ScienceRate*0.3*pow(self.capital + (self.money[1] - self.BondWithdrawl)/self.investment_good_price, 0.3 - 1)*pow(self.Employable, 0.6))*1 + 0.02 #+ self.Inflation*0.01
      #-0.7*np.exp(((self.Population*self.ScienceRate - self.capital)*-1)/((self.money[1] - self.BondWithdrawl)/self.investment_good_price))+0.7
      self.interest = self.interest_rate*self.Corporate_Cummalative_Loans
      self.Corporate_Cummalative_Loans += (self.interest_rate*self.money[1]*self.CorporateDebtRate - self.interest)
      self.PersonalWithdrawls = (self.interest_rate*(self.Household_Savings/(self.Household_Savings+self.Corporate_Savings)))/2
      print("PersonalWithdrawls "+str(self.PersonalWithdrawls))
      print("Interest_Rate: "+str(self.interest_rate))
      print("Interest: "+str(self.interest))
      self.investment_good_price = self.money[3]/self.goods[1]
      self.Bonds *= (1 + self.interest_rate)
      self.money[5] += self.BondWithdrawl
      self.money[1] -= self.BondWithdrawl
      self.GovDebt *= (1 + self.interest_rate)
      self.neg_interest_payments.append(self.GovDebt*self.interest_rate)
      if (self.Government_Savings + self.BondWithdrawl) < 1:
        self.GovDebt +=  self.BondWithdrawl
      else:
        self.Government_Savings -= self.BondWithdrawl
      #print("InterestRate2: "+str(-0.7*np.exp(((Population*ScienceRate - capital)*-1)/(money[1]/investment_good_price))+0.7))
      #Update Invest
      self.TotalInvest += self.money[3]
      self.InvestLeft = (self.Population - self.Researchers - self.Innovators)*self.ScienceRate-self.capital

      #Investment Cell
      #self.ScienceInvest = 0.2
      #self.TheoreticalInvest = 0.2  
      #self.PracticalInvest = 0.4
      #self.AppliedInvest = 0.4
      #self.InfrastructureInvest = 0.1
      #self.QuickInvestment = 0.7

      self.InvestmentDirString = ['Theoretical','Practical','Applied','Infrastructure','QuickInvestment']
      self.InvestmentDirection = [self.ScienceInvest*self.TheoreticalInvest,self.ScienceInvest*self.PracticalInvest,self.ScienceInvest*self.AppliedInvest,self.InfrastructureInvest,self.QuickInvestment]
      self.Geniuses = self.Geniuses*self.Population_growth
      self.time = self.time + 1
      self.Researchers = sum(self.pop_matrix[len(self.pop_matrix) - 2][20:self.retirement_age])#self.Researcher_Percentage*self.Population
      self.Innovators = sum(self.pop_matrix[len(self.pop_matrix) - 1][20:self.retirement_age]) #self.Innovators_Percentage*self.Population
      
      #Resentment
      temp_inflation = abs(max(self.Inflation,0))
      if len(self.ConsumptionArr) >= 1:
        consumption_change =  (self.goods[0]/self.Population - self.ConsumptionArr[len(self.ConsumptionArr) - 1])/self.ConsumptionArr[len(self.ConsumptionArr) - 1] 
      else:
        consumption_change = 0
      if (self.time > 12):
         temp_resentment = pow(temp_inflation*0.01, 0.3)*pow(consumption_change + 1, -0.4)*pow(self.Unemployment, 0.3)*0.4
         self.Resentment = self.Resentment*0.8 + temp_resentment*0.2
      else:
        self.Resentment = 0
      self.ResentmentArr.append(self.Resentment)
      #Capital amount
      #self.capital *= self.capital_destruction
      #self.capital += (self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[4]*self.goods[1] #min((money[3]/(money[2]+money[3]+money[5]*GovGoods))*InvestmentDirection[4]*goods[1], (Population - Researchers - Innovators)*ScienceRate)
      self.last_capital2 = self.capital
      self.capital += self.goods[1]
      #Infrastructure Invest
      #self.capital += ((self.money[3]*self.InvestmentDirection[3])/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[3]*self.goods[1]
      self.last_capital = self.capital
      self.employment = sum(self.pop_matrix.sum(axis=0)[20:self.retirement_age]) - self.StructuralUnemployment*sum(self.pop_matrix.sum(axis=0)[20:self.retirement_age])
      #self.employment = self.capital/self.ScienceRate
      #(Population - Researchers - Innovators)
      #if (self.employment - self.Researchers - self.Innovators - self.StructuralUnemployment*self.Population)/self.Population >= 1:
      #  self.capital = self.ScienceRate*(self.Population - self.Researchers - self.Innovators - self.StructuralUnemployment*self.Population) #*(1-self.Resentment)
      #  self.employment = self.capital/self.ScienceRate

      capital_destroyed = self.lastcapital - self.capital
      capital_percentage = capital_destroyed/self.last_capital
      self.PercentNPL.append(capital_percentage)
      #self.Household_Savings *= (1 - capital_percentage)
      #self.Corporate_Savings *= (1 - capital_percentage)
      #print("Capital Percentage: "+str(capital_percentage))
      #Calculate Capital Distribution
      self.capital_distribution = self.create_distribution([0 for i in range(0, len(self.centers))], self.centers, self.capital, self.hexNum)

      #Calculate Population Distribution
      self.population_distribution = self.create_distribution([0 for i in range(0, len(self.centers))], self.centers, self.Population, self.hexNum)

      #Update Investment:
      #self.Applied = (-self.Practical*np.exp(-(4/(self.Innovators*0.1))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[2]*self.ScienceEff)*self.goods[1])+self.Practical)
      #self.Practical = (-self.Theoretical*np.exp(-(4/(self.Researchers*0.1))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[1]*self.ScienceEff)*self.goods[1])+self.Theoretical)
      #self.Theoretical = (-1*(self.time)*np.exp(-(4/(self.Geniuses+(self.time)))*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[0]*self.ScienceEff)*self.goods[1])+1*self.time)
      self.Applied = self.ScienceEff*self.Practical*pow(self.Innovators,0.4)*pow(0.01*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[2]*self.goods[1]),0.6)
      self.Practical = self.ScienceEff*self.Theoretical*pow(self.Researchers,0.6)*pow(0.01*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[1]*self.goods[1]),0.4)
      self.Theoretical = self.ScienceEff*pow(self.time,0.4)*pow(self.Geniuses,0.6)*pow(0.01*((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*self.InvestmentDirection[0]*self.goods[1]),0.4)

      lastScience = self.ScienceRate
      self.ScienceRate += self.Applied/self.scienceDivisor

      #Update Science:
      growth = (self.ScienceRate/lastScience) - 1
      self.update_science_array(self.HouseScience, self.HouseScienceAm, growth)
      self.update_science_array(self.CapitalScience, self.CapitalScienceAm, growth)
      self.update_science_array(self.RawScience, self.RawScienceAm, growth)
      
      print("Time"+str(self.time))
      #Good Price changes:
      self.wheat_price = (self.HouseDemand[0]*self.money[2])/(self.HouseProduction[0]*self.goods[0])
      print(self.wheat_price)
      for i in range(0,len(self.HouseDemand)):
        self.HousePrices[i] = (self.HouseDemand[i]*self.money[2])/(self.HouseProduction[i]*self.goods[0])
      for i in range(0,len(self.CapitalDemand)):
        self.CapitalPrices[i] = (self.CapitalDemand[i]*self.money[3]*self.QuickInvestment)/(self.CapitalProduction[i]*self.goods[1])
      #for i in range(0,len(self.RawDemand)):
      #  self.RawPrices[i] = (self.RawDemand[i]*self.money[3]*self.QuickInvestment)/(self.RawProduction[i]*self.goods[3])

      #Adding budget variables in:
      self.CorporateTaxArr.append(self.money[4]*self.CorporateTax)
      self.IncomeTaxArr.append(self.money[0]*self.IncomeTax)
      govshare = (self.GovernmentInvest*self.money[5])/(self.GovernmentInvest*self.money[5]+self.InvestmentRate*self.money[4])
      self.InfrastructureArr.append(self.money[3]*self.InfrastructureInvest*govshare)
      self.ScienceBudgetArr.append(self.money[3]*self.ScienceInvest*govshare)
      self.WelfareArr.append(self.money[5]*self.GovWelfare)
      self.EducationArr.append(self.money[5]*self.GovGoods*self.EducationSpend)
      self.MilitaryArr.append(self.money[5]*self.GovGoods*(1-self.EducationSpend))

      #Stats Adding:
      self.append_variable_list(self.var_list, self.variable_list)
      self.GDPPerCapita.append(((self.money[8]*50)/self.ConsumerPrice)/self.pop_matrix.sum())
      self.GoodsTotal.append(self.goods[0]+self.goods[1]+self.goods[2]+self.tradeBalance)
      self.GoodsPerCapita.append(self.GoodsTotal[len(self.GoodsTotal)-1]/self.pop_matrix.sum())
      #print(GoodsTotal[len(GoodsTotal)-1]/Population)
      self.GDP.append(self.money[8]);
      self.GDPGrowth.append((self.GDP[len(self.GDP)-1]/self.GDP[len(self.GDP)-2] - 1)*100)
      self.RealGDPGrowth.append((self.GDP[len(self.GDP)-1]/self.GDP[len(self.GDP)-2] - 1)*100 - self.Inflation)
      #print("GDPGrowth: "+ str(GDPGrowth[len(GDPGrowth)-1]))
      #print("RealGDPGrowth: "+ str(RealGDPGrowth[len(RealGDPGrowth) - 1]))
      #print()
      self.Savings.append(self.money[1]);
      self.InflationTracker.append(self.Inflation);
      self.Investment.append(self.money[3]);
      self.EmploymentRate.append(self.employment/self.pop_matrix.sum())
      self.ConsumptionArr.append(self.goods[0]/self.pop_matrix.sum())
      self.AppliedArr.append(self.Applied)
      self.CapitalArr.append(self.capital)
      self.ScienceArr.append(self.ScienceRate)
      self.InterestRate.append(self.interest_rate)
      self.PopulationArr.append(self.pop_matrix.sum())
      self.Household_SavingsArr.append(self.Household_Savings)
      self.Corporate_SavingsArr.append(self.Corporate_Savings)
      self.GoodsBalance.append(self.tradeBalance)
      self.InfrastructureArray.append(self.Infrastructure)
      print(self.tradeBalance)
      self.UnemploymentArr.append(self.Unemployment)
      #Resets
      self.tradeBalance = 0

  def update_science_array(self, percent_array, array, growth):
    for i in range(0,len(array)):
      array[i] *= (1 + growth*percent_array[i]*(len(self.HouseScience)+len(self.CapitalScience)+len(self.RawScience)))

  def calculateProduction(self, capitalChange):
    print("capitalChange: ", capitalChange)
    house_goods = 0
    capital_goods = 0
    gov_goods = 0
    raw_goods = [0 for i in range(0,len(self.RawDemand))]
    for i in range(0, len(self.RawDemand)):
      print("Raw i",i)
      print(len(self.RawPrices))
      self.RawCapital[i] *= 0.9
      self.RawCapital[i] += capitalChange*(self.RawDemand[i])*(self.money[3]/self.findMoneyTotal())
      labour = sum(self.pop_matrix[len(self.HouseDemand)+len(self.CapitalDemand) + i][20:self.retirement_age])/self.pop_matrix.sum()
      raw_goods[i] += self.production_function(self.RawDemand[i], self.RawCapital[i], self.RawScienceAm[i], self.RawResources[i]*100)
      raw_goods[i] += (self.RawDemand[i]/sum(self.RawDemand))*self.goods[3]
      self.RawPrices[i] = (self.RawDemand[i]*self.money[3]*self.QuickInvestment)/((self.RawDemand[i]/sum(self.RawDemand))*raw_goods[i])
    for i in range(0,len(self.HouseDemand)):
      self.HouseCapital[i] *= 0.9
      self.HouseCapital[i] += capitalChange*self.HouseDemand[i]*(self.money[2]/self.findMoneyTotal())
      labour = sum(self.pop_matrix[i][20:self.retirement_age])/self.pop_matrix.sum()
      house_goods += self.production_function(self.HouseDemand[i], self.HouseCapital[i], self.HouseScienceAm[i], labour, raw_goods[1]*raw_goods[3]*0.1*self.HouseProduction[i]*0.01)
    for j in range(0, len(self.CapitalDemand)):
      self.CapitalCapital[j] *= 0.9
      self.CapitalCapital[j] += capitalChange*(self.CapitalDemand[j])*(self.money[3]*self.InvestmentDirection[4]/self.findMoneyTotal())
      labour = sum(self.pop_matrix[len(self.HouseDemand) + j][20:self.retirement_age])/self.pop_matrix.sum()
      capital_goods += self.production_function(self.CapitalDemand[j], self.CapitalCapital[j], self.CapitalScienceAm[j], labour, raw_goods[0]*raw_goods[2]*0.1*self.CapitalProduction[i]*0.01)
    
    GovDemand = [0 for i in range(0, len(self.GovCapital))]
    GovDemand[0] = self.EducationSpend*self.GovGoods
    GovDemand[1] = self.MilitarySpend*self.GovGoods
    for j in range(0, len(self.GovCapital)):
      self.GovCapital[j] *= 0.9
      self.GovCapital[j] += capitalChange*(GovDemand[j])*(self.money[3]*self.InvestmentDirection[4]/self.findMoneyTotal())
      labour = sum(self.pop_matrix[len(self.HouseDemand) + len(self.CapitalDemand) +len(self.RawDemand) + j][20:self.retirement_age])/self.pop_matrix.sum()
      if j != 0:
        gov_goods += self.production_function(GovDemand[j], self.GovCapital[j], self.ScienceRate, labour, raw_goods[3]*raw_goods[0]*0.05)
        self.GovernmentGoods[j] = self.production_function(GovDemand[j], self.GovCapital[j], self.ScienceRate, labour, raw_goods[3]*raw_goods[0]*0.05)
      else:
        gov_goods += self.production_function(GovDemand[j], self.GovCapital[j], self.ScienceRate, labour)
        self.GovernmentGoods[j] = self.production_function(GovDemand[j], self.GovCapital[j], self.ScienceRate, labour)
    print("House goods: ", house_goods)
    if self.goods[0] >= 0.1 and not math.isnan(house_goods):
      self.goods[0] *= ((self.money[2]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*house_goods)/self.goods[0]
    if self.goods[1] > 0.1 and not math.isnan(capital_goods):
      self.goods[1] *= ((self.money[3]/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*capital_goods)/self.goods[1]
    self.capitalChange2 = self.goods[1]
    if self.goods[2] >= 0.1 and not math.isnan(gov_goods):
      self.goods[2] *= ((self.money[5]*self.GovGoods/(self.money[2]+self.money[3]+self.money[5]*self.GovGoods))*gov_goods)/self.goods[2]
    else:
      self.goods[2] = 0.1
    
  def production_function(self, percentage, capital, scienceRate, employment=1, extra=1):
    #Total = (-self.Employable*percentage*self.ScienceRate*extra*np.exp((-4/(self.Employable*percentage*self.ScienceRate*extra))*capital)+self.ScienceRate*self.Employable*percentage*extra)*(0.9+self.Infrastructure)
    #print("Extra", extra)
    if extra != 1:
      Total = scienceRate*pow(capital*0.2, 0.3)*pow(self.Employable*employment*5, 0.6)*pow(extra, 0.1)*(0.9+self.Infrastructure)
    else:
      Total = scienceRate*pow(capital*0.2, 0.3)*pow(self.Employable*employment*5, 0.7)*(0.9+self.Infrastructure)
    return Total
  
  def findMoneyTotal(self):
    return self.money[2]+self.money[3]+self.money[5]*self.GovGoods
  
  #def distribute_emp(self):
  def getMilitaryGoods(self):
    return self.goods[2]*self.MilitarySpend
  
  def setup_demography(self):
    total_jobs = len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 4
    self.pop_matrix = np.concatenate((np.zeros((total_jobs,20)), np.array([np.arange(10,8.62,-0.02) for i in range(total_jobs)])), axis=1)
    self.multiplier = np.diagflat([1-0.0000000000000001*pow(i,8) for i in range(0,89)], k=1)
    for i in range(19,0,-1):
      self.pop_matrix[0][i] = self.pop_matrix.sum()*(self.Population_growth - 1)#total_jobs * 10 * (0.02*0.05)
    for i in range(0,90):
      self.run_demography()

  def run_demography(self):
    self.pop_matrix = np.dot(self.pop_matrix, self.multiplier)
    self.pop_matrix[0][0] = self.pop_matrix.sum()*(self.Population_growth - 1)
    GovDemand = [0 for i in range(0, len(self.GovCapital) + 2)]
    GovDemand[0] = self.EducationSpend
    GovDemand[1] = self.MilitarySpend
    #Change both of these below later
    GovDemand[2] = self.Researcher_Percentage
    GovDemand[3] = self.Innovators_Percentage
    total_arr = []
    for i in range(0,len(self.HouseDemand)):
      Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*self.HouseEducation[i])*0.003
      a = self.HouseDemand[i]*(self.money[2]/self.findMoneyTotal())*Education_Unemployment
      if a < 0.9:
        total_arr.append(a)
        #self.pop_matrix[i][20] = a*self.pop_matrix[0][19]
      else:
        total_arr.append(0.25)
        #self.pop_matrix[len(self.HouseDemand) + i][20] = 0.25*self.pop_matrix[0][19]
    for i in range(0, len(self.CapitalDemand)):
      Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*self.CapitalEducation[i])*0.003
      a = self.CapitalDemand[i]*((self.money[3]*self.InvestmentDirection[4])/self.findMoneyTotal())*Education_Unemployment
      if a < 0.9:
        total_arr.append(a)
        #self.pop_matrix[len(self.HouseDemand) + i][20] = a*self.pop_matrix[0][19]
      else:
        total_arr.append(0.25)
        #self.pop_matrix[len(self.HouseDemand) + i][20] = 0.25*self.pop_matrix[0][19]
    for i in range(0, len(self.RawDemand)):
      Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*self.RawEducation[i])*0.003
      a = self.RawDemand[i]*((self.money[3]*self.InvestmentDirection[4])/self.findMoneyTotal())*Education_Unemployment
      if a < 0.9:
        total_arr.append(a)
        #self.pop_matrix[len(self.HouseDemand) + len(self.CapitalDemand) + i][20] = a*self.pop_matrix[0][19]
      else:
        total_arr.append(0.25)
        #self.pop_matrix[len(self.HouseDemand) + i][20] = 0.25*self.pop_matrix[0][19]
    self.GovEducation = [4,1]
    for i in range(0, 2):
      Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*self.GovEducation[i])*0.003
      a = GovDemand[i]*((self.money[5]*self.GovGoods)/self.findMoneyTotal())
      if a < 0.9:
        total_arr.append(a)
        #self.pop_matrix[len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + i][20] = a*self.pop_matrix[0][19]
      else:
        total_arr.append(0.25)
        #self.pop_matrix[len(self.HouseDemand) + i][20] = 0.25*self.pop_matrix[0][19]
    #Researchers
    Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*5)*0.003
    a = ((self.money[3]*self.InvestmentDirection[1])/self.findMoneyTotal())*Education_Unemployment
    total_arr.append(a)
    #self.pop_matrix[len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 1 + 1][20] = self.pop_matrix[0][19]*((self.money[3]*self.InvestmentDirection[1])/self.findMoneyTotal()) #GovDemand[i]*(self.money[5]*self.GovGoods/self.findMoneyTotal())
    #Innovators
    Education_Unemployment = 1 - (self.ScienceRate - self.Education*0.02*4)*0.003
    a = ((self.money[3]*self.InvestmentDirection[2])/self.findMoneyTotal())*Education_Unemployment
    total_arr.append(a)
    #print("Demand arr", total_arr)
    total_arr = self.normalize(total_arr)
    #print("Demand arr", total_arr)
    for i in range(0,len(self.pop_matrix)):
      self.pop_matrix[i][20] = self.pop_matrix[0][19]*total_arr[i]
    #self.pop_matrix[len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 1 + 2][20] = self.pop_matrix[0][19]*((self.money[3]*self.InvestmentDirection[2])/self.findMoneyTotal())
  
  def normalize(self, arr):
    sum2 = sum(arr)
    for i in range(0,len(arr)):
      arr[i] = arr[i]/sum2
    return arr
  
  def add_population(self, other_pop_matrix, population_added):
    percentage = population_added/self.pop_matrix.sum()
    self.pop_matrix = self.pop_matrix + percentage*other_pop_matrix

  def create_graph(self, var_list, cutoff):
    for i in var_list:
      plt.plot(getattr(self,i)[cutoff:])
      plt.title(i)
      plt.ylabel(i)
      plt.xlabel('Years')
      plt.show()
      
  def display_data(self):
    self.create_graph(self.var_list, 15)
    plt.plot(self.GDP[5:])
    plt.title('GDP')
    plt.ylabel('GDP')
    plt.show()

    plt.plot(self.UnemploymentArr[20:])
    plt.title('Unemployment')
    plt.ylabel('Unemployment')
    plt.show()

    plt.plot(self.PhillipsArr[20:])
    plt.title('Phillips')
    plt.ylabel('Unemployment')
    plt.show()

    plt.title('Applied')
    plt.plot(self.AppliedArr[20:])
    plt.ylabel('Applied')
    plt.show()

    plt.plot(self.Savings[20:])
    plt.title('Savings')
    plt.ylabel('Savings')
    plt.show()

    plt.plot(self.InflationTracker[20:])
    plt.title('Inflation')
    plt.ylabel('Inflation')
    plt.show()

    plt.title('Investement')
    plt.plot(self.Investment[20:])
    plt.ylabel('Investement')
    plt.show()

    plt.title('GDPGrowth')
    plt.plot(self.GDPGrowth[20:])
    plt.ylabel('GDPGrowth')
    plt.show()

    plt.title('RealGDPGrowth')
    plt.plot(self.RealGDPGrowth[20:])
    plt.ylabel('RealGDPGrowth')
    plt.show()

    plt.title('GoodsProduction')
    plt.plot(self.GoodsTotal[20:])
    plt.ylabel('Goods')
    plt.show()

    plt.title('GDPPerCapita')
    plt.plot(self.GDPPerCapita[20:])
    plt.ylabel('GDPperCapita')
    plt.show()

    plt.title('GoodsPerCapita')
    plt.plot(self.GoodsPerCapita[20:])
    plt.ylabel('Goods')
    plt.show()

    plt.title('Employment')
    plt.plot(self.EmploymentRate[20:])
    plt.ylabel('Employment')
    plt.show()

    plt.title('Capital')
    plt.plot(self.CapitalArr[20:])
    plt.ylabel('Capital')
    plt.show()

    plt.title('Science')
    plt.plot(self.ScienceArr[20:])
    plt.ylabel('Science Rate')
    plt.show()

    plt.title('Interest Rate')
    plt.plot(self.InterestRate[20:])
    plt.ylabel('Interest Rate')
    plt.show()

    plt.title('Population')
    plt.plot(self.PopulationArr[20:])
    plt.ylabel('Population')
    plt.show()


    plt.title('Consumption Per Capita')
    plt.plot(self.ConsumptionArr[20:])
    plt.ylabel('Consumption')
    plt.show()

    plt.title('Household Savings')
    plt.plot(self.Household_SavingsArr[20:])
    plt.ylabel('Household Savings')
    plt.show()

    plt.title('Corporate Savings')
    plt.plot(self.Corporate_SavingsArr[20:])
    plt.ylabel('Corporate Savings')
    plt.show()

    plt.title('Percentage of Non-Performing Loans to total loans')
    plt.plot(self.PercentNPL[20:])
    plt.ylabel('Percentage of Non-Performing Loans to total loans')
    plt.show()

    plt.title('Trade Balance')
    plt.plot(self.GoodsBalance[20:])
    plt.ylabel('Trade Balance')
    plt.show()

    plt.title('Infrastructure')
    plt.plot(self.InfrastructureArray[2:])
    plt.ylabel('Infrastructure')
    plt.show()

    plt.barh([i for i in range(0,90)],self.pop_matrix.sum(axis=0))
    plt.title('Demographics')
    plt.xlabel('Population')
    plt.ylabel('Age')
    plt.show()

    plt.barh(self.HouseProducts + self.CapitalGoods + self.RawGoods + ['Education','Military','Researchers','Entrepreneurs'],[sum(self.pop_matrix[i][20:70]) for i in range(0, len(self.pop_matrix))])
    plt.title('Jobs')
    plt.xlabel('Workers')
    plt.ylabel('Job')
    plt.show()

    plt.barh(self.HouseProducts + self.CapitalGoods + self.RawGoods + ['Education','Military','Researchers','Entrepreneurs'], self.create_wage_array())
    plt.title('Wages')
    plt.xlabel('Pay')
    plt.ylabel('Job')
    plt.show()

    plt.barh(self.HouseProducts + self.CapitalGoods + self.RawGoods, self.HousePrices + self.CapitalPrices + self.RawPrices)
    plt.title('Prices')
    plt.xlabel('Prices')
    plt.ylabel('Good')
    plt.show()
  
  def create_wage_array(self):
    wages = []
    for i in range(0,len(self.HouseDemand)):
      wages.append(self.get_wage(self.HouseProduction[i], i, 2, i))
    for i in range(0,len(self.CapitalDemand)):
      wages.append(self.get_wage(self.CapitalProduction[i], i, 3, len(self.HouseDemand) + i))
    for i in range(0,len(self.RawDemand)):
      wages.append(self.get_wage(self.RawProduction[i]*0.2, i, 3, len(self.HouseDemand) + len(self.CapitalDemand) + i))
    wages.append(self.get_wage(self.GovGoods*self.EducationSpend, 0, 5, len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 0))
    wages.append(self.get_wage(self.GovGoods*self.MilitarySpend, 0, 5, len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 1))
    wages.append(self.get_wage(self.InvestmentDirection[1], 0, 3, len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 2))
    wages.append(self.get_wage(self.InvestmentDirection[2], 0, 3, len(self.HouseDemand) + len(self.CapitalDemand) + len(self.RawDemand) + 3))
    return wages

  def get_wage(self, production_share, index, money_index, population_index):
    production_share
    return (self.money[money_index]*production_share*self.Wages)/(sum(self.pop_matrix[population_index][20:self.retirement_age]))
  
  def save_GoodsPerCapita(self, file):
    plt.title('GoodsPerCapita')
    plt.plot(self.GoodsPerCapita)
    plt.ylabel('Goods')
    plt.xlabel('Years')
    return plt.savefig(file)

  def save_graphs(self, file_path, player_name):
    warnings.filterwarnings("ignore")
    matplotlib.use('Agg')
    plt.title('GoodsPerCapita')
    plt.plot(self.GoodsPerCapita[17:])
    plt.ylabel('Goods')
    plt.xlabel('Years')
    plt.clf()

    a = []

    plt.title('Real GDP Growth')
    plt.plot(self.RealGDPGrowth[17:])
    plt.ylabel('Real GDP Growth')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'RealGDPGrowth')
    a.append(file_path+player_name+'RealGDPGrowth')
    plt.clf()

    labels = ['Welfare','Education','Military']
    sizes = [self.GovWelfare,self.EducationSpend*self.GovGoods,(1-self.EducationSpend)*self.GovGoods]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax1.axis('equal')
    plt.savefig(file_path+player_name+'GovBudget')
    a.append(file_path+player_name+'GovBudget')
    plt.clf()

    plt.title('Trade Balance')
    plt.plot(self.GoodsBalance[17:])
    plt.ylabel('Trade Balance')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'tradeBalance')
    a.append(file_path+player_name+'tradeBalance')
    plt.clf()

    plt.title('GDPPerCapita')
    plt.plot(self.GDPPerCapita[17:])
    plt.ylabel('GDPperCapita')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'GDPPerCapita')
    a.append(file_path+player_name+'GDPPerCapita')
    plt.clf()

    plt.title('Capital')
    plt.plot(self.CapitalArr[17:])
    plt.ylabel('Capital')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'Capital')
    a.append(file_path+player_name+'Capital')
    plt.clf()

    plt.title('GoodsProduction')
    plt.plot(self.GoodsTotal[17:])
    plt.ylabel('Goods')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'GoodsProduction')
    a.append(file_path+player_name+'GoodsProduction')
    plt.clf()

    plt.plot(self.GDP[17:])
    plt.title('GDP')
    plt.ylabel('GDP')
    plt.xlabel('Years')
    plt.savefig(file_path+player_name+'GDP')
    a.append(file_path+player_name+'GDP')
    plt.clf()

    plt.title('GDPGrowth')
    plt.plot(self.GDPGrowth[17:])
    plt.ylabel('GDPGrowth')
    plt.xlabel('GDPGrowth')
    plt.savefig(file_path+player_name+'GDPGrowth')
    a.append(file_path+player_name+'GDPGrowth')
    plt.clf()


    plt.close()

    return a
    
  def create_distribution(self, hexCapital, hexCenter, totalCapital, hexNum): 
    x = np.arange(0, hexNum, 1)
    if len(hexCapital) == 0:
      a = norm.pdf(x,0,1)
      multiplier = totalCapital
      finalCapital = [i*multiplier for i in a]
      return finalCapital
    for i in range(0,len(hexCapital)):
      hexCapital[i] = norm.pdf(x,hexCenter[i],1)
    print(totalCapital)
    a = [sum([hexCapital[j][i] for j in range(0,len(hexCapital))]) for i in range(0,len(hexCapital[0]))]
    multiplier = totalCapital
    finalCapital = [i*multiplier for i in a]
    return finalCapital
