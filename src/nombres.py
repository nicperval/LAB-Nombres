import csv
from collections import namedtuple
from collections import defaultdict
from matplotlib import pyplot as plt

def leer_frecuencias_nombres(ruta):
    with open (ruta, encoding='utf-8') as f:
        FrecuenciaNombre = namedtuple('FrecuenciaNombre', 'año,nombre,frecuencia,genero')
        fichero = csv.reader(f)
        next(fichero)
        lista = []
        for año,nombre,frecuencia,genero in fichero:
            año = int(año)
            frecuencia = int(frecuencia)
            FrecuenciaNombre = (año,nombre,frecuencia,genero)
            lista.append(FrecuenciaNombre)
        return lista

def filtrar_por_genero(lista,genero):
    FrecuenciaNombre = namedtuple('FrecuenciaNombre', 'año,nombre,frecuencia,genero')
    listagen = []
    for año,nombre,frecuencia,gen in lista:
        if genero == gen:
            FrecuenciaNombre = (año,nombre,frecuencia,gen)
            listagen.append(FrecuenciaNombre)
    if len(listagen) == 0:
        listagen = lista
    return listagen

def calcular_nombres(lista,genero):
    conjunto = set()
    for año,nombre,frecuencia,gen in lista:
        if genero == gen:
            conjunto.add(nombre)
    if len(conjunto) == 0:
        for año,nombre,frecuencia,gen in lista:
            conjunto.add(nombre)
    return conjunto

def calcular_top_nombres_de_año(lista,fecha,lim,genero):
    lis = []
    lisdtup = []
    filtro = filtrar_por_genero(lista,genero)
    for año,nombre,frecuencia,gen in filtro:
        if año == fecha:
            tupla = (año,nombre,frecuencia,gen)
            lis.append(tupla)
    ordenado = sorted(lis, key=lambda filtro: filtro[2])
    ordenado.reverse()
    for año,nombre,frecuencia,gen in ordenado:
        tupla = (nombre,frecuencia)
        lisdtup.append(tupla)
        if len(lisdtup) == lim:
            break
    return lisdtup

def calcular_nombres_ambos_generos(lista):
    lis=[]
    masc = calcular_nombres(lista,'Hombre')
    fem = calcular_nombres(lista,'Mujer')
    for i in masc:
        if i in fem:
            lis.append(i)
    return lis

def calcular_nombres_compuestos(lista,genero):
    nombres = calcular_nombres(lista,genero)
    lis = []
    for i in nombres:
        if ' ' in i:
            lis.append(i)
    return lis

def calcular_frecuencia_media_nombre_años(lista,nom,ai,af):
    Rangoaño = []
    for año,nombre,frecuencia,genero in lista:
        if año in range(ai,af):
            tupla = (año,nombre,frecuencia,genero)
            Rangoaño.append(tupla)
    Frecuencias = []
    for año,nombre,frecuencia,genero in Rangoaño:
        if nombre == nom:
            Frecuencias.append(frecuencia)
    if len(Frecuencias) == 0:
        media = 0
    else:
        media = sum(Frecuencias)/len(Frecuencias)
    return media

def calcular_nombre_mas_frecuente_año_genero(lista,año,genero):
    filtrar = calcular_top_nombres_de_año(lista,año,1,genero)
    return filtrar

def calcular_año_mas_frecuencia_nombre(lista,nombre):
    lis = []
    for año,nom,frecuencia,genero in lista:
        if nombre == nom:
            tupla = (año,frecuencia)
            lis.append(tupla)
    ordenado = sorted(lis, key=lambda filtro: filtro[1])
    ordenado.reverse()
    return ordenado[0][0]

def calcular_nombres_mas_frecuentes(lista,genero,decada,n):
    if n == '':
        n = 5
    filgen = filtrar_por_genero(lista,genero)
    lis = []
    y = 0
    for año,nombre,frecuencia,genero in filgen:
            tupla = (nombre,calcular_frecuencia_media_nombre_años(filgen,nombre,decada,decada+10))
            lis.append(tupla)
    suma_contador = defaultdict(lambda: [0, 0])

    for cadena, valor in lis:
        suma_contador[cadena][0] += valor 
        suma_contador[cadena][1] += 1      

    junto = [(cadena, suma / contador) for cadena, (suma, contador) in suma_contador.items()]
        
    ordenado = sorted(junto,key=lambda filtro: filtro[1])
    ordenado.reverse()
    res = []
    x = 0
    while len(res)<n:
        res.append(ordenado[x])
        x += 1
    return res

def calcular_año_frecuencia_por_nombre(lista,genero):
    filtro = filtrar_por_genero(lista,genero)
    nombres = []
    diccionario = {}
    for año,nombre,frecuencia,genero in filtro:
        if nombre not in nombres:
            nombres.append(nombre)
    for i in nombres:
        lis = []
        for año,nombre,frecuencia,genero in filtro:
            if i == nombre:
                tupla = (año,frecuencia)
                lis.append(tupla)
        diccionario[i] = lis
    return diccionario
        
def calcular_nombre_mas_frecuente_por_año(lista,genero):
    lis = []
    año = 2002
    while año <= 2017:
        valores = calcular_top_nombres_de_año(lista,año,1,genero)
        tupla = (año,valores[0][0],valores[0][1])
        lis.append(tupla)
        año += 1
    return lis

def calcular_frecuencia_por_año(lista,nombre):
    frecuencias = {}
    for año, nom, frecuencia, genero in lista:
        if nombre == nom:
            if año not in frecuencias:
                frecuencias[año] = 0
            frecuencias[año] += frecuencia
    return [(año, frec) for año, frec in frecuencias.items()]

def mostrar_evolucion_por_año(lista,nombre):
    frecporaño = calcular_frecuencia_por_año(lista,nombre)
    años = []
    frecuencias = []
    for año,frecuencia in frecporaño:
        años.append(año)
        frecuencias.append(frecuencia)
    plt.plot(años, frecuencias)
    plt.title("Evolución del nombre '{}'".format(nombre))
    plt.show()

def calcular_frecuencias_por_nombre(lista):
    dicc = {}
    for año,nombre,frecuencia,genero in lista:
        if nombre not in dicc:
            dicc[nombre] = 0
        dicc[nombre] += frecuencia
    return dicc

def mostrar_frecuencias_nombres(lista,lim):
    diccionario = calcular_frecuencias_por_nombre(lista)
    lis = [(nombre, frec) for nombre, frec in diccionario.items()]
    nombres = []
    frecuencias = []
    if lim == '':
        lim = 10
    for nombre,frec in lis:      
        nombres.append(nombre)
        frecuencias.append(frec)
        if len(nombres) == 10:
            break
    plt.bar(nombres, frecuencias)
    plt.xticks(rotation=80)
    plt.title("Frecuencia de los {} nombres más comunes".format(lim))
    plt.show()
    