from django.contrib import admin
from .models import Post
from .models import Player
from .models import Tariff
from .models import Hexes
from .models import Economic
from .models import Game, IndTariff, Army, Country, Policy, PolicyGroup, PlayerProduct, Product, MapInterface, GraphInterface, Notification, GraphCountryInterface

admin.site.register(Post)
admin.site.register(Player)
admin.site.register(Tariff)
admin.site.register(Hexes)
admin.site.register(Economic)
admin.site.register(Game)
admin.site.register(IndTariff)
admin.site.register(Army)
admin.site.register(Country)
admin.site.register(PolicyGroup)
admin.site.register(Policy)
admin.site.register(PlayerProduct)
admin.site.register(Product)
admin.site.register(MapInterface)
admin.site.register(GraphInterface)
admin.site.register(Notification)
admin.site.register(GraphCountryInterface)
# Register your models here.
