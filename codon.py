#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:48:17 2017

@author: jmcamza
"""

import requests
import re
host_url="http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=83333&aa=1&style=N"
native_url="http://www.kazusa.or.jp/codon/cgi-bin/showcodon.cgi?species=29760&aa=1&style=N"
sequence1="UAGGCGCCGGCAACGCAG"
"""his code processes the input html to generate a codon table as a dictionary"""

def url_process(url):
    r=requests.get(url)
    text=r.text
    texto1=text[text.find("<PRE>")+5:text.find("</PRE>")]
    texto2=texto1.replace("\n","")
    texto3=re.sub("[\(\[].*?[\)\]]","\n", texto2)
    texto4=texto3.replace("\n  ","\n")
    texto5=texto4.split("\n")
    for x in range(len(texto5)):
        texto5[x]=texto5[x][0:-6]
        texto5[x]=texto5[x].replace("  ","")
        texto5[x]=texto5[x].replace(" ",",")
    texto5=texto5[0:-1]
    for x in range(len(texto5)):
        texto5[x]=texto5[x].split(",")
    my_dict={}
    for i in range(len(texto5)):
        my_dict[texto5[i][0]]=texto5[i]
    return my_dict

#host=url_process(host_url)
#native=url_process(native_url)
#lista=url_process(native_url)
#flotante=float(lista["AAA"][2])
#print(flotante)

"""This code compares two codon tables (dictionaries) generated with the url_process function
and generates a new replacement table (dictionary) according to the inputs.

"""

def replacement(host,native):
    host_dict=url_process(host_url)
    native_dict=url_process(native_url)
    dif_dict={}
    for i in host_dict:
        for j in native_dict:
            if host_dict[i][1]==native_dict[j][1]: #si el aminoácido es el mismo, sacar la diferencia y guardar en nuevo diccionario dif_dict
                dif_dict[native_dict[j][0],host_dict[i][0]]=[native_dict[j][0],host_dict[i][0],native_dict[j][1],host_dict[i][1],abs(float(native_dict[j][2])-float(host_dict[i][2]))]
            else:
                continue
    #return dif_dict
    new_table={}
    for h in dif_dict:
        for k in dif_dict:
            if h!=k:        #Si el par de codones es distinto
                if dif_dict[h][4]==0.00:    #Si la diferencia es cero, guardar el par de codones en la new_table de reemplazo
                    new_table[dif_dict[h][0]]=[dif_dict[h][0],dif_dict[h][1],dif_dict[h][3],dif_dict[h][4]]
                else:
                    for m in list(new_table):
                        if dif_dict[h][0] == new_table[m][0]:#Si el codon ya está en el nuevo diccionario, saltar
                            continue
                        else:
                            if dif_dict[h][4]==dif_dict[k][4]:#si la diferencia es la misma, poner el primero
                                new_table[dif_dict[h][0]]=[dif_dict[h][0],dif_dict[h][1],dif_dict[h][3],dif_dict[h][4]]
                            elif float(dif_dict[h][4])<float(dif_dict[k][4]):#si la diferencia del primero es menor poner el primero
                                new_table[dif_dict[h][0]]=[dif_dict[h][0],dif_dict[h][1],dif_dict[h][3],dif_dict[h][4]]
                            else:# si es mayor la dif del primero entonces poner el segundo.
                                new_table[dif_dict[k][0]]=[dif_dict[k][0],dif_dict[k][1],dif_dict[k][3],dif_dict[k][4]]
                for n in list(new_table):
                    if dif_dict[h][4]==dif_dict[k][4]:
                        continue
                    elif float(dif_dict[h][4])<float(dif_dict[k][4]):#si la diferencia del primero es menor poner el primero
                        new_table[dif_dict[h][0]]=[dif_dict[h][0],dif_dict[h][1],dif_dict[h][3],dif_dict[h][4]]
                    else:# si es mayor la dif del primero entonces poner el segundo.
                        new_table[dif_dict[k][0]]=[dif_dict[k][0],dif_dict[k][1],dif_dict[k][3],dif_dict[k][4]]
            else:
                continue
    return new_table
                    


def change(sequence,host,native):
    a=0
    b=3
    seq=sequence
    new_table=replacement(host,native)
    new=""
    while b <= len(seq):
        new+=new_table[seq[a:b]][1]
        a=a+3
        b=b+3
    return new         
                    
                          
replace3=replacement(host_url,native_url)
new_sequence=change(sequence1,host_url,native_url)
sequence1[0:3]
replace3[sequence1[0:3]][1]
