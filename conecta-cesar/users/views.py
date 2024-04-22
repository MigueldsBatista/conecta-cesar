from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login  # Importando a função login do Django para evitar conflito

# Create your views here.

def index(request):
    return render(request, 'index.html')

def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Verifica se já existe um usuário com esse nome
        user_exists = User.objects.filter(username=username).exists()
        
        if user_exists:
            return HttpResponse("Já existe um usuário com esse nome")
        
        # Se não existe, cria o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()
        
        return HttpResponse("Usuário cadastrado com sucesso")

def login(request):  # Renomeado para evitar conflito
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)
        if user:
            django_login(request, user)  # Use o método 'login' do Django
            
            return render(request, 'app_cc/avisos.html')
        else:
            return HttpResponse('Usuário ou senha inválidos')

def plataforma(request):
    if request.user.is_authenticated:  # Corrigido erro de digitação
        return request('content.html')
    return HttpResponse('Você precisa estar logado')
