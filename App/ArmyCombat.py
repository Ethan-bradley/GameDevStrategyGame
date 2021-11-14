from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes

class ArmyCombat():
	def __init__(self):
		pass

	def doCombat(self, g):
		army_list = Army.objects.filter(game=g)
		bounce = {}
		for a in army_list:
			fought = False
			for j in army_list:
				if a.controller.name != j.controller.name and a.location.hexNum == j.location.hexNum:
					self.calculateCombat(g,a,j)
					fought = True
			if not fought:
				self.switch_hex(a.location, a.controller)


	def calculateCombat(self, g, Army1, Army2):
		diff = abs(Army1.size - Army2.size)
		#Destroy Army if it encounters a naval unit on water.
		if Army1.location.water:
			if Army1.naval and not Army2.naval:
				Army2.delete()
				Army1.save()
				return
			if Army2.naval and not Army1.naval:
				Army1.delete()
				Army2.save()
				return
		if Army1.size > Army2.size:
			Army1.size -= min(diff/3, Army1.size)
			Army2.size -= min(diff/2, Army2.size)
			self.switch_hex(Army1.location, Army1.controller)
			self.retreat_army(g, Army2)
		elif Army2.size > Army1.size:
			Army1.size -= min(diff/2, Army2.size)
			Army2.size -= min(diff/3, Army1.size)
			self.switch_hex(Army2.location, Army2.controller)
			self.retreat_army(g, Army1)
		else:
			Army1.size -= min(diff/2, Army2.size)
			Army2.size -= min(diff/2, Army1.size)
			self.switch_hex(Army1.location, Army1.controller)
			self.retreat_army(g, Army2)

		if Army1.size < 0:
			Army1.delete()
			Army2.save()
		elif Army2.size < 0:
			Army2.delete()
			Army1.save()
		else:
			Army1.save()
			Army2.save()

	def retreat_army(self, g, curr_army):
		h = self.find_retreat_hex(g, curr_army.location, curr_army)
		if h == 'null':
			curr_army.delete()
		else:
			curr_army.location = h
			curr_army.save()

	#Calculates distance between two points
	def calculate_distance(self, x1,y1,x2,y2):
	    return abs(self.square(x2-x1) + self.square(y2-y1))

	def find_retreat_hex(self, g, curr_hex, curr_army):
		hex_list = Hexes.objects.filter(game=g, water=curr_army.naval)
		temp = []
		for h in hex_list:
			if self.calculate_distance(h.xLocation, h.yLocation, curr_hex.xLocation, curr_hex.yLocation) < 2:
				a = Army.objects.filter(game=g, location=h)
				if len(a) < 1:
					return h
				temp.append(h)
		return 'null'

	#Switches control of a hex between two players (doesn't work yet)
	def switch_hex(self, h, player_to):
		loser = h.controller
		loser.get_country().Population -= h.population
		loser.get_country().capital -= h.capital
		h.controller = player_to
		h.color = player_to.color
		player_to.get_country().Population += h.population
		player_to.get_country().capital += h.capital
		
		h.save()
		player_to.save()

	def square(self, x):
		return x*x