from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Função para redirecionar para uma página específica ao acessar a página inicial
def homepage(request):
    return redirect('login')  # Redirecionar para a rota 'login'

urlpatterns = [
    path('admin/', admin.site.urls),  # Rotas para o administrador
    path('auth/', include('users.urls')),  # Incluindo URLs do app 'users'
    path('app/', include('app_cc.urls')),  # Incluindo URLs do app 'app_cc'
    path('', homepage),  # Redirecionar para a página de login ao acessar o caminho raiz
]

# Configuração para servir arquivos estáticos/media
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)