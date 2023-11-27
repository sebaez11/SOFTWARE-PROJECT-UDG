from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView
from .models import Paciente

# Forms
from .forms import PacienteForm

class CustomLoginView(LoginView):
    template_name = 'login.html'


class PacienteUpdateView(UpdateView):
    model = Paciente
    template_name = 'editar_paciente.html'
    fields = ['nombre', 'direccion', 'email']
    success_url = reverse_lazy('lista_pacientes')

def lista_pacientes(request):
    pacientes = Paciente.objects.all()
    return render(request, 'lista_pacientes.html', {'pacientes': pacientes})

def registrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pacientes')
    else:
        form = PacienteForm()
    
    return render(request, 'registrar_paciente.html', {'form': form})