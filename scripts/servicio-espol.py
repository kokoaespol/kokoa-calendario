class estudiante:
   nombres=''
   apellidos=''
   matricula=''
   email=''
   user=''
   def setuser(self):
	self.user=self.email.split('@')[0]

from suds.xsd.doctor import ImportDoctor, Import
from suds.client import Client
import string


url = 'http://ws.espol.edu.ec/saac/wsandroid.asmx?WSDL'
imp = Import('http://www.w3.org/2001/XMLSchema') # the schema to import.
imp.filter.add('http://tempuri.org/')

doctor = ImportDoctor(imp)
client = Client(url, doctor=doctor)

username = ''
matricula = ''
codigoMateria = ''

materiasDisponibles = []
horarioExamenes = []
horarioClases = []
estudiantes=[]
archivo=open('guardar.txt','r')
for line in archivo.readlines():
    if line.__len__>4:
       estu=estudiante()
       estu.matricula=line
       estudiantes.append(estu)
archivo.close()
i=0
for estudiante in estudiantes:
     if estudiante.matricula.__len__>5:
        try:
            matricula =  client.service.wsInfoPersonalEstudiante(int(estudiante.matricula.strip()),'')        
	    estudiante.email= matricula.diffgram.NewDataSet.INFOPERSONALESTUDIANTE.EMAIL
	    estudiante.nombres= matricula.diffgram.NewDataSet.INFOPERSONALESTUDIANTE.NOMBRES
	    estudiante.apellidos= matricula.diffgram.NewDataSet.INFOPERSONALESTUDIANTE.APELLIDOS
            estudiante.setuser()
	    print(estudiante.matricula+' | '+estudiante.user+' | '+estudiante.email+'\n')
        except:
	    print(estudiante.matricula+'Error\n')

#       print estudiante.email	
final=open('final.txt','w')
for estudiante in estudiantes:
    final.write(estudiante.matricula.strip()+' | '+estudiante.user+' | '+estudiante.email+'\n')
final.close()
# APELLIDOS
# CIUDADNACIMIENTO
# FECHANACIMIENTO
# FOTO
# NOMBRES
# PAISNACIMIENTO
# SEXO
#materiasDisponibles =  client.service.wsMateriasDisponibles(matricula)
#horarioClases = client.service.wsHorarioClases(codigoMateria, paralelo)
#horarioExamenes = client.service.wsHorarioClases(codigoMateria, paralelo)
