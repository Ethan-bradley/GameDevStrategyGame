from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='app-home'),
    path('account', views.account_info, name='app-account_info'),
    path('dashboard', views.dashboard, name='app-dashboard'),
    path('help', views.help, name='app-help'),
    path('login', views.login, name='app-login'),
] + static(settings.STATIC_URL,document_root = settings.STATIC_ROOT)

