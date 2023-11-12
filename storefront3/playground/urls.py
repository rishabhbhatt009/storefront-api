from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path('email/', views.send_email),
    path('broker/', views.message_broker),
    # path('slow_api/', views.slow_api),
    path('slow_api', views.slow_api.as_view())
]
