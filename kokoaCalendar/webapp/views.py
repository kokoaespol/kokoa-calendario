from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
 
#from apprest.models import *

# Create your views here.

def ingresar(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        autenticacion= authenticate(username = usuario , password = clave)
     	if autenticacion is not None:
            return redirect('webapp.views.horario')
        else:
            
            url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
            imp = Import('http://www.w3.org/2001/XMLSchema')
            imp.filter.add('http://tempuri.org/')
            doctor = ImportDoctor(imp)
            client = Client(url, doctor=doctor)
            auth = client.service.autenticacion(usuario, clave)

            if auth == True:
                auth = User.objects.create_user(username=usuario, password=clave)
                auth.save()
                auth = authenticate(username = usuario , password = clave)
                login(request,auth) 
                return redirect('webapp.views.horario')
            else:
               return HttpResponseForbidden('Autenticacion Fallida')

    return render(request,"webapp/login.html")
		
def horario(request):
    #user = request.user
    materias_disponibles =['Calculo','Historia','Lenguaje'] 
    horarios = []
    context = {
      'materias':materias_disponibles
    }
    template = 'web/horario.html'
    return render(request, template, context)



