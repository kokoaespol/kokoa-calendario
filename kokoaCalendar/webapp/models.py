from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''
Estudiante (username[first_name], -PK- matricula[last_name]) using User from django.contrib.auth.models
Materias Disponibles (ForeignKey[Estudiante], codigo, nombre, paralelos[String])
Curso (codigo_materia, paralelo, horario_clases, horario_examenes, aula)

'''
class Usuario(models.Model):
  user = models.ForeignKey(User)
  matricula = models.CharField(max_length=10)

  def __unicode__(self):
		return unicode(self.matricula)

class Materia(models.Model):
    creditos = models.PositiveSmallIntegerField()
    nombre = models.CharField(max_length=20, blank=True, null=True, unique=True)
    codigo = models.CharField(max_length=10, blank=True, null=True, unique=True)
    def __unicode__(self):
        return unicode(self.nombre)
 
class Paralelo(models.Model):
    numero = models.PositiveSmallIntegerField()
    materia = models.ForeignKey(Materia, related_name='paralelo')

    def __unicode__(self):
        return unicode(self.numero)

class Horario(models.Model):
    dia = models.CharField(max_length=10)
    inicio = models.CharField(max_length=10)
    fin = models.CharField(max_length=10)
    curso = models.CharField(max_length=10)
    paralelo = models.ForeignKey(Paralelo, related_name ='horario') 

    def __unicode__(self):
        return unicode(self.dia + self.curso)


#wsMateriasDisponibles
class MateriaDisponible(models.Model):
	username = models.ForeignKey(User)
	materia = models.ManyToManyField(Materia)

	def __unicode__(self):
		return unicode(self.materia)

class Curso(models.Model):
	materia = models.ForeignKey(Materia)
	paralelo = models.PositiveSmallIntegerField()
	horario_clases = models.CharField(max_length=50)
	horario_examenes = models.CharField(max_length=50)
	aulaClase = models.CharField(max_length=200)
	aulaExamen = models.CharField(max_length=200)
	def __unicode__(self):
		return unicode(self.materia)

class Plan(models.Model):
	username = models.ForeignKey(User)
	curso = models.ManyToManyField(Curso)

	def __unicode__(self):
		return unicode(self.username)


# wsInfoEstudianteGeneral
class Estudiante(models.Model):
	username = models.ForeignKey(User)
	matricula = models.CharField(max_length=11, blank=True, null=True)
	carrera = models.CharField(max_length=50, blank=True, null=True)
	promedio = models.CharField(max_length=5, blank=True, null=True)
	plan = models.ForeignKey(Plan, blank=True, null=True, related_name="Plan")
	materiaDisponibles = models.ManyToManyField(MateriaDisponible)
	
	def __unicode__(self):
		return unicode(self.username)


