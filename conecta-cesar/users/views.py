from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from rolepermissions.checkers import has_role
from project_cc.roles import Aluno, Professor
from app_cc.models import Aluno as AlunoModel, Professor as ProfessorModel
from django.contrib import messages
from rolepermissions.roles import assign_role




def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    else:
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        senha = request.POST.get('senha')
        user_type = request.POST.get('user_type')

        # Verifica se já existe um usuário com esse nome
        if User.objects.filter(username=user_name).exists():
            messages.error(request, "Já existe um usuário com esse nome")
            return redirect("cadastro")  # Redireciona para a mesma página

        # Se não existe, cria o usuário
        user = User.objects.create_user(username=user_name, email=user_email, password=senha)

        if user_type == 'professor':
            assign_role(user, Professor)
            ProfessorModel.objects.create(usuario=user,  email=user_email)
        elif user_type == 'aluno':
            assign_role(user, Aluno)
            AlunoModel.objects.create(usuario=user,  email=user_email)
        else:
            messages.error(request, "Papel do usuário não especificado. Selecione 'professor' ou 'aluno'.")
            return redirect("cadastro")

        # Mensagem de sucesso
        messages.success(request, "Usuário cadastrado com sucesso. Agora faça login.")
        return redirect("login")  # Redireciona para a página de login

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_name = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=user_name, password=senha)
        if user:
            django_login(request, user)
        
            if has_role(user, Professor):
                return redirect("avisosp")  # URL da página do professor
            
            elif has_role(user, Aluno):
                return redirect("avisos")  # URL da página do aluno
            else:
                messages.error(request, "O usuário não tem um papel definido.")
                return redirect("login")  # Volta para a página de login
        else:
            messages.error(request, "Usuário ou senha incorretos. Por favor, tente novamente.")
            return redirect("login")  # Redireciona para a página de login

def plataforma(request):
    if request.user.is_authenticated:  
        if has_role(request.user, Professor):
            return redirect("avisosp")  # Redireciona para a página do professor
        elif has_role(request.user, Aluno):
            return redirect("avisos")  # Redireciona para a página do aluno
    return HttpResponse('Você precisa estar logado')
