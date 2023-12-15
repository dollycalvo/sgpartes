from django.core.management.base import BaseCommand, CommandError
from partes.models import Empleado
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Agrega o actualiza usuarios al sistema'

    def handle(self, *args, **options):
        #Primero cargamos a los jefes
        jefes = [
            Empleado(legajo=16056,password=make_password("abc123"),apellidos='Barberis',nombres='Claudia Mabel ',puesto_id=2,email='barberis@gmail.com'),
            Empleado(legajo=16753,password=make_password("abc123"),apellidos='Bazzana',nombres='Santiago Pablo ',puesto_id=2,email='bazzana@gmail.com'),
            Empleado(legajo=18525,password=make_password("abc123"),apellidos='Di Pietrantonio',nombres='Carla',puesto_id=2,email='dipietrantonio@gmail.com'),
            Empleado(legajo=17773,password=make_password("abc123"),apellidos='Felicioni ',nombres='Flavia Eleonora',puesto_id=2,email='felicioni@gmail.com'),
            Empleado(legajo=16585,password=make_password("abc123"),apellidos='Moreira',nombres='Fabián Ariel ',puesto_id=2,email='moreira@gmail.com'),
            Empleado(legajo=15672,password=make_password("abc123"),apellidos='Murúa',nombres='Carlos Alejandro',puesto_id=2,email='murua@gmail.com'),
            Empleado(legajo=14604,password=make_password("abc123"),apellidos='Wentzeis',nombres='Luis María Pedro ',puesto_id=2,email='wentzeis@gmail.com'),
            Empleado(legajo=16714,password=make_password("abc123"),apellidos='Romero',nombres='Luis Darío',puesto_id=2,email='romero2@gmail.com'),
            Empleado(legajo=17074,password=make_password("abc123"),apellidos='Romero',nombres='Gastón Leonardo',puesto_id=2,email='romero1@gmail.com')
        ]            
            
        for jefe in jefes:
            jefe.save()
            
        for i in range(0, len(jefes)):
            if i < 7:
                jefes[i].jefe_directo = jefes[0]
            elif i == 7:
                jefes[i].jefe_directo = jefes[1]
            else:
                jefes[i].jefe_directo = jefes[4]
            jefes[i].save()
            
        agentes = [
            Empleado(legajo=21308,password=make_password("abc123"),apellidos='Ackerley',nombres='Pablo Alejandro',puesto_id=1,email='ackerley@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=21750,password=make_password("abc123"),apellidos='Alberio',nombres='Valentina',puesto_id=1,email='alberio@gmail.com',jefe_directo=jefes[6]),
            Empleado(legajo=20189,password=make_password("abc123"),apellidos='Azpitarte',nombres='Ignacio Agustín',puesto_id=1,email='azpitarte@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=16808,password=make_password("abc123"),apellidos='Badaracco',nombres='Carla Noemí',puesto_id=1,email='badaracco@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=10335,password=make_password("abc123"),apellidos='Befumo',nombres='Oscar Alberto',puesto_id=1,email='befumo@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=18025,password=make_password("abc123"),apellidos='Beliera',nombres='Juan Ignacio',puesto_id=1,email='beliera@gmail.com',jefe_directo=jefes[7]),
            Empleado(legajo=16810,password=make_password("abc123"),apellidos='Bellino',nombres='Pablo Armando',puesto_id=1,email='bellino@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=18215,password=make_password("abc123"),apellidos='Benhaim',nombres='Alejandra Inés',puesto_id=1,email='benhainm@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=19451,password=make_password("abc123"),apellidos='Beyfeld ',nombres='Yevgeniya',puesto_id=1,email='beyfeld@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=14570,password=make_password("abc123"),apellidos='Cabrera',nombres='Claudio Alejandro ',puesto_id=1,email='cabrera@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=17008,password=make_password("abc123"),apellidos='Calvo',nombres='María Dolores',puesto_id=1,email='mdcalvo@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=20011,password=make_password("abc123"),apellidos='Carbonell',nombres='Carlos Guillermo ',puesto_id=1,email='carbonell@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=18631,password=make_password("abc123"),apellidos='Cartelli',nombres='Carlos José',puesto_id=1,email='cartelli@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=18755,password=make_password("abc123"),apellidos='Casella',nombres='Federico',puesto_id=1,email='casella@gmail.com',jefe_directo=jefes[7]),
            Empleado(legajo=17881,password=make_password("abc123"),apellidos='Castillo',nombres='Ezequiel Matías ',puesto_id=1,email='castillo1@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=17155,password=make_password("abc123"),apellidos='Castillo',nombres='Jorge Martín',puesto_id=1,email='castillo2@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=21601,password=make_password("abc123"),apellidos='Cavallaro',nombres='Nicolas Gastón ',puesto_id=1,email='cavallaro@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=14761,password=make_password("abc123"),apellidos='Chautemps',nombres='Norma Adriana',puesto_id=1,email='chautemps@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=21832,password=make_password("abc123"),apellidos='Clerici',nombres='Alan',puesto_id=1,email='clerici@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=20983,password=make_password("abc123"),apellidos='Colaccini',nombres='Mariano',puesto_id=1,email='colaccini@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=21715,password=make_password("abc123"),apellidos='Dantones',nombres='Pedro Marco ',puesto_id=1,email='dantones@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=21878,password=make_password("abc123"),apellidos='De La Fuente',nombres='Javier Martín',puesto_id=1,email='delafuente@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=18325,password=make_password("abc123"),apellidos='Del Curto',nombres='Guillermo Eduardo',puesto_id=1,email='delcurto@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=21833,password=make_password("abc123"),apellidos='Del Villar',nombres='Leandro Iván',puesto_id=1,email='delvillar@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=20984,password=make_password("abc123"),apellidos='Fabio',nombres='Ernesto Javier',puesto_id=1,email='fabio@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=20999,password=make_password("abc123"),apellidos='Frith',nombres='Federico Augusto',puesto_id=1,email='frith@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=21632,password=make_password("abc123"),apellidos='Gasanego Barbuscio',nombres='Julián Tomás',puesto_id=1,email='gasanego@gmail.com',jefe_directo=jefes[8]),
            Empleado(legajo=19532,password=make_password("abc123"),apellidos='Gómez',nombres='Fernando Luis',puesto_id=1,email='gomez@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=21582,password=make_password("abc123"),apellidos='Gómez Fava',nombres='Florencia Victoria ',puesto_id=1,email='gomezfava@gmail.com',jefe_directo=jefes[8]),
            Empleado(legajo=20649,password=make_password("abc123"),apellidos='Gonzalez',nombres='Agustina Moira ',puesto_id=1,email='gonzalez@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=20988,password=make_password("abc123"),apellidos='Knaidel',nombres='Ariel David',puesto_id=1,email='knaidel@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=19837,password=make_password("abc123"),apellidos='Liendo',nombres='Hernán',puesto_id=1,email='liendo@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=19291,password=make_password("abc123"),apellidos='Martínez López',nombres='Javier Matías ',puesto_id=1,email='martinez@gmail.com',jefe_directo=jefes[6]),
            Empleado(legajo=20010,password=make_password("abc123"),apellidos='Martinetti',nombres='Mateo Augusto',puesto_id=1,email='martinetti@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=21587,password=make_password("abc123"),apellidos='Mendivil',nombres='Martín',puesto_id=1,email='mendivil@gmail.com',jefe_directo=jefes[8]),
            Empleado(legajo=20819,password=make_password("abc123"),apellidos='Mestre Ahumada',nombres='Guadalupe',puesto_id=1,email='mestreo@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=17428,password=make_password("abc123"),apellidos='Morales',nombres='Marcela Beatriz ',puesto_id=1,email='morales@gmail.com',jefe_directo=jefes[2]),
            Empleado(legajo=15188,password=make_password("abc123"),apellidos='Naccarato',nombres='Fernando Diego',puesto_id=1,email='nacaratto@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=18524,password=make_password("abc123"),apellidos='Núñez',nombres='Rodrigo Javier',puesto_id=1,email='nunez@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=17432,password=make_password("abc123"),apellidos='Ontiveros',nombres='Pablo Augusto ',puesto_id=1,email='ontiveros@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=17794,password=make_password("abc123"),apellidos='Orso',nombres='José Andrés',puesto_id=1,email='orso@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=20942,password=make_password("abc123"),apellidos='Parrino',nombres='Florencia',puesto_id=1,email='parrino@gmail.com',jefe_directo=jefes[6]),
            Empleado(legajo=11680,password=make_password("abc123"),apellidos='Pereyra',nombres='Adalberto Armando',puesto_id=1,email='pereyra@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=16563,password=make_password("abc123"),apellidos='Parlapiano',nombres='Mariela Silvia ',puesto_id=1,email='parlapiano@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=16987,password=make_password("abc123"),apellidos='Pescio',nombres='Gastón Omar',puesto_id=1,email='pescio@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=20992,password=make_password("abc123"),apellidos='Politano',nombres='Juan Manuel ',puesto_id=1,email='politano@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=13760,password=make_password("abc123"),apellidos='Quiroz',nombres='Horacio',puesto_id=1,email='quiroz@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=15424,password=make_password("abc123"),apellidos='Ríos',nombres='Juan Carlos',puesto_id=1,email='rios@gmail.com',jefe_directo=jefes[0]),
            Empleado(legajo=19936,password=make_password("abc123"),apellidos='Rodríguez',nombres='Juan José',puesto_id=1,email='rodriguez@gmail.com',jefe_directo=jefes[5]),
            Empleado(legajo=17721,password=make_password("abc123"),apellidos='Rodríguez Maziere ',nombres='Jennifer Mirna',puesto_id=1,email='maziere@gmail.com',jefe_directo=jefes[1]),
            Empleado(legajo=21511,password=make_password("abc123"),apellidos='Romero',nombres='María Celeste',puesto_id=1,email='romero3@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=21589,password=make_password("abc123"),apellidos='Roqueiro',nombres='Ariel Nicolas',puesto_id=1,email='roqueiro@gmail.com',jefe_directo=jefes[8]),
            Empleado(legajo=20343,password=make_password("abc123"),apellidos='Spataro',nombres='Fiamma Belén',puesto_id=1,email='spataro@gmail.com',jefe_directo=jefes[2]),
            Empleado(legajo=21590,password=make_password("abc123"),apellidos='Stein Palavecino',nombres='Ana',puesto_id=1,email='stein@gmail.com',jefe_directo=jefes[7]),
            Empleado(legajo=17944,password=make_password("abc123"),apellidos='Stella',nombres='Luis Roberto',puesto_id=1,email='stella@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=21013,password=make_password("abc123"),apellidos='Urcelay',nombres='Fernando Carlos ',puesto_id=1,email='urcelay@gmail.com',jefe_directo=jefes[2]),
            Empleado(legajo=15624,password=make_password("abc123"),apellidos='Zandonadi',nombres='Walter Fabián ',puesto_id=1,email='zandonari@gmail.com',jefe_directo=jefes[4]),
            Empleado(legajo=20300,password=make_password("abc123"),apellidos='Ruppel',nombres='Micael Esteban',puesto_id=1,email='ruppel@gmail.com',jefe_directo=jefes[7]),
            Empleado(legajo=21416,password=make_password("abc123"),apellidos='Rosas',nombres='Santiago Miguel',puesto_id=1,email='rosas@gmail.com',jefe_directo=jefes[3]),
            Empleado(legajo=21207,password=make_password("abc123"),apellidos='Martín',nombres='Leopoldo Mauricio',puesto_id=1,email='martin@gmail.com',jefe_directo=jefes[0])
        ]            
        
        for agente in agentes:
            agente.save()
