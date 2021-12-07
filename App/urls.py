from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views

urlpatterns = [
    path('', views.home, name='app-home'),
    path('register/', user_views.register, name='register'),
    path('account', user_views.account, name='account'),
    path('dashboard', views.dashboard, name='app-dashboard'),
    path('help', views.help, name='app-help'),
    path('login', views.login, name='app-login'),
    path('new_game', views.new_game, name='app-new_game'),
    path('game/<str:g>/<str:player>/', views.game, name='app-game'),
    path('joinGame/<str:g>/', views.joinGame, name='joinGame'),
    path('lobby', views.lobby, name='app-lobby'),
    path('map/<str:g>/<str:p>/<str:l>/<str:lprev>', views.map, name='map'),
    path('map/<str:g>/<str:p>', views.map, name='app-map'),
    path('graphs/<str:g>/<str:p>', views.graph, name='app-graph'),
    path('gamegraphs/<str:g>/<str:p>', views.gamegraph, name='app-game-graph'),
    path('policies/<str:g>/<str:p>', views.policies, name='app-policies'),
    path('trade/<str:g>/<str:p>', views.trade, name='app-trade'),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)