from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from project_cc.roles import Aluno, Professor
  # Importando a função login do Django para evitar conflito

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
        user_type = request.POST.get('user_type')

        # Verifica se já existe um usuário com esse nome
        user_exists = User.objects.filter(username=username).exists()
        
        if user_exists:
            return HttpResponse("Já existe um usuário com esse nome")
        
        # Se não existe, cria o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)

        user.save()
        if user_type=='professor':
            assign_role(user, Professor)
            return HttpResponse("Professor cadastrado com sucesso")
        
        elif user_type=='aluno':
            assign_role(user, Aluno)
            return HttpResponse("Aluno cadastrado com sucesso")
        
        else:
            return HttpResponse("Papel do usuário não especificado. Selecione 'professor' ou 'aluno'.")
    # Retornos apropriados conforme a seleção do campo
       
            
        
      


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')  # Capturando username
        senha = request.POST.get('senha')  # Capturando senha

        user = authenticate(username=username, password=senha)
        if user:
            django_login(request, user)
        
            user = request.user  # Obter o usuário autenticado
            if has_role(user, Professor):
                return render(request, 'app_cc/professor/avisosp.html')
            
            elif has_role(user, Aluno):
                return render(request, 'app_cc/aluno/avisos.html')
            else:
                return HttpResponse("O usuário não tem um papel definido")
        else:
            return HttpResponse('Usuário ou senha inválidos')
        
def plataforma(request):
    if request.user.is_authenticated:  # Corrigido erro de digitação
        return request('content.html')
    return HttpResponse('Você precisa estar logado')
