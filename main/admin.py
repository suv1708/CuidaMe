from django.contrib import admin
from .models import User, Paciente, Medico, Metria, Cita

# Personalización de modelos en el admin
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'id_number', 'phone_number')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'id_number')
    list_filter = ('is_staff', 'is_active')

class PacienteAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'get_email', 'get_telefono')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name()
    get_nombre_completo.short_description = 'Nombre Completo'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_telefono(self, obj):
        return obj.user.phone_number
    get_telefono.short_description = 'Teléfono'

class MedicoAdmin(admin.ModelAdmin):
    list_display = ('get_nombre_completo', 'especializacion', 'get_email', 'get_telefono')
    list_filter = ('especializacion',)
    search_fields = ('user__first_name', 'user__last_name', 'especializacion')
    
    def get_nombre_completo(self, obj):
        return obj.user.get_full_name()
    get_nombre_completo.short_description = 'Nombre Completo'
    
    def get_email(self, obj):
        return obj.user.email
    get_email.short_description = 'Email'
    
    def get_telefono(self, obj):
        return obj.user.phone_number
    get_telefono.short_description = 'Teléfono'

class MetriaAdmin(admin.ModelAdmin):
    list_display = ('get_paciente', 'estatura', 'peso', 'presion_arterial', 'frecuencia_cardiaca', 'tipo_sangre')
    list_filter = ('tipo_sangre',)
    
    def get_paciente(self, obj):
        return obj.paciente.user.get_full_name()
    get_paciente.short_description = 'Paciente'

class CitaAdmin(admin.ModelAdmin):
    list_display = ('get_paciente', 'get_medico', 'fecha', 'hora')
    list_filter = ('fecha', 'medico')
    search_fields = ('paciente__user__first_name', 'paciente__user__last_name', 'medico__user__first_name', 'medico__user__last_name')
    
    def get_paciente(self, obj):
        return obj.paciente.user.get_full_name()
    get_paciente.short_description = 'Paciente'
    
    def get_medico(self, obj):
        return obj.medico.user.get_full_name()
    get_medico.short_description = 'Médico'

# Registro de modelos con sus clases Admin personalizadas
admin.site.register(User, UserAdmin)
admin.site.register(Paciente, PacienteAdmin)
admin.site.register(Medico, MedicoAdmin)
admin.site.register(Metria, MetriaAdmin)
admin.site.register(Cita, CitaAdmin)
