from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as django_login
from rolepermissions.checkers import has_role
from project_cc.roles import Aluno, Professor
from app_cc.models import Aluno as AlunoModel, Professor as ProfessorModel
from django.contrib import messages
from rolepermissions.roles import assign_role
from django.utils.translation import gettext as _





# Cadastro de novo usuário
def cadastro(request):
    """
    View function for user registration.

    This function handles both GET and POST requests.
    In case of a GET request, it renders the 'cadastro.html' template.
    In case of a POST request, it creates a new user and assigns a role
    based on the selected user type.
    """

    # The only way for the request to be a GET is if the user tries to access the registration page directly by typing the URL in the browser.
    # In this case, we simply render the registration form.
    if request.method == 'GET':
        return render(request, 'cadastro.html')

    else:
        # Get form data
        user_name = request.POST.get('username')
        user_email = request.POST.get('email')
        senha = request.POST.get('senha')
        user_type = request.POST.get('user_type')

        # Check if a user with the same name already exists
        if User.objects.filter(username=user_name).exists():
            messages.error(request, _("Já existe um usuário com esse nome"))
            return redirect("cadastro")  # Redirect to the same page

        # Create a new user
        user = User.objects.create_user(username=user_name, email=user_email, password=senha)

        # Assign a role based on the selected user type
        if user_type == 'professor':
            assign_role(user, Professor)
            ProfessorModel.objects.create(usuario=user,  email=user_email)
        elif user_type == 'aluno':
            assign_role(user, Aluno)
            AlunoModel.objects.create(usuario=user,  email=user_email)
        else:
            messages.error(request, _("Papel do usuário não especificado. Selecione 'professor' ou 'aluno'."))
            return redirect("cadastro")

        # Success message
        messages.success(request, _("Usuário cadastrado com sucesso. Agora faça login."))
        return redirect("login")  # Redirect to the login page

def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        user_name = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=user_name, password=senha)
        if user:
            # A função django-login é necessária para que o usuário seja considerado logado no sistema.
            # A biblioteca Django mantém o estado do usuário logado usando um cookie.
            # A função django-login cria e atualiza esse cookie para que o usuário seja considerado logado.
            django_login(request, user)
            
            if has_role(user, Professor):
                return redirect("avisosp")  # URL da página do professor
            
            elif has_role(user, Aluno):
                return redirect("avisos")  # URL da página do aluno
            else:
                messages.error(request, _("O usuário não tem um papel definido."))
                return redirect("login")  # Volta para a página de login
        else:
            messages.error(request, _("Usuário ou senha incorretos. Por favor, tente novamente."))
            return redirect("login")  # Redireciona para a página de login

def plataforma(request):
    if request.user.is_authenticated:  
        if has_role(request.user, Professor):
            return redirect("avisosp")  # Redireciona para a página do professor
        elif has_role(request.user, Aluno):
            return redirect("avisos")  # Redireciona para a página do aluno
    return HttpResponse(_('Você precisa estar logado'))
