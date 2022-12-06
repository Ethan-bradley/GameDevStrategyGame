from .models import Hexes, Country

class HexList():
	def __init__(self):
		self.hexList = []
		first_row = [['Caribbean Sea',True,0,'#3262a8','Neutral',False,0,0,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral',False,0,0,0,0],['Caribbean Sea',False,100,'#3262a8','Neutral', False,0,1,0,0],['Caribbean Sea',True,50,'#3262a8','Neutral', False,1,0,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral',False,0,0,0,0], ['Barbados', False, 100,'#fc2403','UK', True,0,0,0,2]]
		second_row = [['Cayman',False,0,'#e8cf10','Spain', False, 0,1,1,0],['Caribbean Sea',True,0,'#3262a8','Neutral', False, 0,0,0,0],['Caribbean Sea',False,50,'#3262a8','Neutral', False,2,0,0,0],['Caribbean Sea',False,100,'#3262a8','Neutral', True,0,2,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Caribbean Sea', True, 50,'#3262a8','Neutral', False,2,0,0,0], ['Caribbean Sea', True, 50,'#3262a8','Neutral', False,0,0,0,1]]
		third_row = [['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Jamaica',False,0,'#d2d6d5','Neutral', False,0,0,0,0],['Caribbean Sea',True,50,'#3262a8','Neutral', False,0,1,0,0],['Caribbean Sea',True,50,'#3262a8','Neutral', False,1,0,0,0],['Caribbean Sea', True, 50,'#3262a8','Neutral', False,0,0,0,0], ['Puerto Rico', False, 50,'#d2d6d5','Neutral', False,1,1,0,0]]
		fourth_row = [['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Caribbean Sea',True,30,'#3262a8','Neutral', False,0,1,0,0],['Caribbean Sea',True,100,'#3262a8','Neutral', True,0,1,0,0],['Caribbean Sea',True,70,'#3262a8','Neutral', False,2,0,0,0],['Caribbean Sea', True, 70,'#3262a8','Neutral', False,0,1,0,0], ['Atlantic Ocean', True, 50,'#3262a8','Germany', False,1,0,1,0]]
		fifth_row = [['Caribbean Sea',True,0,'#3262a8','Neutral', False,0,0,0,0],['Cuba',False,0,'#d2d6d5','Neutral', False,0,1,1,0],['Cuba',False,30,'#d2d6d5','Neutral', False,1,1,0,0],['Caribbean Sea',True,100,'#3262a8','Neutral', True,0,1,0,0],['Haiti',False,70,'#d2d6d5','Neutral', False,2,1,0,0],['Dominican Republic', False, 70,'#d2d6d5','Neutral', False,0,1,2,0], ['Atlantic Ocean', True, 50,'#3262a8','Neutral', False,0,0,1,0]]
		sixth_row = [['Atlantic Ocean',True,0,'#3262a8','Neutral', False,0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','Neutral', False,0,0,0,0],['Atlantic Ocean',True,30,'#3262a8','Neutral', False,0,1,0,0],['Atlantic Ocean',True,100,'#3262a8','Neutral', True,0,1,0,0],['Atlantic Ocean',True,70,'#3262a8','Neutral', False,2,0,0,0],['Atlantic Ocean', True, 70,'#3262a8','Neutral', False,0,1,0,0], ['Atlantic Ocean', True, 50,'#3262a8','Neutral', False,0,0,0,0]]
		seventh_row = [['Atlantic Ocean',True,0,'#3262a8','Neutral', False,0,0,0,0],['Atlantic Ocean',True,0,'#3262a8','Neutral', False,0,0,0,0],['Bahamas',False,30,'#ad3315','France', False,0,1,0,1],['Atlantic Ocean',True,100,'#3262a8','Neutral', True,0,1,0,0],['Atlantic Ocean',True,70,'#3262a8','Neutral', False,2,0,0,0],['Atlantic Ocean', True, 70,'#3262a8','Neutral', False,0,1,0,0], ['Bermuda', False, 50,'#15ad31','Italy', False,0,1,1,0]]
		self.hexList.append(first_row)
		self.hexList.append(second_row)
		self.hexList.append(third_row)
		self.hexList.append(fourth_row)
		self.hexList.append(fifth_row)
		self.hexList.append(sixth_row)
		self.hexList.append(seventh_row)

	def apply(self, g, p):
		y = 0
		total = len(self.hexList)
		for i in self.hexList:
			x = 0
			for j in i:
				start = Country.objects.filter(name=j[4])[0]
				temp = Hexes(hexNum=total*y+x ,game=g, controller=p, color=j[3], name=j[0], water=j[1], xLocation=x, yLocation=y, population=j[2], start_country=start, center=j[5], metal=j[6], food=j[7], wood=j[8], gold=j[9])
				temp.save()
				x += 1
			y += 1