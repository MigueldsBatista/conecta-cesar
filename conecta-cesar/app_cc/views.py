from django.shortcuts import render
from django.utils import translation
from .models import Disciplina, Nota
from django.http import HttpResponse

# Create your views here.
def index(request):
    #main pg
    return render(request, 'app_cc/index.html')


#Student Links
def avisos(request):
    return render(request, 'app_cc/avisos.html')


def boletim(request):
    if request.method == "POST":
        # Processar dados do formulário
        for disciplina in Disciplina.objects.all():
            # Recuperar a nota enviada pelo formulário
            nota_value = request.POST.get(f"notas[{disciplina.disciplina}]")
            if nota_value is not None:
                # Substituir vírgulas por pontos e, em seguida, converter para float
                nota_value = nota_value.replace(',', '.')
                try:
                    nota_value = float(nota_value)
                except ValueError:
                    return HttpResponse("Erro: Valor da nota inválido")

                # Obter a instância da nota correspondente
                nota_instance = Nota.objects.filter(disciplina=disciplina).first()
                if nota_instance:
                    # Atualizar a nota no banco de dados
                    nota_instance.nota = nota_value
                    nota_instance.save()

    # Recuperar disciplinas e notas
    disciplinas_com_notas = []
    for disciplina in Disciplina.objects.all():
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))

    return render(request, 'app_cc/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})


def diariop(request):
    return render(request, 'app_cc/diariop.html')


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

def diario(request):
    return render(request, 'app_cc/diario.html')
