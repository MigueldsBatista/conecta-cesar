from django.shortcuts import render
from django.utils import translation
from .models import Disciplina, Nota
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Diario
from datetime import date
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm
from django.contrib import messages
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')  # Redirecionar para a página de login após o registro
    else:
        form = CustomUserCreationForm()
    return render(request, 'app_cc/register.html', {'form': form})


#Login 
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import CustomAuthenticationForm
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('avisos')  # Redirecionar para 'avisos' após o login
            else:
                # Adiciona uma mensagem de erro para ser exibida no template
                messages.error(request, 'Usuário ou senha incorretos.', extra_tags='alert-danger')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'app_cc/index.html', {'form': form})

    

#------------------------------------------------------------------------------------------------------------


#Student Links
def avisos(request):
    return render(request, 'app_cc/avisos.html')

def boletim(request):
    # Recuperar todas as disciplinas
    disciplinas = Disciplina.objects.all()

    # Lista para armazenar disciplinas com suas notas
    disciplinas_com_notas = []

    # Iterar sobre todas as disciplinas
    for disciplina in disciplinas:
        # Verificar se há uma nota associada a esta disciplina
        try:
            nota_instance = Nota.objects.get(disciplina=disciplina)
        except Nota.DoesNotExist:
            nota_instance = None

        # Adicionar a disciplina à lista, juntamente com sua nota (ou None, se não houver nota)
        disciplinas_com_notas.append((disciplina, nota_instance))

    return render(request, 'app_cc/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})


def boletimp(request):
    if request.method == "POST":
        for disciplina in Disciplina.objects.all():
            nota_value = request.POST.get(f"notas[{disciplina.disciplina}]")
            if nota_value is not None:
                nota_value = nota_value.replace(',', '.')
                try:
                    nota_value = float(nota_value)
                except ValueError:
                    return HttpResponse("Erro: Valor da nota inválido")

                nota_instance, created = Nota.objects.get_or_create(disciplina=disciplina)
                nota_instance.nota = nota_value
                nota_instance.save()

    disciplinas_com_notas = []
    for disciplina in Disciplina.objects.all():
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))

    return render(request, 'app_cc/boletimp.html', {'disciplinas_com_notas': disciplinas_com_notas})

def diariop(request):
    if request.method == 'POST':
        disciplina = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')
        
        # Salvar o diário no banco de dados
        Diario.objects.create(disciplina=disciplina, titulo=titulo, texto=texto)

        # Redirecionar para a mesma página para exibir os diários atualizados
        return redirect('diariop')
    else:
        # Obter todos os diários salvos
        diarios = Diario.objects.all()
        return render(request, 'app_cc/diariop.html', {'diarios': diarios})

def diario(request):
    # Obtém todos os diários salvos
    diarios = Diario.objects.all()
    # Renderiza o template 'app_cc/diario.html' passando os diários para o contexto
    return render(request, 'app_cc/diario.html', {'diarios': diarios})


def frequencia(request):
    return render(request, 'app_cc/frequencia.html')


#Professor Links
def turmas(request):
    return render(request, 'app_cc/turmas.html')

def perfilp(request):
    return render(request, 'app_cc/perfilp.html')

def frequenciap(request):
    return render(request, 'app_cc/frequenciap.html')

def calendariop(request):
    return render(request, 'app_cc/calendariop.html')

def avisosp(request):
    return render(request, 'app_cc/avisosp.html')

def frequenciap(request):
    return render(request, 'app_cc/frequenciap.html')

def disciplinas_e_notas(request):
    disciplinas_com_notas = []

    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))

    return render(request, 'app_cc/disciplina.html', {'disciplinas_com_notas': disciplinas_com_notas})

def perfil(request):
    return render(request, 'app_cc/perfil.html')


