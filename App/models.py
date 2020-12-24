from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from collections import OrderedDict

class Post(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return self.title

class Game(models.Model):
	name = models.CharField(max_length=100)
	host = models.ForeignKey(User, on_delete=models.CASCADE)
	#num_players = models.IntegerField(default=0)
	#players = ManyToManyField("Player")
	#hexes = ManyToManyField("Hexes")

class Player(models.Model):
	name = models.CharField(max_length=100)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	host = models.BooleanField()
	#game = models.OneToOneField("Game", on_delete=models.CASCADE)


class Tariff(models.Model):
	curr_player = models.OneToOneField("Player", on_delete=models.CASCADE, default="")
	name = models.CharField(max_length=100)
	#players = models.ManyToManyField("Player")
	#for i in range(0,4):
	#	i = models.DecimalField(max_digits=70, decimal_places=50)
	#for i in range(0,players.count):
	#	i = models.DecimalField(max_digits=70, decimal_places=50)
	#tariffs = models.ManyToManyField("Player")
	#t = OrderedDict()
	#for p in players.values():
	#		t[p] =  models.DecimalField(max_digits=70, decimal_places=50)
class IndTariff(models.Model):
	controller = models.ForeignKey(Tariff, db_index=True, on_delete=models.CASCADE)
	#key = models.CharField(max_length=100)
	key = models.OneToOneField("Player", on_delete=models.CASCADE)
	tariffAm = models.DecimalField(max_digits=70, decimal_places=50)

class Hexes(models.Model):
	hexNum = models.IntegerField()

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
