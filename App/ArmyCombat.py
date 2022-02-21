from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes, Notification

class ArmyCombat():
	def __init__(self):
		pass

	def doCombat(self, g):
		army_list = Army.objects.filter(game=g)
		bounce = {}
		deleted = []
		for a in army_list:
			if a in deleted:
				continue
			a.moved = False
			a.save()
			fought = False
			for j in army_list:
				if a.controller.name != j.controller.name and a.location.hexNum == j.location.hexNum:
					self.calculateCombat(g,a,j, deleted)
					fought = True
			if not fought and a.controller != a.location.controller:
				self.switch_hex(a.location, a.controller, g)
		self.doMaintenace(g)

	def doMaintenace(self,g):
		army_list = Army.objects.filter(game=g)
		for a in army_list:
			if a.controller.get_country().Military - a.size*0.1 < 0:
				self.rebel(g,a)
			else:
				g.GameEngine.modify_country_by_name(a.controller.country.name, 'Military', a.controller.get_country().Military - a.size*0.1)
				g.save()

	def rebel(self,g,a):
		a.delete()

	def calculateCombat(self, g, Army1, Army2, deleted):
		diff = abs(Army1.size - Army2.size)
		#Destroy Army if it encounters a naval unit on water.
		arm1_deleted = True
		arm2_deleted = True
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
			Army1.size -= max((int) (Army2.size*0.05), 1)
			Army2.size -= max((int) (Army1.size*0.1), 1)
			self.switch_hex(Army1.location, Army1.controller, g)
			arm2_deleted = self.retreat_army(g, Army2, deleted)
			message2 = "A battle occured in "+Army1.location.name+" with the victory of "+Army1.controller.name+"'s "+Army1.name+" over "+Army2.controller.name+"'s "+Army2.name
			Notification.objects.create(game=g, message=message2)
		elif Army2.size > Army1.size:
			Army1.size -= max((int) (Army2.size*0.1), 1)
			Army2.size -= max((int) (Army1.size*0.05), 1)
			self.switch_hex(Army2.location, Army2.controller, g)
			arm1_deleted = self.retreat_army(g, Army1, deleted)
			message2 = "A battle occured in "+Army2.location.name+" with the victory of "+Army2.controller.name+"'s "+Army2.name+" over "+Army1.controller.name+"'s "+Army1.name
			Notification.objects.create(game=g, message=message2)
		else:
			Army1.size -= max((int) (Army2.size*0.05), 1)
			Army2.size -= max((int) (Army1.size*0.05), 1)
			self.switch_hex(Army1.location, Army1.controller, g)
			message2 = "A battle occured in "+Army1.location.name+" with the victory of "+Army1.controller.name+"'s "+Army1.name+" over "+Army2.controller.name+"'s "+Army2.name
			Notification.objects.create(game=g, message=message2)
			arm2_deleted = self.retreat_army(g, Army2, deleted)
		#import pdb; pdb.set_trace()
		if Army1.size < 0 and arm1_deleted:
			deleted.append(Army1)
			try:
				Army1.delete()
			except:
				print('No Army to delete.')
			Army2.save()
		if Army2.size < 0 and arm2_deleted:
			deleted.append(Army2)
			try:
				Army2.delete()
			except:
				print('No Army to delete.')
			Army1.save()
		if arm1_deleted:
			Army1.save()
		if arm2_deleted:
			Army2.save()

	def retreat_army(self, g, curr_army, deleted):
		h = self.find_retreat_hex(g, curr_army.location, curr_army)
		#import pdb; pdb.set_trace()
		if h == 'null':
			deleted.append(curr_army)
			curr_army.delete()
			return False
		else:
			curr_army.location = h
			curr_army.save()
			return True

	#Calculates distance between two points
	def calculate_distance(self, x1,y1,x2,y2):
	    return abs(self.square(x2-x1) + self.square(y2-y1))

	def find_retreat_hex(self, g, curr_hex, curr_army):
		hex_list = Hexes.objects.filter(game=g, water=curr_army.naval)
		temp = []
		#import pdb; pdb.set_trace()
		for h in hex_list:

			if self.calculate_distance(h.xLocation, h.yLocation, curr_hex.xLocation, curr_hex.yLocation) < 2 and h != curr_army.location and h.controller == curr_army.controller:
				a = Army.objects.filter(game=g, location=h)
				if len(a) < 1:
					return h
				temp.append(h)
		return 'null'

	#Switches control of a hex between two players (doesn't work yet)
	def switch_hex(self, h, player_to, g):
		loser = h.controller
		#import pdb; pdb.set_trace()
		#g.GameEngine.modify_country_by_name(loser.country.name, 'Population', loser.get_country().add_population(loser.get_country().pop_matrix,-h.population*0.8))
		loser.get_country().add_population(loser.get_country().pop_matrix,-h.population*0.8)
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
		g.GameEngine.modify_country_by_name(player_to.country.name, 'capital', player_to.get_country().capital + h.capital*0.7)
		#player_to.get_country().Population += h.population*0.75
		#player_to.get_country().capital += h.capital*0.75
		g.save()
		h.save()
		player_to.save()
		loser.save()

	def square(self, x):
		return x*x