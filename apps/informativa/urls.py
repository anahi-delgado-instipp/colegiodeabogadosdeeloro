from django.urls import path
from apps.informativa import views
from .views import pagina_informatica

urlpatterns = [
    path('', views.pagina_informatica, name='pagina_informatica')
    

]
