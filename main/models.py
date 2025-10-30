from django.db import models
from django.contrib.auth.models import AbstractUser 

# Create your models here.


class User(AbstractUser):
    id_number = models.CharField(max_length=20, unique=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    def edad(self):
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
    
    def __str__(self):
        return self.get_full_name()
    
    
class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    historial_medico = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.user.get_full_name()
    
class Metria(models.Model):
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),  
        ('N/E', 'No especificado') 
    ]
    
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    estatura = models.FloatField(blank=False)
    peso = models.FloatField(blank=False)
    presion_arterial = models.CharField(max_length=20, blank=False, default="120/80")
    frecuencia_cardiaca = models.IntegerField(default=80)
    tipo_sangre = models.CharField(max_length=20, choices=BLOOD_TYPE_CHOICES, default="N/E")
    
class Medico(models.Model):
    SPECIALIZATION_CHOICES = [
        ('Dermatología', 'Dermatólogo'),
        ('Neurocirugía', 'Neurocirujano'),
        ('Ortopedia', 'Ortopedista'),
        ('General', 'Médico General'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    especializacion = models.CharField(choices=SPECIALIZATION_CHOICES, default="General")
    
    def __str__(self):
        return f"Dr. {self.user.get_full_name()} - {self.especializacion}"
    
class Cita(models.Model):
    medico = models.ForeignKey(Medico, on_delete=models.CASCADE)
    paciente = models.OneToOneField(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    description = models.TextField(blank=True, null=True)
    
    
    def __str__(self):
        return f"Cita de {self.paciente.user.get_full_name()} con {self.medico.user.get_full_name()} el {self.fecha} a las {self.hora}"
    
