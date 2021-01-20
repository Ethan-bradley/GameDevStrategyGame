from .models import Hexes, Country

class HexList():
	def __init__(self):
		self.hexList = []
		first_row = [['Atlantic Ocean',True,0,'#3262a8','Spain',False],['Portugal',False,100,'#e8cf10','Spain', False],['Andalusia',False,50,'#e8cf10','Spain', False],['South Baleric Sea',True,0,'#3262a8','Spain', False],['Rome', False, 100,'#15ad31','Italy', True]]
		second_row = [['Atlantic Ocean',True,0,'#3262a8','Spain', False],['Castille',False,50,'#e8cf10','Spain', False],['Madrid',False,100,'#e8cf10','Spain', True],['North Baleric Sea',True,0,'#3262a8','France', False],['Lombardy', False, 50,'#15ad31','Italy', False]]
		third_row = [['Atlantic Ocean',True,0,'#3262a8','UK', False],['Bay of Biscay',True,0,'#3262a8','France', False],['Bordeaux',False,50,'#ad3315','France', False],['Lyon',False,50,'#ad3315','France', False],['Switzerland', False, 50,'#15ad31','Italy', False]]
		fourth_row = [['Atlantic Ocean',True,0,'#3262a8','UK', False],['Brest',False,30,'#ad3315','France', False],['Paris',False,100,'#ad3315','France', True],['Alsace Lorraine',False,70,'#ad3315','France', False],['Bavaria', False, 70,'#ad3315','Germany', False]]
		fifth_row = [['London',False,100,'#fc2403','UK', True],['North Sea',True,0,'#3262a8','UK', False],['Belgium',False,50,'#ad3315','Germany', False],['Ruhr',False,100,'#ad3315','Germany', True],['Hanover', False, 50,'#ad3315','Germany', False]]
		self.hexList.append(first_row)
		self.hexList.append(second_row)
		self.hexList.append(third_row)
		self.hexList.append(fourth_row)
		self.hexList.append(fifth_row)

	def apply(self, g, p):
		y = 0
		total = len(self.hexList)
		for i in self.hexList:
			x = 0
			for j in i:
				start = Country.objects.filter(name=j[4])[0]
				temp = Hexes(hexNum=total*y+x ,game=g, controller=p, color=j[3], name=j[0], water=j[1], xLocation=x, yLocation=y, population=j[2], start_country=start, center=j[5])
				temp.save()
				x += 1
			y += 1