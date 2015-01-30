from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import unicodedata
class Horas():
  dia = ""
  inicio = ""
  final = ""
  curso = ""
  def __init__(self, dia, inicio, final, curso):
    self.dia = dia 
    self.inicio = inicio
    self.final = final
    self.curso = curso 

class Paralelo_web():
  numero = ''
  horarios = []
  def __init__(self, numero):
    self.numero = numero

  def getHorarios(self, codigo):
    servicio = Servicio()
    print 'codigo'+ codigo 
    client = Client(servicio.url, doctor = servicio.doctor)
    resultado = client.service.wsHorarioClases(codigo, self.numero)
    lista = []
    for horario in resultado[1][0][0]:
      dia = horario['NOMBREDIA']
      inicio = horario['HORAINICIO']
      fin = horario['HORAFIN']
      curso = horario['AULA']
      print dia + inicio + fin + curso
      horario_ = Horas(dia,inicio,fin,curso)
      lista.append(horario_)
    self.horarios =  lista
  
class Materia_web():
  nombre =''
  tipo = ''
  creditos = 0
  facultad =''
  codigo = ''
  ultimo_cambio = ''
  paralelos = []

  def __init__(self,nombre,tipo,creditos,facultad,codigo,ultimo):
    self.nombre = ''.join((c for c in unicodedata.normalize('NFD', nombre) if unicodedata.category(c) != 'Mn'))
    self.tipo = tipo
    self.creditos = creditos
    self.facultad = facultad
    self.codigo = codigo 
    self.ultimo_cambio = ultimo

  def obtenerParalelos(self):
    servicio = Servicio()
    client = Client(servicio.url, doctor = servicio.doctor)
    resultado = client.service.wsBuscarMateria(self.codigo, '1')
    for paralelo in resultado[1][0][0]:
      paralelo_ = Paralelo_web(paralelo['PARALELO'])
      self.paralelos.append(paralelo_)

class Servicio():
  url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
  imp = Import('http://www.w3.org/2001/XMLSchema')
  imp.filter.add('http://tempuri.org/')
  doctor = ImportDoctor(imp)

  def getMatricula(self, username):
    client = Client(self.url, doctor=self.doctor)
    resultado = client.service.wsInfoUsuario(username)
    return resultado[1][0][0]['IDENTIFICACION']

  def getNombreCompleto(self, username):
    client = Client(self.url, doctor=self.doctor)
    resultado = client.service.wsInfoUsuario(username)
    return resultado[1][0][0]['NOMBRES'] + resultado[1][0][0]['APELLIDOS']

  def getTipo(self, username): 
    client = Client(self.url, doctor=self.doctor)
    resultado = client.service.wsInfoUsuario(username)
    return resultado[1][0][0]['TIPO']
  
  def getMateriasDisponibles(self, matricula):
    lista = []
    client = Client(self.url, doctor=self.doctor)
    resultado = client.service.wsMateriasDisponibles(matricula)
    for materia in resultado[1][0][0]:
       materia_ = Materia_web(materia['NOMBRE_MATERIA'],materia['TIPOCREDITO'],materia['NUMCREDITOS'],'',materia['COD_MATERIA_ACAD'],materia['ULTIMO_CAMBIO'])
       lista.append(materia_)
    return lista


      
      

