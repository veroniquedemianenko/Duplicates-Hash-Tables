import matplotlib.pyplot as plt

import string
from math import floor, sqrt

# Ouverture des fichiers

shake = open(r"/Users/veroniquedemianenko/Desktop/bigdata/tp1/texte_Shakespeare.txt", 'r')
shake = shake.readlines()
shake = [mot.strip() for mot in shake]  # On supprime les '\n' marquant le saut de ligne

corn = open(r"/Users/veroniquedemianenko/Desktop/bigdata/tp1/corncob_lowercase.txt", 'r')
corn = corn.readlines()
corn = [mot.strip() for mot in corn]

# On travaille dans ce TP sur le document texte_Shakespeare et corncob_lowercase


alphabet = list(string.ascii_lowercase)
alphabet.append('-')
utf8_alphabet = [ord(letter) for letter in alphabet]

print('Nombre de lignes:', len(shake), len(corn))





M = max(len(shake), len(corn))*3

# M n'est pas premier donc on prend le nombre premier suivant

# Ici on prend

M=58111


# Fonction de hachage par division

def emilie_veronique_hachagediv(mot,M):
    mot = list(mot.lower())
    nombre = 0
    for i in range(len(mot)):
        indice = utf8_alphabet[alphabet.index(mot[i])]
        nombre += indice*(26**(len(mot)-i-1))
    h = nombre%M
    return h



# Fonction de hachage par multiplication

A = ( sqrt(5) - 1 ) / 2

def emilie_veronique_hachagemult(mot,M):
    mot = list(mot)
    nombre = 0
    for i in range(len(mot)):
        indice = alphabet.index(mot[i])
        nombre += indice*(26**(len(mot)-i-1))
    h = floor( M * (nombre * A - floor(nombre *A) ) )
    return h



# Hachage par adressage fermé

def hash_ferme(shake, corn, M):
    table_hachage = [ [] for i in range(M)]
    for mot in shake:
        indice = emilie_veronique_hachagediv(mot,M)
        table_hachage[indice].append(mot)

    for mot in corn:
        indice = emilie_veronique_hachagediv(mot,M)
        table_hachage[indice].append(mot)
    return table_hachage



# Hachage par adressage ouvert


M2 = 243073  # vu qu'on ajoute tous les élements à la liste, on a au pire tout le temps des collisions, donc on fait : len(shake)+len(corn). On multiplie par 3 pour avoir un taux de remplissage de 30%, et on prend le premier nombre premier qui suit ce résultat.

# Nous avons testé deux façons de faire le hachage par adressage ouvert : par sondage linéaire et par double hachage.

def hash_ouvert_lineaire(shake, corn, M2):
    table_hachage = [0]*M2
    for mot in shake:
        indice = emilie_veronique_hachagediv(mot,M2)
        while table_hachage[indice]!= 0 :
            indice = (indice + 1)%M2
        table_hachage[indice]=mot

    for mot in corn:
        indice = emilie_veronique_hachagediv(mot,M2)
        while table_hachage[indice]!= 0 :
            indice = (indice + 1)%M2
        table_hachage[indice]=mot
    return table_hachage



def hash_ouvert_double(shake,corn,M2):
    table_hachage = [0]*M2
    for mot in shake:
        i=0
        indice_double= emilie_veronique_hachagediv(mot,M2)
        indice_div= indice_double
        indice_mult = emilie_veronique_hachagemult(mot,M2)

        while table_hachage[indice_double]!= 0 :
            indice_double = (indice_mult+i*indice_div)%M2  #c'est la fonction du cours h(x,i)=(h1(x)+i*h2(x))modM
            i+=1
        table_hachage[indice_double]=mot

    for mot in corn:
        i=0
        indice_double= emilie_veronique_hachagediv(mot,M2)
        indice_div= indice_double
        indice_mult = emilie_veronique_hachagemult(mot,M2)

        while table_hachage[indice_double]!= 0 :
            indice_double = (indice_mult+i*indice_div)%M2
            i+=1
        table_hachage[indice_double]=mot
    return table_hachage





def intersection_ouvert(shake, corn): #attention espace mémoire linéaire
    M2=243073

    table_hachage_ouvert=hash_ouvert_double(shake, corn, M2) #ou utiliser hash_ouvert_double
    mots_en_double = set()
    mots_vus = set()
    for mot in table_hachage_ouvert:
        if mot != 0:
            if mot in mots_vus:
                mots_en_double.add(mot)
            else:
                mots_vus.add(mot)
    return list(mots_en_double)




def intersection_ferme(shake,corn): # les mots en double devraient se trouver dans une seule et même liste de la table de hachage, et non pas dans deux différentes.
    M=58111
    table_hachage_ferme=hash_ferme(shake,corn,M)
    mots_en_double= set()
    mots_vus = set()
    for liste in table_hachage_ferme:
        for mot in liste:
            if mot != 0:
                if mot in mots_vus:
                    mots_en_double.add(mot)
                else:
                    mots_vus.add(mot)
    print(len(mots_en_double))
    return list(mots_en_double)

# 15759 pour intersection fermé et ouverts !






