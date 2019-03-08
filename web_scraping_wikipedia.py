import lxml.html as html
import urllib2
import numpy as np
import matplotlib.pyplot as plt
import math

# Fuente: wikipedia

def descargar_pagina(url): 
    parsed = html.parse(urllib2.urlopen(url))
    return parsed.getroot()

def multiple_rest(valor, multiple):
    return valor % multiple

def truncar(s):
    try:
        return int(s)
    except:
        try:
            int(s[0])
            a = 0
            while (a <= (len(s)-1)):
                if ((s[a] == " ") | (s[a] == "+")):
                    return int(s[0:a])
                a = a + 1
            return int(s)
        except:
            return 0

def extraer(doc):
    tabla = doc.find_class("wikitable")
    print("tabla --->", len(tabla), tabla, type(tabla))
    body = tabla[0].findall(".//tbody")
    print("body --->", len(body), body, type(body))
    filas = body[0].findall(".//tr")
    print("filas --->", len(filas))
    array = []
    for f in filas:
	    elements = f.findall(".//td")
	    for e in elements:
	    	array.append(e.text_content().strip())
    return array

def imprimir_tabla(lista):
    a=0
    for i in lista:
	    print i
	    a += 1
	    if (multiple(a,8)):
		    print "******************************************************"

def dias(lista):
    a=0
    d = []
    for i in lista:
        if (multiple_rest(a,8) == 0):
            d.append(i)
        a += 1
    return d

def tipo(lista):
    a=0
    t = []
    for i in lista:
        if (multiple_rest(a,8) == 1):
            t.append(i)
        a = a + 1
    return t

def quien(lista):
    a=0
    t = []
    for i in lista:
        if (multiple_rest(a,8) == 6):
            t.append(i)
        a = a + 1
    return t

def dead(lista):
    a=0
    t = []
    l = []
    for i in lista:
        if (multiple_rest(a,8) == 2):
            t.append(i)
        a = a + 1
    for i in t:
    	num = truncar(i)
        l.append(num)
    return l

def donde(lista):
    a=0
    t = []
    for i in lista:
        if (multiple_rest(a,8) == 4):
            t.append(i)
        a = a + 1
    return t

def count_list(lista):
    count = 0
    for i in range(0, len(lista)):
        count = count + lista[i]
    return len(lista), count

def matriz_quien_dead(list_quien, list_dead):
    dic_quien = {}
    for l in list_quien:
        if ((l in dic_quien) == True):
            dic_quien[l] = (dic_quien.get(l) + 1)
        else:
            dic_quien[l] = 1
    dic_quien_dead = {}
    x = 0
    for i in list_dead:
        if ((list_quien[x] in dic_quien_dead) == True):
            dic_quien_dead[list_quien[x]] = (dic_quien_dead.get(list_quien[x]) + list_dead[x])
        else:
            dic_quien_dead[list_quien[x]] = list_dead[x]
        x = x + 1
    x=0
    m_quien_dead = [['WHO'],['TIMES'],['DEAD']]
    for i in dic_quien:
        for x in range(0,(len(dic_quien)-1)):
            if i in m_quien_dead[0]:
                None
            else:
                m_quien_dead[0].append(i)
                m_quien_dead[1].append(dic_quien.get(i))
                m_quien_dead[2].append(dic_quien_dead.get(i))
    return m_quien_dead

def matriz_donde_dead(list_donde, list_dead):
    dic_donde = {}
    for l in list_donde:
        if (l in dic_donde):
            dic_donde[l] = dic_donde.get(l) + 1
        else:
            dic_donde[l] = 1
    dic_donde_dead = {}
    x = 0
    for l in list_donde:
        if (list_donde[x] in dic_donde_dead):
            dic_donde_dead[list_donde[x]] = (dic_donde_dead.get(list_donde[x]) + list_dead[x])
        else:
            dic_donde_dead[l] = list_dead[x]
        x=x+1
    m_donde_dead = [['WHERE'], ['TIMES'], ['DEAD']]
    for i in dic_donde:
        if (i in m_donde_dead[0]):
            None
        else:
            m_donde_dead[0].append(i)
            m_donde_dead[1].append(dic_donde.get(i))
            m_donde_dead[2].append(dic_donde_dead.get(i))
    return m_donde_dead

def intercambiar(matriz,i,j):
    aux_quien = matriz[0][j]
    matriz[0][j] = matriz[0][i]
    matriz[0][i] = aux_quien

    aux_veces = matriz[1][j]
    matriz[1][j] = matriz[1][i]
    matriz[1][i] = aux_veces

    aux_dead = matriz[2][j]
    matriz[2][j] = matriz[2][i]
    matriz[2][i] = aux_dead

