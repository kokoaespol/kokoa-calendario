import sys
from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO
from webapp.models import *

#Funcion que realiza la conversion de un pdf a un txt y un Arreglo de String
def convert_pdf_to_txt(path):

    matriculas = []
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = file(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos=set()
    
    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
        interpreter.process_page(page)
    fp.close()
    device.close()
    str = retstr.getvalue()
    retstr.close()
    
    arreglo = str.split("\n")
    

    for i in arreglo:
        
        tmp = i
        #tmp = tmp.split(" ")
        #tmp.pop(0)
        if len(tmp) == 9:
            if tmp.isdigit():
                matriculas.append(tmp)
            
    #text_file = open("UltimasMatriculas.txt", "w")
    #text_file.write("%s" % unicode(matriculas))
    #text_file.close()           
    #print matriculas"""
    return matriculas
    

def consulta_Materias_Estudiante():


	allMatriculas = convert_pdf_to_txt('/home/julio/Escritorio/LISTADOS_ESTUDIANTES_DE_LA_ESPOL.pdf')
	
	url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
	imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
	imp.filter.add('http://tempuri.org/')

	doctor = ImportDoctor(imp)
	client = Client(url, doctor=doctor)

	materiasDisponibles = []
	horarioExamenes = []
	horarioClases = []
	cursos = []
	paralelosEstudiante = []
	total = []
	
	#Obtenemos la Matricula de un estudiante apartir de su username
	#matricula =  client.service.wsConsultaCodigoEstudiante(username)
	#matricula = matricula[1].__getitem__(0).__getitem__(0).__getitem__("COD_ESTUDIANTE")
	
	#Registramos los users
	#user = User.objects.create_user(username = 'Cirguelero', password = '1',first_name = 'Ronald Geovanny',
	#								 last_name = 'Luna Alburquerque', email = 'cirguelero@gmail.com')
	#user.save()
	
	#Recorremos todas las materias disponibles de un estudiante
	#paraleloInicio 
	#paraleloFinal

	nallMatriculas = len(allMatriculas)

	for i in range(0,nallMatriculas):
		matricula = allMatriculas[i]

		#Obtenemos informacion del estudiante
		info_Estudiante = client.service.wsInfoEstudianteGeneral(matricula)
		#total.append(info_Estudiante)
		username_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("USUARIO") 
		nombres_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("NOMBRES")
		apellidos_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("APELLIDOS")
		promedioGeneral_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("PROMEDIOGENERAL")
		carrera_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("CARRERA")
		email_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("EMAIL")
		#facultad_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("FACULTAD")
		#factorP_Estudiante = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("FACTOR")
		#foto = infoEstudiante[1].__getitem__(0).__getitem__(0).__getitem__("FOTO")

	
		#print (total)
		#print len(total)

		#Obtenemos el numero de Materias Disponibles de un estudiante 
		materiasDisponibles =  client.service.wsMateriasDisponibles(matricula)
		nMateriasDisponibles = len(materiasDisponibles[1].__getitem__(0).__getitem__(0))
		
		usernameAPIs = User.objects.get(username=username)
		
		estudiante = Estudiante(username = usernameAPIs, matricula = matricula,carrera = carrera_Estudiante,promedio = promedioGeneral_Estudiante)
		estudiante.save()
		
		matDisponible = MateriaDisponible(username = usernameAPIs)
		matDisponible.save()
		
		for i in range(0,nMateriasDisponibles):
			infoParalelos = []
			paralelosExistentes =[]
			cadenaParalelos = ''
			
			codigoMateria = materiasDisponibles[1].__getitem__(0).__getitem__(0).__getitem__(i).__getitem__("COD_MATERIA_ACAD")
			nombreMateria = materiasDisponibles[1].__getitem__(0).__getitem__(0).__getitem__(i).__getitem__("NOMBRE_MATERIA")
			numeroCreditos = materiasDisponibles[1].__getitem__(0).__getitem__(0).__getitem__(i).__getitem__("NUMCREDITOS")
			nombreMateria = nombreMateria.encode('utf-8')
			
			
			try:
				#Obtenemos los paralelos de cada Materia
				consultaParalelos =  client.service.wsBuscarMateria(codigoMateria,1)
				nConsultaParalelos = len(consultaParalelos[1].__getitem__(0).__getitem__(0).__getitem__(0))
			#except:
			#	print("Error: codigoMateria not found")
			
				#Concatenacion de todos los paralelos
				for p in range(0,nConsultaParalelos):
					paralelosExistentes.append(consultaParalelos[1].__getitem__(0).__getitem__(0).__getitem__(p).__getitem__("PARALELO"))
					cadenaParalelos = cadenaParalelos + str(consultaParalelos[1].__getitem__(0).__getitem__(0).__getitem__(p).__getitem__("PARALELO")) + ',' 
				
			#try:
				#Registro de una materia con todos sus respectivos paralelos
				materiaAPIs = Materia(creditos = numeroCreditos, nombre = nombreMateria, codigo = codigoMateria, paralelos = cadenaParalelos)
				materiaAPIs.save()
			#except:
			#	print("Error: materiaAPIs not Post or already exist!!!")
			
			#try:
				#Obtenemos una referncia a un objecto Materia
				nombreMateriaAPIs = Materia.objects.get(nombre = nombreMateria)

				
				matDisponible.materia.add(nombreMateriaAPIs)
				matDisponible.save()



			#except:
			#	nombreMateriaAPIs = ''
			#	print("Error: nombreMateriaAPIs not found")

			#if nombreMateriaAPIs != '':
					
			#try:
				#Recorremos todos los paralelos existente en una materia
				for paralelo in paralelosExistentes:
					m = []
					
					#Obtenemos el horario de clases y examenes de una materia
					horarioClases = client.service.wsHorarioClases(codigoMateria, paralelo)
					horarioExamenes = client.service.wsHorarioExamenes(codigoMateria, paralelo)
					
					if len(horarioClases[1]) != 0:
						tmpClase = []
						tmpExamen = []
						a = ''
						a1 = ''
						b = ''
						b1 = ''
						#Obtenemos cuantos dias de clases y examenes hay en un paralelo
						nHorarioClases=len(horarioClases[1].__getitem__(0).__getitem__(0))
						nHorarioExamenes=len(horarioExamenes[1].__getitem__(0))

						#Recorremos para consultar la hora y dia de una materia
						for h in range(0,1):

							#Consulta de Informacion sobre Examenes
							codigoAulaClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("AULA")
							bloqueAulaClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("BLOQUE")
							campusClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("CAMPUS")
							bloqueCampusClase= horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("BLOQUECAMPUS")
							idAulaClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("IDAULA")

							horaInicioClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("HORAINICIO")
							horaFinalClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("HORAFIN")
							diaClase = horarioClases[1].__getitem__(0).__getitem__(0).__getitem__(h).__getitem__("NOMBREDIA")
							
							codigoAulaClase = codigoAulaClase.encode('utf-8')
							a = a + diaClase + ':' + horaInicioClase + '-' + horaFinalClase + ','
							a1 = a1 + diaClase +  ':' + codigoAulaClase + '-' + bloqueAulaClase + '-' + campusClase + '-' \
									+ bloqueCampusClase + '-' + idAulaClase + ',' 
							#a = [codigoAulaClase,bloqueAulaClase,campusClase,bloqueCampusClase,idAulaClase,horaInicioClase,horaFinalClase,diaClase]
							#tmpClase.append(a)
							
						for e in range(0,1):
							
							#Consulta de Informacion sobre Examenes
							codigoAulaExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("AULA")
							bloqueAulaExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("BLOQUE")
							campusExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("CAMPUS")
							bloqueCampusExamen= horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("BLOQUECAMPUS")
							idAulaExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("IDAULA")
							
							horaInicioExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("HORAINICIO")
							horaFinalExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("HORAFIN")
							diaExamen = horarioExamenes[1].__getitem__(0).__getitem__(e).__getitem__("NOMBREDIA")
							
							codigoAulaExamen = codigoAulaExamen.encode('utf-8')
							b = b + diaExamen + ':' + horaInicioExamen + '-' + horaFinalExamen + ','
							b1 = b1 + diaExamen +  ':' + codigoAulaExamen + '-' + bloqueAulaExamen + '-' + campusExamen + '-' 
									+ bloqueCampusExamen + '-' + idAulaExamen + ',' 
							#b = [codigoAulaExamen,bloqueAulaExamen,campus,bloqueCampus,idAulaExamen,horaInicioExamen,horaFinalExamen,diaExamen]
							#tmpExamen.append(b)


						
						curso = Curso(materia = nombreMateriaAPIs ,paralelo = paralelo, horario_clases = a, horario_examenes= b, aulaClase = a1, aulaExamen = b1 )
						curso.save()
						#materia = Materia.objects.get(materia = nombreMateriaAPIs)
						
						
						#m = [paralelo,codigoMateria,nombreMateria, tmpClase,tmpExamen]
						#infoParalelos.append(m)



			except:
				print("Error: service not found or name not found")
		
		md = MateriaDisponible.objects.get(username = usernameAPIs)
		estudiante.MateriaDisponibles.add(md)
		estudiante.save()

			#cursos.append(infoParalelos)

		#materiasEstudiante.append(cursos)
		#estudiante = apped.([matricula,cursos])
	
	#return estudiante
	

#print (convert_pdf_to_txt('/home/julio/Escritorio/LISTADOS_ESTUDIANTES_DE_LA_ESPOL.pdf'))

consulta_Materias_Estudiante()


#print "FIN"

"""
[201218737, [[[ESPOL00059, DEPORTE RECREATIVO: TENIS, [[CANCHA DE TENIS, 
BLOQUE DEPORTE, CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 933, 
PT13H, PT14H30M, LUNES], [CANCHA DE TENIS, BLOQUE DEPORTE, CAMPUS PROSPERINA, 
BLOQUE DEPORTE CAMPUS PROSPERINA, 933, PT13H, PT14H30M, MIERCOLES]], []]]]]
FIN


[201218737, [[  ]]]
[ESPOL00059, DEPORTE RECREATIVO: TENIS, [[CANCHA DE TENIS, 
BLOQUE DEPORTE, CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 933,
 PT13H, PT14H30M, LUNES], [CANCHA DE TENIS, BLOQUE DEPORTE, CAMPUS PROSPERINA, 
 BLOQUE DEPORTE CAMPUS PROSPERINA, 933, PT13H, PT14H30M, MIERCOLES]], []], 
 [ESPOL00059, DEPORTE RECREATIVO: TENIS, [[CANCHA DE TENIS, BLOQUE DEPORTE, 
 CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 933, PT9H, PT10H30M, MARTES], 
 [CANCHA DE TENIS, BLOQUE DEPORTE, CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 
 933, PT9H, PT10H30M, JUEVES]], []]
 

 [201218737, [  ]]

  [[ESPOL00059, DEPORTE RECREATIVO: TENIS, [['CANCHA DE TENIS', 
 BLOQUE DEPORTE, CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 933,
  PT13H, PT14H30M, LUNES], ['CANCHA DE TENIS', BLOQUE DEPORTE, CAMPUS PROSPERINA,
  BLOQUE DEPORTE CAMPUS PROSPERINA, 933, PT13H, PT14H30M, MIERCOLES]], []]]

  [[ESPOL00042, DEPORTE RECREATIVO: PING PONG, [['COLISEO SECCI\xc3\x93N PING PONG', 
  BLOQUE DEPORTE, CAMPUS PROSPERINA, BLOQUE DEPORTE CAMPUS PROSPERINA, 936, PT12H, 
  PT13H30M, LUNES], ['COLISEO SECCI\xc3\x93N PING PONG', BLOQUE DEPORTE, CAMPUS PROSPERINA, 
  BLOQUE DEPORTE CAMPUS PROSPERINA, 936, PT12H, PT13H30M, MIERCOLES]], []]]
  """
