from django.shortcuts import render

# Create your views here.
def index(request):
    #main pg
    return render(request, 'app_cc/index.html')
""" tudo que está sendo trabalhado dentro dessa função """


#Student Links
def aviso(request):
    return render(request, 'app_cc/avisos.html')

def disciplina(request):
    return render(request, 'app_cc/disciplina.html')

def boletim(request):
    return render(request, 'app_cc/boletim.html')

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

"""Para cada arquivo html é preciso fazer uma def de request do caminho do arquivo para o app"""