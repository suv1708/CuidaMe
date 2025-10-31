# views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from .models import Medico, Paciente, Cita, Metria
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import *
from .models import User, Medico, Paciente
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

# --- HOME (Landing con modals) ---


def home(request):
    login_form = CustomLoginForm()
    register_form = CustomUserCreationForm()
    return render(request, 'main/home.html', {
        'login_form': login_form,
        'register_form': register_form,
    })

# --- REGISTRO (procesa desde el modal) ---


def register_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('reg-email') or request.POST.get('email')
        password = request.POST.get('password')
        especialidad = request.POST.get('especialidad', None)
        tipo = request.POST.get('registro-tipo', 'paciente')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'El usuario ya existe.')
            return redirect('home')

        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        if tipo == 'medico':
            Medico.objects.create(
                user=user, especializacion=especialidad or "General")
            messages.success(
                request, f'Médico {first_name} registrado correctamente.')
        else:
            Paciente.objects.create(user=user)
            messages.success(
                request, f'Paciente {first_name} registrado correctamente.')

        return redirect('home')
    return redirect('home')

# --- LOGIN (procesa desde el modal) ---


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            # Redirección automática según el tipo de usuario
            if hasattr(user, 'medico'):
                messages.success(request, f'Bienvenido Dr. {user.first_name} {user.last_name}')
                return redirect('dashboard_medico')
            elif hasattr(user, 'paciente'):
                messages.success(request, f'Bienvenido {user.first_name} {user.last_name}')
                return redirect('dashboard_paciente')
            return redirect('home')
        
        else:
            messages.error(request, 'Credenciales incorrectas.')
            return redirect('home')
        
    return redirect('home')


# --- LOGOUT ---

def logout_view(request):
    logout(request)
    return redirect('home')

# --- DASHBOARDS ---


@login_required
def medico_pacientes(request):
    """Vista para ver pacientes del médico"""
    medico = request.user.medico
    citas = Cita.objects.filter(medico=medico)
    pacientes = set([cita.paciente for cita in citas])
    
    context = {
        'pacientes': pacientes
    }
    return render(request, 'main/medico_pacientes.html', context)

@login_required
def dashboard_medico(request):
    if not hasattr(request.user, 'medico'):
        return redirect('dashboard_paciente')

    medico = request.user.medico
    # Obtener pacientes con citas con este médico
    citas = Cita.objects.filter(medico=medico).order_by('fecha', 'hora')
    
    # Obtener todos los pacientes para referencia
    todos_pacientes = Paciente.objects.all()
    
    
    
    context = {
        'medico': medico,
        'citas': citas,
        'todos_pacientes': todos_pacientes,
        
    }
    
    return render(request, 'main/dashboard_medico.html', context)

@login_required
def detalle_paciente(request, paciente_id):
    """Vista para que el médico vea el detalle de un paciente específico"""
    if not hasattr(request.user, 'medico'):
        return redirect('dashboard_paciente')

    paciente = get_object_or_404(Paciente, id=paciente_id)

    # Obtener métricas y citas
    metria = Metria.objects.filter(paciente=paciente).first()
    citas = Cita.objects.filter(
        paciente=paciente, medico=request.user.medico).order_by('fecha', 'hora')

    if request.method == "POST":
        form = PacienteEditForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('detalle_paciente', paciente_id=paciente.id)
    else:
        form = PacienteEditForm(instance=paciente)

    context = {
        'paciente': paciente,
        'metria': metria,
        'citas': citas,
        'form': form,
    }
    return render(request, 'main/detalle_paciente.html', context)
    
        

@login_required
def medico_perfil(request):
    """Vista para el perfil del médico"""
    medico = request.user.medico
    
    context = {
        'medico': medico
    }
    return render(request, 'main/medico_perfil.html', context)

@login_required
def medico_citas(request):
    """Vista para gestionar citas del médico"""
    medico = request.user.medico
    citas = Cita.objects.filter(medico=medico).order_by('fecha', 'hora')
    
    context = {
        'citas': citas,
        'medico': medico
    }
    return render(request, 'main/medico_citas.html', context)


@login_required
def dashboard_paciente(request):
    if not hasattr(request.user, 'paciente'):
        return redirect('dashboard_medico')

    paciente = request.user.paciente
    
    # Obtener métricas del paciente
    try:
        metria = Metria.objects.get(paciente=paciente)
    except Metria.DoesNotExist:
        metria = None
    
    # Obtener citas del paciente
    citas = Cita.objects.filter(paciente=paciente).order_by('fecha', 'hora')
    
    context = {
        'paciente': paciente,
        'metria': metria,
        'citas': citas,
    }
    
    return render(request, 'main/dashboard_pacientes.html', context)

@login_required
def paciente_citas(request):
    """Vista para gestionar citas del paciente"""
        
    paciente = request.user.paciente
    citas = Cita.objects.filter(paciente=paciente).order_by('fecha', 'hora')
    medicos = Medico.objects.all()
    
    if request.method == 'POST':
        medico_id = request.POST.get('medico')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        descripcion = request.POST.get('descripcion')
        
        medico = get_object_or_404(Medico, id=medico_id)
        
        Cita.objects.create(
            medico=medico,
            paciente=paciente,
            fecha=fecha,
            hora=hora,
            description=descripcion
        )
        messages.success(request, 'Cita agendada correctamente')
        return redirect('paciente_citas')
    
    context = {
        'citas': citas,
        'medicos': medicos
    }
    return render(request, 'main/paciente_citas.html', context)

@login_required
def paciente_metricas(request):
    """Vista para gestionar métricas del paciente"""
    paciente = request.user.paciente
    
    try:
        metria = Metria.objects.get(paciente=paciente)
    except Metria.DoesNotExist:
        metria = None
    
    if request.method == 'POST':
        estatura = request.POST.get('estatura')
        peso = request.POST.get('peso')
        presion_arterial = request.POST.get('presion_arterial')
        frecuencia_cardiaca = request.POST.get('frecuencia_cardiaca')
        tipo_sangre = request.POST.get('tipo_sangre')
        
        if metria:
            metria.estatura = estatura
            metria.peso = peso
            metria.presion_arterial = presion_arterial
            metria.frecuencia_cardiaca = frecuencia_cardiaca
            metria.tipo_sangre = tipo_sangre
            metria.save()
        else:
            metria = Metria.objects.create(
                paciente=paciente,
                estatura=estatura,
                peso=peso,
                presion_arterial=presion_arterial,
                frecuencia_cardiaca=frecuencia_cardiaca,
                tipo_sangre=tipo_sangre
            )
        messages.success(request, 'Métricas actualizadas correctamente')
        return redirect('paciente_metricas')
    
    context = {
        'metria': metria,
        'tipos_sangre': Metria.BLOOD_TYPE_CHOICES
    }
    return render(request, 'main/paciente_metricas.html', context)

@login_required
def paciente_perfil(request):
    """Vista para el perfil del paciente"""
    paciente = request.user.paciente
    
    context = {
        'paciente': paciente
    }
    return render(request, 'main/paciente_perfil.html', context)

@login_required
def editar_perfil_paciente(request):
    """Vista para editar el perfil del paciente"""
    paciente = request.user.paciente
    form = PacienteForm(instance=request.user)
    
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente')
            return redirect('paciente_perfil')
        else:
            messages.error(request, 'Error al actualizar el perfil')
            context = {
                'form': form
            }
            return render(request, 'main/perfil_edit.html', context)

    context = {
        'form': form
    }
    return render(request, 'main/perfil_edit.html', context)
        
    


