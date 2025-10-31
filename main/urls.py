from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('register/', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/paciente/', dashboard_paciente, name='dashboard_paciente'),
    path('dashboard/medico/', dashboard_medico, name='dashboard_medico'),
    path('dashboard/medico/paciente/<int:paciente_id>/', detalle_paciente, name='detalle_paciente'),
    path('dashboard/paciente/perfil/',paciente_perfil, name='paciente_perfil'),
    path('dashboard/paciente/citas/', paciente_citas, name='paciente_citas'),
    path('dashboard/paciente/metricas/', paciente_metricas, name='paciente_metricas'),
    path('dashboard/paciente/perfil/editar/', editar_perfil_paciente, name='editar_perfil_paciente'),
    path('dashboard/medico/perfil/', medico_perfil, name='medico_perfil'),
    path('dashboard/medico/citas/', medico_citas, name='medico_citas'),
    path('dashboard/medico/pacientes/', medico_pacientes, name='medico_pacientes'),
]
