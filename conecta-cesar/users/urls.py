from django.urls import path
from . import views


urlpatterns=[
    path('', views.login),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.login, name='login'),
    path('plataforma', views.plataforma, name="plataforma"),
]