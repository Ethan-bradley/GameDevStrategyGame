from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from collections import OrderedDict
from picklefield.fields import PickledObjectField

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Country(models.Model):
	name = models.CharField(max_length=100)
	color = models.CharField(max_length=50, default='#ffffff')
	large = models.BooleanField(default=False)

	def __str__(self):
		return self.name
#Game Class
class Game(models.Model):
	name = models.CharField(max_length=100)
	host = models.ForeignKey(User, on_delete=models.CASCADE)
	num_players = models.IntegerField(default=5)
	curr_num_players = models.IntegerField(default=0)
	color = models.CharField(max_length=50, default='#ffffff')
	neutral = models.CharField(max_length=100,default="Neutral")
	board_size = models.IntegerField(default=7)
	years_per_turn = models.IntegerField(default=1)
	year = models.IntegerField(default=0)
	GameEngine = PickledObjectField(default="")
	gameEnd = models.BooleanField(default = False)
	winner = models.CharField(max_length = 100, default = '')


class Player(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	host = models.BooleanField()
	game = models.ForeignKey("Game", on_delete=models.CASCADE, default="")
	country = models.ForeignKey("Country", on_delete=models.CASCADE, default="")
	#Whether ready or not for the next turn
	ready = models.BooleanField(default=False)
	color = models.CharField(max_length=50, default='#ffffff')
	robot = models.BooleanField(default=False)
	projection_unloaded = models.BooleanField(default=True)
	money = models.IntegerField(default=0)

	#Resources
	coal = models.IntegerField(default=0)
	iron = models.IntegerField(default=0)
	wheat = models.IntegerField(default=0)
	oil = models.IntegerField(default=0)
	food = models.IntegerField(default=0)
	wood = models.IntegerField(default=0)
	metal = models.IntegerField(default=0)
	sugar = models.IntegerField(default=0)
	gold = models.IntegerField(default=0)
	ammunition = models.IntegerField(default=0)
	#Country = PickledObjectField()
	#Government Variables:
	IncomeTax = models.FloatField(default=0.2)
	CorporateTax = models.FloatField(default=0.1)
	Welfare = models.FloatField(default=0.1)
	AdditionalWelfare= models.FloatField(default=0)
	Education = models.FloatField(default=0.05)
	Military = models.FloatField(default=0.01)
	Bonds = models.FloatField(default=0)
	MoneyPrinting = models.IntegerField(default=200)
	MilitaryAm = models.IntegerField(default=0)
	NationsDefeated = models.IntegerField(default=0)
	#Science Investment
	InfrastructureInvest = models.FloatField(default=0.017)
	ScienceInvest = models.FloatField(default=0.0)
	TheoreticalInvest = models.FloatField(default=0.1)
	PracticalInvest = models.FloatField(default=0.3)
	AppliedInvest = models.FloatField(default=0.6)

	#Restrictions
	investment_restriction = models.FloatField(default=0.0)

	def __str__(self):
		return self.name

	def get_country(self):
		return self.game.GameEngine.get_country_by_name(self.country.name)

	def modify_country(self, attr, set_am):
		self.game.GameEngine.modify_country_by_name(self.country.name, attr, set_am)
		self.game.save()

	def get_trade_var(self, var):
		return self.game.GameEngine.get_trade(self.game.GameEngine.get_country_index(self.country.name), var)

class Tariff(models.Model):
	curr_player = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	name = models.CharField(max_length=100)
	game = models.ForeignKey("Game", on_delete=models.CASCADE, default="")
	#players = models.ManyToManyField("Player")
	#for i in range(0,4):
	#	i = models.DecimalField(max_digits=70, decimal_places=50)
class IndTariff(models.Model):
	controller = models.ForeignKey(Tariff, db_index=True, on_delete=models.CASCADE)
	#key = models.CharField(max_length=100)
	key = models.ForeignKey("Player", on_delete=models.CASCADE)
	tariffAm = models.FloatField(default=0.1)
	sanctionAm = models.FloatField(default=0)
	moneySend = models.FloatField(default=0)
	militarySend = models.FloatField(default=0)
	nationalization = models.FloatField(default=1.0)

class PlayerProduct(models.Model):
	curr_player = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	name = models.CharField(max_length=100)
	game = models.ForeignKey("Game", on_delete=models.CASCADE, default="")
	#players = models.ManyToManyField("Player")
	#for i in range(0,4):
	#	i = models.DecimalField(max_digits=70, decimal_places=50)
class Product(models.Model):
	controller = models.ForeignKey("PlayerProduct", db_index=True, on_delete=models.CASCADE)
	#key = models.CharField(max_length=100)
	name = models.CharField(max_length=100)
	exportRestriction = models.FloatField(default=1)
	subsidy = models.FloatField(default=0.125)

class Hexes(models.Model):
	hexNum = models.IntegerField()
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE)
	color = models.CharField(max_length=50, default='#ffffff')
	start_country = models.ForeignKey("Country", on_delete=models.CASCADE, default='')
	name = models.CharField(max_length=50, default='none')
	center = models.BooleanField(default=False)
	water = models.BooleanField(default=False)
	xLocation = models.IntegerField(default=0)
	yLocation = models.IntegerField(default=0)
	population = models.IntegerField()
	capital = models.IntegerField(default=0)
	oil = models.IntegerField(default=0)
	iron = models.IntegerField(default=0)
	coal = models.IntegerField(default=0)
	wheat = models.IntegerField(default=0)
	food = models.IntegerField(default=0)
	wood = models.IntegerField(default=0)
	metal = models.IntegerField(default=0)
	sugar = models.IntegerField(default=0)
	gold = models.IntegerField(default=0)
	ammunition = models.IntegerField(default=0)
	def __str__(self):
		return self.name

