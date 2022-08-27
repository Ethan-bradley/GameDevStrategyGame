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
    path('policies/<str:g>/<str:p>', views.policies, name='app-policies'),
    path('trade/<str:g>/<str:p>', views.trade, name='app-trade'),
    path('runNext/<str:g>', views.runNext, name='app-run-next'),
    path('runNext2/<str:g>', views.runNext2, name='app-run-next-2'),
    path('runNext3/<str:g>', views.runNext3, name='app-run-next-3'),
    path('delete/<str:g>/<str:p>', views.delete, name='app-delete'),
    path('runArmy/<str:g>', views.runArmy, name='app-run-army'),
    path('fixVars/<str:g>', views.fixVars, name='app-run-fix-vars'),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

# For Django >= 2.0

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)