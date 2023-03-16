from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('home/',views.home,name='home'),
    path('',views.home,name='home'),
    path('login_user/',views.login_user,name='login_user'),
    path('signup/',views.signup,name='signup'),
    path('signout/',views.signout,name='signout'),
    path('dashboard/',views.dashboard,name='dashboard'),
    path('chart/',views.chart,name='chart'),
] + static(settings.STATIC_URL,document_root=settings.STATIC_ROOT) # Configuração para servir arquivos de mídia
