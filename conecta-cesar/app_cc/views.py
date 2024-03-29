from django.shortcuts import render

# Create your views here.
def index(request):
    #main pg
    return render(request, 'app_cc/index.html')
""" tudo que está sendo trabalhado dentro dessa função """

def aviso(request):
    return render(request, 'app_cc/avisos.html')

def disciplina(request):
    return render(request, 'app_cc/disciplina.html')

"""Para cada arquivo html é preciso fazer uma def de request do caminho do arquivo para o app"""