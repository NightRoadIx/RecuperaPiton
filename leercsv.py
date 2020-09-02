'''
  Lectura de archivos CSV directamente descargados de una página en la web www

  URL Uniform Resource Locator 
  URI Uniform Resource Indicator
'''
# Las librerías que se tienen que importar
import requests                   # Realizar pedidos por medio de la www
import urllib.request             # hacer pedidos utilizando URL
import time
from bs4 import BeautifulSoup     # Manejar páginas web con hipertexto

import pandas                     # Manejo de grandes cantidades de datos
import numpy as np                # Manejo de datos numéricos
import matplotlib.pyplot as mp    # Manejo de gráficas

# # # # # # # # DESCARGA DE DATOS # # # # # # # #
# Requerir de una URL
# Muy similar a lo su sucede en una computadora de forma local
# C:\Mis Documentos\
url = 'http://web.mta.info/developers/turnstile.html'

# ***
# TODO: Controlar los posibles errores o excepciones que puedan aparecer al
#       solicitar la respuesta de la página web

# Solicitar por medio de la web la respuesta del sitio
respuesta = requests.get(url)
# Ver la respuesta
print(respuesta)

# Ahora se arreglarán estos datos con las funciones de BeautifulSoup
# parser -> Analizador sintáctico 
sopa = BeautifulSoup(respuesta.text, "html.parser")
# Esto va a mostrar el código fuente de la página
print(sopa.prettify())

# Encontrar y mostrar todas las etiquetas que inicien con <a ...>
sopa.findAll('a')

# ***
# TODO: Estos datos se alamacenen en un archivo de texto (de forma local)
# para agilizar entonces las descargas

# ***
# TODO: Generar una lista con el texto colocado en la página web
# esto es por ejemplo: Saturday, August 03, 2019
#
# De ser posible modificar esas fechas a lenguaje castellano (español pues)

# Generar una lista para guardar los enlaces
listaEnlaces = []
# Recorrer entonces la lista con las etiquetas <a ...>
for enlace in sopa.findAll('a'):
  # De esas etiquetas obtener (get) a lo que este apuntando
  # 'href'
  tmp = enlace.get('href')
  # Eso convertirlo a una cadena de texto y comparar 
  # donde aparezca 'txt' y 'data' que son aquellos enlaces
  # de interés, pues son los que contienen información
  if(( "txt" in str(tmp) ) and ( "data" in str(tmp) )):
    # Mostrarlos
    print( str(tmp) )
    # Añadirlos a la lista
    listaEnlaces.append(str(tmp))

# TODO: Contabilizar cuantos elementos hay y colocarlos como disponibles de
#       lectura

# TODO: Mostrar al usuario solamente el nombre de los archivos o el texto del
#       enlace guardando en listaFechas
link = listaEnlaces[0]

# Realizar la descarga del archivo
# Crear la dirección de descarga
urlDescarga = url[:url.rfind('/')+1] + link
print(urlDescarga)

# Generar el nombre del archivo
archon = link.split("/")[-1]
print(archon)
# Obtener el archivo de la urlDescarga y guardar en archon
urllib.request.urlretrieve(urlDescarga,archon)
# Se detiene el programa por un segundo para evitar problemas
time.sleep(1)

# # # # # # # # MANIPULACIÓN DEL ARCHIVO # # # # # # # #
# Apertura del archivo usando PANDAS
df = pandas.read_csv(archon)

# Mostrar los 5 primeros registros de la tabla de datos tipo PANDAS
df.head()

# Obtener la lista de estaciones sin que se repitan
df['STATION'].unique().tolist()

# TODO: Obtener todos los datos de manera única donde lo requiera, de los cuales
# esta conformada la tabla de datos