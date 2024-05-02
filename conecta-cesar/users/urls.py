from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),  # Página de login
    path('cadastro/', views.cadastro, name='cadastro'),  # Página de cadastro
    path('plataforma/', views.plataforma, name='plataforma'),  # Plataforma
]