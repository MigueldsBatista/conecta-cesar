from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Disciplina, Nota, Diario
from rolepermissions.decorators import has_role_decorator
from rolepermissions.decorators import has_permission_decorator
from project_cc.roles import Professor, Aluno


# Register
 

# -----------------------------------------STUDENT VIEWS--------------------------------------------
@has_role_decorator(Aluno)
def avisos(request):
    return render(request, 'app_cc/aluno/avisos.html')
#----------------------------------------------------------------------------------------------------------------    
@has_role_decorator(Aluno)
def disciplinas_e_notas(request):
    disciplinas_com_notas = []
    disciplinas = Disciplina.objects.all()
    for disciplina in disciplinas:
        notas = Nota.objects.filter(disciplina=disciplina)
        disciplinas_com_notas.append((disciplina, notas))
    return render(request, 'app_cc/aluno/disciplina.html', {'disciplinas_com_notas': disciplinas_com_notas})

#----------------------------------------------------------------------------------------------------------------    
@has_role_decorator(Aluno)
def boletim(request):
    disciplinas = Disciplina.objects.all()
    disciplinas_com_notas = []
    for disciplina in disciplinas:
        try:
            nota_instance = Nota.objects.get(disciplina=disciplina)
        except Nota.DoesNotExist:
            nota_instance = None
        disciplinas_com_notas.append((disciplina, nota_instance))
    return render(request, 'app_cc/aluno/boletim.html', {'disciplinas_com_notas': disciplinas_com_notas})
#----------------------------------------------------------------------------------------------------------------   
@has_role_decorator(Aluno) 
def frequencia(request):
    return render(request, 'app_cc/aluno/frequencia.html')
#---------------------------------------------------------------------------------------------------------------- 
   
@has_role_decorator(Aluno)
def perfil(request):
    return render(request, 'app_cc/aluno/perfil.html')

#---------------------------------------------------------------------------------------------------------------- 

@has_role_decorator(Aluno)
def diario(request):
    # Obtém todos os diários salvos
    diarios = Diario.objects.all()
    # Renderiza o template 'app_cc/diario.html' passando os diários para o contexto
    return render(request, 'app_cc/aluno/diario.html', {'diarios': diarios})


@has_role_decorator(Aluno)
def calendario(request):
    return render('app_cc/aluno/calendario.html')

#----------------------------------------------------------------------------------------------------------------    
#----------------------------------------PROFESSOR VIEWS---------------------------------------------------------  
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def turmas(request):
    return render(request, 'app_cc/professor/turmas.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def perfilp(request):
    return render(request, 'app_cc/professor/perfilp.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def frequenciap(request):
    return render(request, 'app_cc/professor/frequenciap.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def calendariop(request):
    return render(request, 'app_cc/professor/calendariop.html')
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def diariop(request):
    if request.method == 'POST':
        disciplina = request.POST.get('disciplina')
        titulo = request.POST.get('titulo')
        texto = request.POST.get('texto')
        Diario.objects.create(disciplina=disciplina, titulo=titulo, texto=texto)
        return redirect('diariop')
    else:
        diarios = Diario.objects.all()
        return render(request, 'app_cc/professor/diariop.html', {'diarios': diarios})
#----------------------------------------------------------------------------------------------------------------    

@has_role_decorator(Professor)
def avisosp(request):
    return render(request, 'app_cc/professor/avisosp.html')
#----------------------------------------------------------------------------------------------------------------    
@has_role_decorator(Professor)
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

    return render(request, 'app_cc/professor/boletimp.html', {'disciplinas_com_notas': disciplinas_com_notas})




