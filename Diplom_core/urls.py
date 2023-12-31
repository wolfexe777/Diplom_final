from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('PsichologyTest.urls')),
    path('', TemplateView.as_view(template_name='base.html')),
]
