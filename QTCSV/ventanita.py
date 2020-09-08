# -*- coding: utf-8 -*-
import sys

# # #Importar aquí las librerías a utilizar # # #
import pandas as pd
import matplotlib.pyplot as plt

from PyQt5 import uic, QtWidgets, QtCore

# Las librerías que se tienen que importar
import requests                   # Realizar pedidos por medio de la www
import urllib.request             # hacer pedidos utilizando URL
import time
from bs4 import BeautifulSoup     # Manejar páginas web con hipertexto

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

qtCreatorFile = "prueba.ui" # Aquí va el nombre de tu archivo

Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    # Función de inicio de la ventana
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        
        # Controladores
        self.boton1.clicked.connect(self.lerCSV_BS)
        self.boton2.clicked.connect(self.grafica)
        
        # Agregar la ToolBar para graficar
        self.addToolBar(NavigationToolbar(self.MplWidget.canvas, self))
        
    # Métodos de la clase
    def lerCSV_BS(self):
        # Deshabilitar el combobox para evitar errores
        self.combox.setEnabled(False)
        url = 'http://web.mta.info/developers/turnstile.html'
        respuesta = requests.get(url)
        print(respuesta)
        sopa = BeautifulSoup(respuesta.text, "html.parser")
        print(sopa.prettify())
        sopa.findAll('a')
        
        listaEnlaces = []
        for enlace in sopa.findAll('a'):
          tmp = enlace.get('href')
          if(( "txt" in str(tmp) ) and ( "data" in str(tmp) )):
            print( str(tmp) )
            listaEnlaces.append(str(tmp))
        
        # TODO: Se le mostrará al usuario la lista para seleccionar la información
        link = listaEnlaces[0]
        urlDescarga = url[:url.rfind('/')+1] + link
        print(urlDescarga)
        # Cargar directamente de la www
        # TODO: Permitir al usuario seleccionar entre solo leer o descargar el archivo
        self.df = pd.read_csv(urlDescarga)
        # Cargar los datos al combobox
        self.combox.addItems(self.df['STATION'].unique().astype(str).tolist())
        # Habiliar el combobox para su uso
        self.combox.setEnabled(True)
        
    def grafica(self):
        estacion = self.df[self.df["STATION"] == self.combox.currentText()]
        scpfinal = estacion[estacion["SCP"] == "02-00-00"]
        fechas = scpfinal["DATE"].unique().tolist()        
        
        # Limpiar la gráfica
        self.MplWidget.canvas.axes.clear()
        for f in fechas:
          self.MplWidget.canvas.axes.plot( scpfinal[scpfinal["DATE"] == f]["TIME"].tolist(),
          scpfinal[scpfinal["DATE"] == f]["ENTRIES"].tolist() )
        
        self.MplWidget.canvas.axes.set_title("Entries for the station " + scpfinal["STATION"].unique().tolist()[0] + 
                 " using SCP = " + scpfinal["SCP"].unique().tolist()[0] )
        self.MplWidget.canvas.axes.grid()
        self.MplWidget.canvas.axes.set_xlabel("TIME")
        self.MplWidget.canvas.axes.set_ylabel("ENTRIES")
        self.MplWidget.canvas.axes.legend(fechas, loc = 'upper right')
        self.MplWidget.canvas.draw()

# FUNCIÓN MAIN
if __name__ == "__main__":
    app =  QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())