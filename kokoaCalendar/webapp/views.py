from django.shortcuts import render

# Create your views here.

def horario(request):
    #user = request.user
    materias_disponibles =['Calculo','Historia','Lenguaje'] 
    horarios = []
    context = {
      'materias':materias_disponibles
    }
    template = 'web/horario.html'
    return render(request, template, context)


