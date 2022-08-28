from .models import Game, Player, IndTariff, Tariff, Army, Policy, PolicyGroup, Hexes, Notification, Building

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
		for j in army_list:
			if j.size < 0:
				try:
					j.delete()
				except:
					print("No army to delete!")
		self.doMaintenace(g)

	def doMaintenace(self,g):
		army_list = Army.objects.filter(game=g)
		for a in army_list:
			if a.controller.MilitaryAm - a.size*0.5 < 0:
				self.rebel(g,a)
			else:
				a.controller.MilitaryAm -= a.size*0.5
				g.save()

	def rebel(self,g,a):
		try:
			a.delete()
		except:
			print("Army deletion error.")

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
		defense_bonus = 2
		army1_fortification = 1
		army2_fortification = 1
		if not Army1.moved:
			army1_fortification = 2
		if not Army2.moved:
			army2_fortification = 2
		Army1combat = Army1.size*army1_fortification
		Army2combat = Army2.size*army2_fortification
		turn = g.GameEngine.get_country_by_name("UK").time - 17
		if Army1combat > Army2combat:
			message2 = "A battle occured in " + Army1.location.name + " with the victory of " + Army1.controller.name + "'s " + Army1.name + " of size " + str(
				Army1.size) + " with casualties of " + str(max((int)(Army2.size * 0.05),
								 1)) + " over " + Army2.controller.name + "'s " + Army2.name + " of size " + str(Army2.size) + " with casulties of " + str(max((int)(Army1.size * 0.1), 1))
			Army1.size -= max((int) (Army2.size*0.05), 1)
			Army2.size -= max((int) (Army1.size*0.1), 1)
			self.switch_hex(Army1.location, Army1.controller, g)
			arm2_deleted = self.retreat_army(g, Army2, deleted)
			Notification.objects.create(game=g, message=message2, year=turn)
		elif Army2combat > Army1combat:
			message2 = "A battle occured in " + Army2.location.name + " with the victory of " + Army2.controller.name + "'s " + Army2.name + " of size " + str(
				Army2.size) + " with casualties of " + \
					   str(max((int)(Army1.size * 0.05), 1)) + " over " + Army1.controller.name + "'s " + Army1.name
			" of size " + str(Army1.size) + " with casualties of " + str(max((int)(Army2.size * 0.1), 1))
			Army1.size -= max((int) (Army2.size*0.1), 1)
			Army2.size -= max((int) (Army1.size*0.05), 1)
			self.switch_hex(Army2.location, Army2.controller, g)
			arm1_deleted = self.retreat_army(g, Army1, deleted)
			Notification.objects.create(game=g, message=message2, year=turn)
		else:
			Army1.size -= max((int) (Army2.size*0.05), 1)
			Army2.size -= max((int) (Army1.size*0.05), 1)
			self.switch_hex(Army1.location, Army1.controller, g)
			message2 = "A battle occured in "+Army1.location.name+" with the victory of "+Army1.controller.name+"'s "+Army1.name+" over "+Army2.controller.name+"'s "+Army2.name
			Notification.objects.create(game=g, message=message2, year=turn)
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
			try:
				curr_army.delete()
			except:
				print("No army to delete.")
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

	#Switches control of a hex between two players
	def switch_hex(self, h, player_to, g):
		loser = h.controller
		h.controller = player_to
		h.color = player_to.country.color
		buildings = Building.objects.filter(game=g, location=h)
		for building in buildings:
			building.player_controller = player_to
			building.save()
		h.save()
		player_to.save()
		loser.save()

	def square(self, x):
		return x*x