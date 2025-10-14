from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

# Медиа-файлы из MEDIA_ROOT
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Статическая раздача ресурсов проекта (только для разработки)
urlpatterns += static('/images/', document_root=os.path.join(settings.BASE_DIR, 'images'))
urlpatterns += static('/videos/', document_root=os.path.join(settings.BASE_DIR, 'videos'))
urlpatterns += static('/audio/', document_root=os.path.join(settings.BASE_DIR, 'audio')) 