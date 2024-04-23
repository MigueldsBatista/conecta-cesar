from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from rolepermissions.roles import assign_role
from rolepermissions.checkers import has_role
from project_cc.roles import Aluno, Professor
from django.contrib import messages

  # Importando a função login do Django para evitar conflito

def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user_type = request.POST.get('user_type')

        # Verifica se já existe um usuário com esse nome
        if User.objects.filter(username=username).exists():
            messages.error(request, "Já existe um usuário com esse nome")
            return redirect("cadastro")  # Redireciona para a mesma página

        # Se não existe, cria o usuário
        user = User.objects.create_user(username=username, email=email, password=senha)

        if user_type == 'professor':
            assign_role(user, Professor)
        elif user_type == 'aluno':
            assign_role(user, Aluno)
        else:
            messages.error(request, "Papel do usuário não especificado. Selecione 'professor' ou 'aluno'.")
            return redirect("cadastro")

        # Mensagem de sucesso
        messages.success(request, "Usuário cadastrado com sucesso. Agora faça login.")
        return redirect("login")  # Redireciona para a página de login


# View para o login
def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')  # Capturando username
        senha = request.POST.get('senha')  # Capturando senha
        
        user = authenticate(username=username, password=senha)
        if user:
            django_login(request, user)
        
            if has_role(user, Professor):
                return render(request, "app_cc/professor/avisosp.html")  # URL da página do professor
            
            elif has_role(user, Aluno):
                return redirect("app_cc/aluno/avisos.html")  # URL da página do aluno
            else:
                messages.error(request, "O usuário não tem um papel definido.")
                return redirect("login")  # Volta para a página de login
        else:
            messages.error(request, "Usuário ou senha incorretos. Por favor, tente novamente.")
            return redirect("login")  # Redireciona para a página de login
def plataforma(request):
    if request.user.is_authenticated:  # Corrigido erro de digitação
        return request('content.html')
    return HttpResponse('Você precisa estar logado')