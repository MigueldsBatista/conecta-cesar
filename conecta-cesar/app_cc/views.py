from django.shortcuts import render
from .models import Disciplina, Nota

#static



# Create your views here.
def index(request):
    #main pg
    return render(request, 'app_cc/index.html')
""" tudo que está sendo trabalhado dentro dessa função """


#Student Links
def aviso(request):
    return render(request, 'app_cc/avisos.html')


def boletim(request):
    disciplinas_com_notas = []

    disciplinas = Disciplina.objects.all()#codigo que faz o cadastro de notas 

    for disciplina in disciplinas:
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))

    return render(request, 'app_cc/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})


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

def teste(request):
    return render(request, 'app/teste.html')

def perfil(request):
    return render(request, 'app_cc/perfil.html')

def perfil(request):
    return render(request, 'app_cc/diariop.html')

def perfil(request):
    return render(request, 'app_cc/diario.html')
"""Para cada arquivo html é preciso fazer uma def de request do caminho do arquivo para o app"""
