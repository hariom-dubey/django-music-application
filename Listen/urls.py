from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from music import views

urlpatterns = [
    path('', views.main_pg, name='main_pg'),
    path('manage/hariom/', admin.site.urls),
    path('music/', include('music.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



