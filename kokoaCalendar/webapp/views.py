# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponseBadRequest, HttpResponseNotFound
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import json
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from webservice import *
from webapp.models import *
#from apprest.models import *

# Create your views here.

def ingresar(request):
    if request.method == 'POST':
        usuario = request.POST['username']
        clave = request.POST['password']
        autenticacion= authenticate(username = usuario , password = clave)
     	if autenticacion is not None:
          login(request,autenticacion)
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
              servicio = Servicio()
              matricula = servicio.getMatricula(usuario)
              print matricula
              usuario_datos = Usuario(user = auth,matricula = matricula)
              usuario_datos.save()
              

              auth = authenticate(username = usuario , password = clave)
              if auth is not None:
                print auth
                login(request,auth) 
              return redirect('webapp.views.horario')
          else:
             return HttpResponseForbidden('Autenticacion Fallida')

    return render(request,"webapp/login.html")
		
def horario(request):
    #user = request.user
    user = request.user
    print user
    if not user.is_authenticated() :
      return HttpResponseForbidden('Debe hacer login')
    materias_disponibles = MateriaDisponible.objects.filter(username = user)
    print len(materias_disponibles)
    materias_list =[]
    if len(materias_disponibles) == 0 :
       servicio = Servicio()
       print 'aqui'
       matricula = Usuario.objects.filter(user= user)[0]
       print matricula
       materias = servicio.getMateriasDisponibles(matricula.matricula)
       print len(materias)
       materiadisp_ = MateriaDisponible()
       for materia in materias:
          materia.obtenerParalelos()
          print materia.creditos
          print materia.nombre
          nombre = materia.nombre
          print materia.codigo
          existe = Materia.objects.filter(codigo=materia.codigo)
          if len(existe)==0:            
            materia_ = Materia(creditos = materia.creditos,nombre =nombre, codigo = materia.codigo)
            materia_.save()
            materias_list.append(materia_)
#materiadisp_.materia.add(materia_)
            for paralelo in materia.paralelos:
               paralelo.getHorarios(materia.codigo)
               print 'paralleo'
               paralelo_ = Paralelo(numero = paralelo.numero, materia=materia_)
               paralelo_.save()
               print 'paralelos save'
               for hora in paralelo.horarios:
                  horario_ = Horario(dia=hora.dia,inicio=hora.inicio,fin=hora.final,curso=hora.curso, paralelo=paralelo_)
                  horario_.save()
       for m in materias_list:
          materiadisp_.materia.add(m)
       materiadisp_.save()      
         
    horarios = []
    context = {
      'materias':materias_disponibles
    }
    template = 'web/horario.html'
    return render(request, template, context)



