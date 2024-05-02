from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include("users.urls")),
    path('', include('users.urls')),
    path('/', include('app_cc.urls'))
    
]
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)