class Economic(models.Model):
	hexnum = models.OneToOneField("Hexes", on_delete=models.CASCADE)
	controller = models.CharField(max_length=100)
	player_controller = models.OneToOneField("Player", on_delete=models.CASCADE)
	factory_num = models.IntegerField()
	resentment = models.DecimalField(max_digits=70, decimal_places=50)
	steel_prod = models.DecimalField(max_digits=70, decimal_places=50)
	oil_prod = models.DecimalField(max_digits=70, decimal_places=50)
	welfare = models.DecimalField(max_digits=70, decimal_places=50)
	population = models.DecimalField(max_digits=70, decimal_places=50)

class Building(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	location = models.ForeignKey("Hexes", on_delete=models.CASCADE)
	player_controller = models.ForeignKey("Player", on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	# (a) Integers used for locating the required variable in the building dictionary
	BUILD_RESOURCE = 0
	BUILD_COST = 1
	PROD_RESOURCE = 2
	PROD_OUTPUT = 3
	MAINTENANCE_RESOURCE = 4
	MAINTENANCE_COST = 5
	SYMBOL = 6
	# (b) Variables dedicated to each building
	CITY = "City"
	FACTORY = "Factory"
	FARM = "Farm"
	MINE = "Mine"
	LODGE = "Woodcutter's Lodge"
	PORT = "Port"
	MODES = [
		(CITY, 'City'),
		(FACTORY, 'Factory'),
		(FARM, 'Farm'),
		(MINE, 'Mine'),
		(LODGE, "Woodcutter's Lodge"),
		(PORT, "Port")
	]
	# (c) The building dictionary. Contains the building's output, maintenance cost, and its representative symbol
	# Refer to (a) for the function of each index value in the dictionary
	buildingDict = {
		'City': ['wood', 1, ['gold', 'wood', 'metal'], 1, 'wood', 1, '🏬'],
		'Factory': ['metal', 1, ['metal'], 1, 'metal', 1, '🔗'],
		'Farm': ['wood', 2, ['food'], 1, 'wood', 1, '🚜'],
		'Mine': ['metal', 2, ['metal'], 1, 'metal', 1, '⛏️'],
		'Lodge': ['wood', 3, ['wood'], 1, 'wood', 1, '🏠'],
		'Port': ['wood', 4, ['gold'], 1, 'gold', 1, '🚢']
	}
	building_type = models.CharField(max_length=20,choices=MODES,default=FARM)

	#Adds the resource production to the player's resources and subtracts maintenance cost
	def addResources(self):
		player = self.player_controller
		modify = self.buildingDict[self.building_type]
		curr_am_maintenance = getattr(player, modify[self.MAINTENANCE_RESOURCE])
		for resource in modify[self.PROD_RESOURCE]:
			curr_am = getattr(player, resource)
			if curr_am_maintenance - modify[self.MAINTENANCE_COST] >= 0:
				setattr(player, resource, curr_am + modify[self.PROD_OUTPUT])
		setattr(player, modify[self.MAINTENANCE_RESOURCE], curr_am_maintenance - modify[self.MAINTENANCE_COST])
		player.save()

	#Applies the cost of the building towards the player
	def applyCost(self):
		player = self.player_controller
		modify = self.buildingDict[self.building_type]
		curr_am = getattr(player, modify[self.BUILD_RESOURCE])
		#Return False if the player doesn't have enough the required resource
		if curr_am - modify[self.BUILD_COST] < 0:
			return False
		else:
			setattr(player, modify[self.BUILD_RESOURCE], curr_am - modify[self.BUILD_COST])
			player.save()
			return True
	#Returns the building's symbol for display
	def getSymbol(self):
		emoji = self.buildingDict[self.building_type][self.SYMBOL]
		return emoji

#adding the ships class
class Ship(models.Model):
	#add ship qualities(formatting to make them work on the game board)
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	location = models.ForeignKey("Hexes", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	ship_type = models.CharField(max_length=20,choices=MODES,default=NEW)

	#add ship attributes (keep in this order for proper initialization)
	max_health = models.IntegerField(default=0)
	health = models.IntegerField(default=0)
	damage = models.IntegerField(default=0)
	cost = models.IntegerField(default=0)
	movement = models.IntegerField(default=0)
	troop_count = models.IntegerField(default=0)
	troop_capacity = models.IntegerField(default=0)
	cool_down = models.IntegerField(default=0)
	reload_speed = models.FloatField(default=1.0)
	range_attack = models.FloatField(default=1.0)
	range_visibility = models.FloatField(default=1.0)

	#add ship_types
	NEW = "Default"
	MERCHANT = "Merchant Ship"
	COLONIZER = "Colonizer Ship"
	SMALLWARSHIP = "Small Warship"
	MEDIUMWARSHIP = "Medium Warship"
	BIGWARSHIP = "Big Warship"

	MODES = [
	(MERCHANT, "Merchant Ship"),
	(COLONIZER, "Colonizer Ship"),
	(BUBA DOCTOR, "Doctor Ship"),
	(TUGBOAT, "TugBoat Ship"),
	(SMALLWARSHIP, "Small Warship"),
	(MEDIUMWARSHIP, "Medium Warship"),
	(BIGWARSHIP, "Big Warship")
	]

	####init####
	#return: void ; initializes a specific ship model
	def initialize_ship(self):
		player = self.controller
		#separate into different ship_types and then specific ship_class
		ship_dict = {"Merchant Ship": [23,],"Colonizer Ship": [],"Merchant Ship": [],"Merchant Ship": [],"Merchant Ship": [],"Merchant Ship": []}
		fields = ["max_health","health","damage","cost","movement","troop_count","troop_capacity","cool_down","reload_speed","range_attack","range_visibility"]
		if(!check_funds()):
			return
		else:
			#disregard any bugs for getting free ship
			#set ship attributes based on ship_type
			for i,field_val in enumerate(ship_dict[self.ship_type]):
				setattr(self, fields[i], field_val)
			#update the player_funds with the curr_val
			player_funds = self.controller.money - self.cost
			#setattr(self, "controller", player_funds - self.cost)

	#return: bool ; checks if the player has sufficient funds
	def check_funds(self):
		#assume that money is the correct currency
		#a check for initialized ship
		if self.ship_type == "Default":
			return False
		return self.controller.money >= self.ship_type

	####ship_functionality####
	#return: void ; attack enemy_ship (called by upper-level)
	def attack_ship(self, enemy_ship):
		#enemy ship will get destroyed
		if(self.damage >= enemy_ship.health):
			enemy_ship.delete()
		else:
			#enemy ship takes damage damage
			enemy_ship.take_damage(self.damage)
			#setattr(enemy_ship,"health", enemy_ship.health - self.damage)

	#return: void ; self ship takes damage_amount in damage (called by another ship)
	def take_damage(self, damage_amount):
		setattr(self,"health", self.health - damage_amount)


	####specific ship methods####
	#updates resources collected by a merchant_ship only
	def addResources(self):
		"""
		Enables a ship to harvest resources from a given Hex (does not require maintenance cost to harvest)
		Function not complete - 11/9/22 -> buildingdict must reflect real resources! 
		"""
		player = self.player_controller
		
		#Change buildingDict to reflect natural resources on ocean tiles.
		buildingDict = {'IronMine':['iron',1, 'money',1],'Farm':['food',1,'money',0],'Military':['MilitaryAm',1,'food',1], 'Commercial':['money', 1,'food',1]}
		modify = buildingDict[self.building_type]
		
		#Check if the tile has a merchant ship, and if so, add to player attributes.
		if self.ship_type == "Merchant Ship":
			curr_am = getattr(player, modify[0])
			setattr(player, modify[0], curr_am + modify[1])
			
		player.save()

		return self.name



class Army(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	size = models.IntegerField()
	controller = models.ForeignKey("Player", on_delete=models.CASCADE)
	naval = models.BooleanField()
	location = models.ForeignKey("Hexes", on_delete=models.CASCADE)
	name = models.CharField(max_length=100)
	moved = models.BooleanField(default=False)
	max_movement = models.IntegerField(default=2)

	def __str__(self):
		return self.name

class PolicyGroup(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	player = models.ForeignKey("Player", on_delete=models.CASCADE)
	name = models.CharField(max_length=50, default='none') 

class Policy(models.Model):
	policy_group = models.ForeignKey("PolicyGroup", on_delete=models.CASCADE)
	game = models.ForeignKey("Game", on_delete=models.CASCADE, default="")
	player = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	name = models.CharField(max_length=50, default='none')
	applied = models.BooleanField(default=False)
	SavingsEffect = models.FloatField(default=0)
	ConsumptionEffect = models.FloatField(default=0)
	WelfareEffect = models.FloatField(default=0)
	InequalityEffect = models.FloatField(default=0)
	HealthSpend = models.FloatField(default=0)
	Healthcare = models.IntegerField(default=0)
	ConsumerLoans = models.FloatField(default=0)
	Education = models.FloatField(default=0)
	GovGoods = models.FloatField(default=0)
	WageEffect = models.FloatField(default=0)
	PopEffect = models.FloatField(default=0)

class Pops(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	EducationLevel = models.IntegerField(default=0)
	Income = models.FloatField(default=0)
	Occupation = models.CharField(max_length=50, default='Unemployed')
	Population_size = models.IntegerField(default=0)
	trust = models.IntegerField(default=100)
	Faction = models.ForeignKey("Faction", on_delete=models.CASCADE, default="")

class Faction(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	name = models.CharField(max_length=50, default='NoName')
	controller = models.ForeignKey("Player", on_delete=models.CASCADE, default="")

class PolicySupport(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	Faction = models.ForeignKey("Faction", on_delete=models.CASCADE, default="")
	PolicyAssociated = models.ForeignKey("Policy", on_delete=models.CASCADE, default="")

class MapInterface(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	POLITICAL = 'PO'
	RESOURCES = 'RE'
	MODES = [
	(POLITICAL, 'Political'),
	(RESOURCES, 'Resources'),
	]
	mode = models.CharField(max_length=2,choices=MODES,default=POLITICAL)

class GraphInterface(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	INCOMETAX = 'Income_Tax'
	CORPORATETAX = 'Corporate_Tax'
	WELFARE = 'Welfare'
	EDUCATION = "Education"
	SCIENCE = "Science"
	INFRASTRUCTURE = "Infrastructure"
	MILITARY = "Military"
	MONEY = "MoneyPrintingArr"
	IRON = "Iron"
	WHEAT = "Wheat"
	COAL = 'Coal'
	OIL = 'Oil'
	FOOD = 'Food'
	CONSUMER = 'ConsumerGoods'
	STEEL = 'Steel'
	MACHINERY = 'Machinery'
	MODES = [
	(INCOMETAX, 'Income Tax'),
	(CORPORATETAX, 'Corporate Tax'),
	(WELFARE, 'Welfare'),
	(EDUCATION, 'Education'),
	(SCIENCE, 'Science'),
	(INFRASTRUCTURE, 'Infrastructure Spending'),
	(MILITARY, 'Military Spending'),
	(MONEY, 'Money Printing'),
	(IRON,'Iron Prices'),
	(WHEAT, 'Wheat Prices'),
	(COAL, 'Coal Prices'),
	(OIL, 'Oil Prices'),
	(FOOD, 'Food Prices'),
	(CONSUMER, 'Consumer Goods Prices'),
	(STEEL, 'Steel Prices'),
	(MACHINERY, 'Machinery Prices')
	]
	mode = models.CharField(max_length=20,choices=MODES,default=INCOMETAX)

class GraphCountryInterface(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	controller = models.ForeignKey("Player", on_delete=models.CASCADE, default="")
	country = models.ForeignKey("Country", on_delete=models.CASCADE, default="")
	large = models.BooleanField(default=False)

class Notification(models.Model):
	game = models.ForeignKey("Game", on_delete=models.CASCADE)
	message = models.TextField()
	year = models.IntegerField(default=0)

"""
Here begins the code for Ship Implementations
"""
