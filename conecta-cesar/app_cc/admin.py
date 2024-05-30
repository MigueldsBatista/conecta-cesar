from django.contrib import admin
<<<<<<< HEAD:app_cc/admin.py
from app_cc.models import Disciplina, Nota, Diario, Turma, Nota, Aluno, Professor, Falta, Evento, Aviso
=======
from app_cc.models import Disciplina, Nota, Diario, Turma, Nota, Aluno, Professor, Falta, Evento, Aviso, Relatorio, NotaRelatorio, FaltaRelatorio
>>>>>>> eff11cadb53bf6d859484ed08b7fdf418d668f18:conecta-cesar/app_cc/admin.py

# Register your models here.
admin.site.register(Professor)
admin.site.register(Nota)
admin.site.register(Disciplina)
admin.site.register(Diario)
admin.site.register(Turma)
admin.site.register(Aluno)
admin.site.register(Falta)
admin.site.register(Evento)
admin.site.register(Aviso)
<<<<<<< HEAD:app_cc/admin.py
=======
admin.site.register(Relatorio)
admin.site.register(FaltaRelatorio)
admin.site.register(NotaRelatorio)

>>>>>>> eff11cadb53bf6d859484ed08b7fdf418d668f18:conecta-cesar/app_cc/admin.py



