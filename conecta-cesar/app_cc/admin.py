from django.contrib import admin


from app_cc.models import Login
from app_cc.models import Question
from app_cc.models import Question, Entry



# Register your models here.
admin.site.register(Login)
admin.site.register(Question)
admin.site.register(Entry)


