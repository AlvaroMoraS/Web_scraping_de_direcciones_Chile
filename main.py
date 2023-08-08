import requests
from bs4 import BeautifulSoup
import pandas as pd
import time #lo usaremos para luego dar segundos entre cada consulta.
import csv

df = pd.read_csv('rut.csv', thousands='.' , sep="|", decimal=",") #con este script leo el csv, con separador de miles con puntos, decimales con comas, y seprador de columnas con pipe '|'
df['rut'] = df['rut'].map('{:,}'.format).str.replace(",", "~").str.replace(".", ",") .str.replace("~", ".") #con esto, reemplazaré el formato de de separador de miles a puntos, sin decimales.

df['rutDV'] = df['rut'].map(str) + '-' + df['dv'].map(str) #con este script concateno el RUT y el DV, con el formato xx.xxx.xxx-Y


def extractor(rut):
  response = requests.get('https://www.nombrerutyfirma.com/rut?term=' + rut)
  html = BeautifulSoup(response.text, 'html.parser')
  td_html = html.find_all('td') #esto busca todos los tag con "td" en la página web.
  calle = list()
  for i in td_html:
    calle.append(i.text)
  
  if bool(calle) == False:
    calle=['','','','','']
  
  direccionCalle = calle[3] #valor de la calle
  comunaCiudad = calle[4] #valor de la comuna
  time.sleep(3) #doy 3 segundos de tiempo.

  return direccionCalle + '|' + comunaCiudad #envío la calle y la comuna juntas, separadas por un pipe '|'
  #print(calle[3])

df['direccion|comuna'] = df['rutDV'].apply(extractor) #con este script ejecutamos las consultas

df[['calle', 'comuna']] = df['direccion|comuna'].str.split('|', 1, expand=True) #esto divide la columna "direccion|comuna" en dos columnas apartes: calle y comuna
del(df['direccion|comuna']) #esto borra la columna "direccion|comuna", ya que ya la dividimos en el paso anterior en 2 columnas
df.to_csv('resultadoConsultas.csv', index=False, sep='|', encoding='utf-8') #esto exporta a CSV el resultado, con separador |, y encodeado con UTF-8.