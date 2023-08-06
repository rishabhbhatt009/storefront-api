from django.urls import path
from django.views.generic import TemplateView
from . import views

# URLConf
urlpatterns = [
    # path for the root endpoint
    path('', TemplateView.as_view(template_name='core/index.html')),
]
