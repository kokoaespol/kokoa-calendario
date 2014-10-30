from django.db import models
from django.contrib.auth.models import User
# Create your models here.

'''
Estudiante (username[first_name], -PK- matricula[last_name]) using User from django.contrib.auth.models
Materias Disponibles (ForeignKey[Estudiante], codigo, nombre, paralelos[String])
Curso (codigo_materia, paralelo, horario_clases, horario_examenes, aula)

'''
class Materia(models.Model):
	creditos = models.PositiveSmallIntegerField()
	nombre = models.CharField(max_length=20, blank="true", null="true")
	codigo = models.CharField(max_length=10, blank="true", null="true")
	paralelos = models.CharField(max_length=100, blank="true", null="true")

	def __unicode__(self):
		return unicode(self.nombre)


# wsMateriasDisponibles
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
	aula = models.CharField(max_length=11)

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
	matricula = models.CharField(max_length=11, blank="true", null="true")
	carrera = models.CharField(max_length=50, blank="true", null="true")
	promedio = models.CharField(max_length=5, blank="true", null="true")
	plan = models.ForeignKey(Plan, blank="true", null="true", related_name="Plan")
	materiaDisponibles = models.ManyToManyField(MateriaDisponible)
	
	def __unicode__(self):
		return unicode(self.username)