def ordenar_matriz(m_quien_dead):
    frontera = 2
    incremento = len(m_quien_dead[0]) / 2
    # incrementos: 25, 23, 21, 19, 17...
    while (incremento > 0):
        for inicio in range(0,incremento):
            for i in range(inicio+incremento, len(m_quien_dead[0]), incremento):
                posicion = i
                valor_actual = m_quien_dead[2][i]
                while(posicion >= incremento) and (m_quien_dead[2][posicion-incremento]<valor_actual):
                    intercambiar(m_quien_dead,(posicion-incremento),posicion)
        incremento = incremento - 2

def grafica_quien(m, anho, mes):
    plt.title(mes + anho)
    plt.xlabel("numero de atentados")
    plt.barh(m[0][1:16], m[1][1:16])
    plt.show()

def grafica_quien_dead(m, anho, mes):
    plt.title(mes + anho)
    plt.xlabel("numero de muertos")
    plt.barh(m[0][1:16], m[2][1:16])
    plt.show()

def graficas_quien_dead(list_quien, list_dead, anho, mes):## solo llama a las funciones anteriores
    m_quien_dead = matriz_quien_dead(list_quien, list_dead)
    ordenar_matriz(m_quien_dead)
    grafica_quien(m_quien_dead, anho, mes)
    grafica_quien_dead(m_quien_dead, anho, mes)
    for i in range(0,(len(m_quien_dead[0])-1)):
        print(m_quien_dead[0][i],   '  -  '  , m_quien_dead[1][i],   '  -  '   , m_quien_dead[2][i])
    print(len(m_quien_dead[0]))
def graficas_donde_dead(list_donde, list_dead, anho, mes):## solo llama a las funciones anteriores
    m_donde_dead = matriz_donde_dead(list_donde, list_dead)
    ordenar_matriz(m_donde_dead)
    grafica_quien(m_donde_dead, anho, mes)
    grafica_quien_dead(m_donde_dead, anho, mes)

#####################################################################################################################################

def primer_raspado():
    #url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_January_2017'
    #anho=' 2017 '
    #mes=' Enero '
    #url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_February_2017'
    #anho=' 2017 '
    #mes=' Febrero '
    #url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_February_2019'
    #anho=' 2019 '
    #mes=' Febrero '
    url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_1970'
    anho = '1970'
    mes = ' - '
    #url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_March_2019'
    #anho=' 2019 '
    #mes=' Marzo '
    document = descargar_pagina(url)
    lista = extraer(document)
    list_dias = dias(lista)
    #print(list_dias)
    list_tipo = tipo(lista)
    #print(list_tipo)
    list_dead = dead(lista)
    #print(list_dead)
    list_quien = quien(lista)
    #print(list_quien)
    list_donde = donde(lista)
    #print(list_donde)
    print("longitud listas ---> ", len(list_dias), len(list_tipo), len(list_dead), len(list_quien), len(list_donde))
    graficas_quien_dead(list_quien, list_dead, anho, mes)
    graficas_donde_dead(list_donde, list_dead, anho, mes)

######################################################################################################################################

def count_dead_month_year(url):
    document = descargar_pagina(url)
    lista = extraer(document)
    list_dead = dead(lista)
    print(list_dead)
    return count_list(list_dead)

def grafica_month_year_dead(matriz):
    plt.ylabel("numero de victimas")
    pseudomierda = np.arange(len(matriz[0][1:]))
    plt.bar(pseudomierda, matriz[2][1:])
    plt.xticks(pseudomierda, matriz[0][1:])
    plt.show()

def grafica_month_year(matriz):
    plt.ylabel("numero de atentados")
    pseudomierda = np.arange(len(matriz[0][1:]))
    plt.bar(pseudomierda, matriz[1][1:])
    plt.xticks(pseudomierda, matriz[0][1:])
    plt.show()

def segundo_raspado():
    url = 'https://en.wikipedia.org/wiki/List_of_terrorist_incidents_in_'
    list_month = ['January_', 'February_', 'March_', 'April_', 'May_', 'June_', 'July_', 'August_', 'September_', 'October_',
    'November_', 'December_']
    list_years = ['2015', '2016', '2017', '2018', '2019']
    list_month_grafic = ['E', 'F', 'MR', 'AB', 'MY', 'JN', 'JL', 'AG', 'S', 'O', 'N', 'D']
    matriz = [['Year-Month'], ['TIMES'],['DEAD']]
    for i in list_years:
        x=0
        for j in list_month:
            if ((i == '2019') and (j == 'April_')):
                print("LLegamos a la fecha actual")
                break 
            urli = url+j+i
            print('urli ---> ', urli)
            times, count = count_dead_month_year(urli)
            if j == 'January_':
                matriz[0].append(list_month_grafic[x]+i[2:])
            else:
                matriz[0].append(list_month_grafic[x])
            matriz[1].append(times)
            matriz[2].append(count)
            x=x+1
    for i in range(0,(len(matriz[0])-1)):
        print(matriz[0][i],   '  -  '  , matriz[1][i],   '  -  '   , matriz[2][i])
    grafica_month_year(matriz)
    grafica_month_year_dead(matriz)

primer_raspado()

segundo_raspado()














