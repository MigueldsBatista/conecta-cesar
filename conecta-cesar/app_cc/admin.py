from django.contrib import admin


from app_cc.models import Login
from app_cc.models import Question
from app_cc.models import Question, Entry
from app_cc.models import Disciplina
from app_cc.models import Disciplina, Nota
from app_cc.models import Diario



# Register your models here.
admin.site.register(Login)
admin.site.register(Question)
admin.site.register(Entry)
admin.site.register(Nota)
admin.site.register(Disciplina)
admin.site.register(Diario)

