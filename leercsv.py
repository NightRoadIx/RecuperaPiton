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

# DESCARGA DE DATOS
# Requerir de una URL
url = 'http://web.mta.info/developers/turnstile.html'

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