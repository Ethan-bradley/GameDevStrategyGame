from .models import Hexes, Country

class HexList():
	def __init__(self):
		self.hexList = []
		first_row = [['Atlantic Ocean',True,0,'#3262a8','Spain',False,0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','Spain',False,0,0,0,0],['Portugal',False,100,'#d2d6d5','Neutral', False,0,1,0,0],['Andalusia',False,50,'#e8cf10','Spain', False,1,0,0,0],['South Baleric Sea',True,0,'#3262a8','Spain', False,0,0,0,0],['Rome', False, 100,'#15ad31','Italy', True,0,0,0,1],['Central Adriatic',True,0,'#3262a8','Italy',False,0,0,0,0]]
		second_row = [['Atlantic Ocean',True,0,'#3262a8','Spain', False, 0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','Spain', False, 0,0,0,0],['Castille',False,50,'#e8cf10','Spain', False,1,0,0,0],['Madrid',False,100,'#e8cf10','Spain', True,0,1,0,0],['North Baleric Sea',True,0,'#3262a8','France', False,0,0,0,0],['Lombardy', False, 50,'#15ad31','Italy', False,0,1,0,0]]
		third_row = [['Atlantic Ocean',True,0,'#3262a8','UK', False,0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','UK', False,0,0,0,0],['Bay of Biscay',True,0,'#3262a8','France', False,0,0,0,0],['Bordeaux',False,50,'#ad3315','France', False,0,1,0,0],['Lyon',False,50,'#ad3315','France', False,1,0,0,0],['Switzerland', False, 50,'#d2d6d5','Neutral', False,0,0,0,1], ['Austria', False, 50,'#d2d6d5','Neutral', False,0,0,0,0]]
		fourth_row = [['Atlantic Ocean',True,0,'#3262a8','UK', False,0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','UK', False,0,0,0,0],['Brest',False,30,'#ad3315','France', False,0,1,0,0],['Paris',False,100,'#ad3315','France', True,0,1,0,0],['Alsace Lorraine',False,70,'#ad3315','France', False,2,0,0,0],['Bavaria', False, 70,'#808080','Germany', False,0,1,0,0]]
		fifth_row = [['Cornwall',False,100,'#fc2403','UK', True,0,0,0,1],['London',False,100,'#fc2403','UK', True,0,0,0,1],['North Sea',True,0,'#3262a8','UK', False,0,0,0,0],['Belgium',False,50,'#d2d6d5','Neutral', False,1,0,0,0],['Ruhr',False,100,'#808080','Germany', True,0,0,2,0],['Hanover', False, 50,'#808080','Germany', False,0,0,1,0], ['Saxony', False, 50,'#808080','Germany', False,0,0,0,0]]
		sixth_row = [['Wales',False,100,'#fc2403','UK', True,0,0,1,0],['Midlands',False,100,'#fc2403','UK', True,0,0,1,0],['North Sea',True,0,'#3262a8','UK', False,0,0,0,0],['North Sea',True,50,'#3262a8','UK', False,1,0,0,0],['Netherlands',False,100,'#d2d6d5','Neutral', True,0,1,0,0],['Hamburg', False, 50,'#808080','Germany', False,0,1,0,0]]
		self.hexList.append(first_row)
		self.hexList.append(second_row)
		self.hexList.append(third_row)
		self.hexList.append(fourth_row)
		self.hexList.append(fifth_row)
		self.hexList.append(sixth_row)

	def apply(self, g, p):
		y = 0
		total = len(self.hexList)
		for i in self.hexList:
			x = 0
			for j in i:
				start = Country.objects.filter(name=j[4])[0]
				temp = Hexes(hexNum=total*y+x ,game=g, controller=p, color=j[3], name=j[0], water=j[1], xLocation=x, yLocation=y, population=j[2], start_country=start, center=j[5], iron=j[6], wheat=j[7], coal=j[8], oil=j[9])
				temp.save()
				x += 1
			y += 1