from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseForbidden, HttpResponse, HttpResponseBadRequest, HttpResponseNotFound
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import json
#from apprest.models import *

# Create your views here.

def login1(request):
    try:
        user = request.POST['username'].strip()
        pwd = request.POST['password'].strip()
        print 'Holi' + pwd
        return HttpResponse(str(pwd))
    except:
        return HttpResponseBadRequest('Error parametros')
    """
	from django.contrib.auth import authenticate, login
    auth = authenticate(username = user , password = pwd)
    if auth is not None:
        login(request, auth)
        response = {'username':auth.pk}

        #return HttpResponse(json.dumps(response))
        return HttpResponse(auth.pk,status=202)
    else:

        url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
        imp = Import('http://www.w3.org/2001/XMLSchema')
        imp.filter.add('http://tempuri.org/')
        doctor = ImportDoctor(imp)
        client = Client(url, doctor=doctor)
        auth = client.service.autenticacion(user,pwd)

        if auth == True:
            auth = User.objects.create_user(username=user, password=pwd)
            auth.save()
            auth = authenticate(username = user , password = pwd)
            #auth = User.objects.filter(username = user)
            login(request,auth) 
            return HttpResponse(auth.pk,status=202)
        else:
            #self.username = None
            #self.password = None
            return HttpResponseForbidden('Autenticacion Fallida')


        #erficiar usuario en web servic
        #if el usuario de arriba existe, save
        #user = User(userna,pawd) .save
        #login(request, user)a
        #else 
        #return HttpBadRequest('Valio')
        #return HttpResponseBadRequest('Error autenticacion')"""

def horario(request):
    #user = request.user
    materias_disponibles =['Calculo','Historia','Lenguaje'] 
    horarios = []
    context = {
      'materias':materias_disponibles
    }
    template = 'web/horario.html'
    return render(request, template, context)



