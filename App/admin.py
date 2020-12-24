from django.contrib import admin
from .models import Post
from .models import Player
from .models import Tariff
from .models import Hexes
from .models import Economic
from .models import Game

admin.site.register(Post)
admin.site.register(Player)
admin.site.register(Tariff)
admin.site.register(Hexes)
admin.site.register(Economic)
admin.site.register(Game)

# Register your models here.
