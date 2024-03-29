from django.apps import AppConfig


class AppCcConfig(AppConfig):#App config deve ser usado pra colocar em settings
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app_cc'
