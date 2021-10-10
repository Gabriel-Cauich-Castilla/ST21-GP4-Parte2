# -*- coding: utf-8 -*-
"""
Spyder Editor

Proyecto de Analisis de datos
"""

# Función para extraer valores de un diccionario
def valor_diccionario(dic,):
    return dic["valor"]

def lista_longitud(n,):
    lista = []
    for i in range(n):
        lista.append(0)
    return lista

# Función para unir dos listas del mismo tamaño

def unir_listas(lista1,lista2,):
    tamano_listas = len(lista1)
    # Lista en la que se unirán las listas
    arreglo = []
    for i in range(tamano_listas): 
        arreglo.append({"llave":lista1[i],"valor":lista2[i]})
    return arreglo


# Funcion para eliminar duplicados
def consolidar(lista1):
    lista1_conjunto = set(lista1)
    lista_nueva = list(lista1_conjunto)
    lista_nueva.sort()
    return lista_nueva

# Funcion para crear tablas de totales con base en una lista 

def tabla_totales(lista1):
    tamaño_lista = len(lista1)
    totales = lista_longitud(tamaño_lista)
    tabla = unir_listas(lista1,totales)
    return tabla
    

# Se agrega el módulo csv para leer la base de datos en modo lectura
import csv

# Se agregan las listas para las rutas de importación y exportación

rutas_origen_destino = []
paises = []
medios = []
montos =[]


# ANALISIS DE RUTAS 
# Se abre el archivo 

with open("synergy_logistics_database.csv","r",encoding='utf-8-sig') as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    
    # Se generan las rutas de origen y destino 
    for linea in lector:
        rutas_origen_destino.append(linea["origin"]+" - "+linea["destination"])
        paises.append(linea["origin"])
        medios.append(linea["transport_mode"])
        montos.append(int(linea["total_value"]))
        

# Se calcula el número de registros
num_registros=len(rutas_origen_destino)

# Se usa la función "consolidar" para crear los catálogos de rutas, países y
# medios de transporte

rutas = consolidar(rutas_origen_destino)
medios = consolidar(medios)
paises = consolidar(paises)

# Se generan las estructuras para acumular el número y monto de las operaciones
operaciones_ruta = tabla_totales(rutas)
totales_medios = tabla_totales(medios)
totales_pais = tabla_totales(paises)


with open("synergy_logistics_database.csv","r",encoding='utf-8-sig') as archivo_csv:
    lector = csv.DictReader(archivo_csv)
    
    # Se recorre el archivo línea por línea
    for linea in lector:
        # Se extrae la información a utilizar
        ruta = linea["origin"]+" - "+linea["destination"]
        medios = linea["transport_mode"]
        pais = linea["origin"]
        monto = int(linea["total_value"])
        
        # Se acumulan las operaciones por ruta
        for index in range(len(operaciones_ruta)):
            if operaciones_ruta[index]["llave"] == ruta:
                operaciones_ruta[index]["valor"]+=1
                
        # Se acumula el monto de las operaciones por medio
        for index in range(len(totales_medios)):
            if totales_medios[index]["llave"] == medios:
                totales_medios[index]["valor"]+=monto
                
        # Se acumula el monto de las operaciones por país
        for index in range(len(totales_pais)):
            if totales_pais[index]["llave"] == pais:
                totales_pais[index]["valor"]+= monto
                


# Se ordena la tabla de totales por operación y se reporta el top 10 

operaciones_ruta.sort(key=valor_diccionario,reverse=True)       

print("Top 10 rutas más demandadas: \n" )
print("Ruta : Operaciones")
operaciones_totales_top10 = 0
for valor in range(10):
    operaciones_totales_top10 += operaciones_ruta[valor]["valor"]
    print(str(valor +1)+
          "."+operaciones_ruta[valor]["llave"]+
          ": "+str(operaciones_ruta[valor]["valor"]))    

print("\nEl top 10 de rutas concentra el "+
      str(100*operaciones_totales_top10//num_registros)+"% "+
      "de las operaciones")

# Se ordena la tabla de montos y se reportan los porcentajes de participación

totales_medios.sort(key=valor_diccionario,reverse=True)       


print(" \nMontos de operación por medio de transporte: \n" )
print("Medio : Monto : %")

# Se calcula el monto total de las operaciones para reportar los porcentajes
monto_total = sum(montos)

for valor in range(len(totales_medios)):
    print(str(valor +1)+
          "."+totales_medios[valor]["llave"]+
          ": "+str(totales_medios[valor]["valor"])+" : "+
          str(100*totales_medios[valor]["valor"]//monto_total))   


totales_pais.sort(key=valor_diccionario,reverse=True)     

# Se inician los criterios que validarán la suma del 80% y que recorrerán
# los índices
suma_acumulada = 0
index = 0
print(" \nPorcentajes de operación por país: Top 80% \n" )
print("País: %")
while suma_acumulada < 0.8*monto_total:
    print(str(index+1)+"."+totales_pais[index]["llave"]+" : "+
          str(100*totales_pais[valor]["valor"]//monto_total))
    suma_acumulada+=totales_pais[valor]["valor"]
    index+=1



