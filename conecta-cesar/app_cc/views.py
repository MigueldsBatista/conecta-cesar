from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.contrib import messages
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from .models import Disciplina, Nota, Diario

# Register
 

# Student Links
def avisos(request):
    return render(request, 'app_cc/avisos.html')
#----------------------------------------------------------------------------------------------------------------    


def avisosp(request):
    
    return render(request, 'app_cc/avisosp.html')
#----------------------------------------------------------------------------------------------------------------    

def boletim(request):
    disciplinas = Disciplina.objects.all()
    disciplinas_com_notas = []
    for disciplina in disciplinas:
        try:
            nota_instance = Nota.objects.get(disciplina=disciplina)
        except Nota.DoesNotExist:
            nota_instance = None
        disciplinas_com_notas.append((disciplina, nota_instance))
    return render(request, 'app_cc/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})
#----------------------------------------------------------------------------------------------------------------    

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
#----------------------------------------------------------------------------------------------------------------    

def diariop(request):
    if request.method == 'POST':
        disciplina = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')
        Diario.objects.create(disciplina=disciplina, titulo=titulo, texto=texto)
        return redirect('diariop')
    else:
        diarios = Diario.objects.all()
        return render(request, 'app_cc/diariop.html', {'diarios': diarios})
#----------------------------------------------------------------------------------------------------------------    

def frequencia(request):
    return render(request, 'app_cc/frequencia.html')
#----------------------------------------------------------------------------------------------------------------    

def perfil(request):
    return render(request, 'app_cc/perfil.html')
def diario(request):
    # Obtém todos os diários salvos
    diarios = Diario.objects.all()
    # Renderiza o template 'app_cc/diario.html' passando os diários para o contexto
    return render(request, 'app_cc/diario.html', {'diarios': diarios})

#----------------------------------------------------------------------------------------------------------------  
#----------------------------------------PROFESSOR VIEWS---------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------    


def turmas(request):
    return render(request, 'app_cc/turmas.html')

def perfilp(request):
    return render(request, 'app_cc/perfilp.html')

def frequenciap(request):
    return render(request, 'app_cc/frequenciap.html')

def calendariop(request):
    return render(request, 'app_cc/calendariop.html')



def disciplinas_e_notas(request):
    disciplinas_com_notas = []
    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))
    return render(request, 'app_cc/disciplina.html', {'disciplinas_com_notas': disciplinas_com_notas})



