import requests
import random

#Asignar las id de la base de datos de speedrun.com de los generos de videojuegos
id_puzzle="y72yd2do"
id_platform='qdnqqrn8'
id_sanbox='q4n60ln9'
id_metroidvania='qdnqyk28'

#Obtener los videojuegos pertenecientes a cada genero
gamePuzzle=requests.get('https://www.speedrun.com/api/v1/games?max=200&genre='+id_puzzle).json()['data']
gamePlatform=requests.get('https://www.speedrun.com/api/v1/games?max=200&genre='+id_platform).json()['data']
gameSandbox=requests.get('https://www.speedrun.com/api/v1/games?max=200&genre='+id_sanbox).json()['data']
gameMetroidvania=requests.get('https://www.speedrun.com/api/v1/games?max=200&genre='+id_metroidvania).json()['data']

#Definir funcion que permite escribir en el formato indicado para la base de conocimientos
def escribirBase(f,listaJuegos,genero,caracteristica):
    dif = ['dif_dificil', 'dif_media', 'dif_facil']
    for p in listaJuegos:
        id=p['id']
        nombre=p['names']['international']
        if nombre.find("\'")==-1:
            genero=genero
            caracterisitica_extra=caracteristica
            anio=p['released']
            antiguedad=''
            if anio>2000:
                antiguedad="nuevo"
            else:
                antiguedad="antiguo"
            dificultad=random.choice(dif)
            duracion = ''
            try:
                resTime=requests.get('https://www.speedrun.com/api/v1/games/'+id+'/records?times').json()['data'][0]['runs'][0]['run']['times']['primary_t']
            except IndexError:
                resTime=5400
            except KeyError:
                pass
            if resTime>=5400:
                duracion='dur_larga'
            elif resTime>= 1800:
                duracion='dur_media'
            else:
                duracion='dur_corta'
            print("game(\'" + nombre + "\'," + genero + "," + duracion + "," + antiguedad + "," + dificultad + "," + caracterisitica_extra + ").\n")
            try:
                f.write("game(\'"+nombre+"\',"+genero+","+duracion+","+antiguedad+","+dificultad+","+caracterisitica_extra+").\n")
            except UnicodeEncodeError:
                pass


f=open('base.pl','w')
escribirBase(f,gamePuzzle,"puzzle","pensar")
escribirBase(f,gamePlatform,"plataforma","etapas_distintas")
escribirBase(f,gameSandbox,"sandbox","mundo_abierto")
escribirBase(f,gameMetroidvania,"metroidvania","desbloquear_zonas")
f.close()

