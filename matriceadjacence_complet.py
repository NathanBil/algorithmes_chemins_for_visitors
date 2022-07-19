#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import copy
"""Implémentation d'un graphe à l'aide d'une matrice d'adjacence. Les n sommets
sont identifiés par de simples naturels (0, 1, 2, ..., n-1)."""


class AreteErronee(Exception):
    """Exception raised for errors in the input iterable.

    Attributes:
        erreur -- message d'erreur explicatif
    """

class MatriceAdjacence(object):
    def __init__(self, num=0):
        """Initialise un graphe sans arêtes sur num sommets.

        >>> G = MatriceAdjacence()
        >>> G._matrice_adjacence
        []
        """
        self._matrice_adjacence = [[0] * num for _ in range(num)]
        
       
    def ajouter_arete(self, source, destination):
        """Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_arete(1,1)
        >>> g1.ajouter_arete(1,2)
        >>> g1._matrice_adjacence
        [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
        """
        
        #cas où le user a entré des valeurs interdites on sort
        if source < 0 or destination < 0:
            print("Vous avez entré une valeur inférieure à 0, le programme s'arrête")
            return 
        
        if(len(self._matrice_adjacence)-1 < destination or len(self._matrice_adjacence)-1 < source):
            #variable qui contient le nombre de 0 (donc de sommet) à ajouter dans chaque liste en plus
            #on récupère le plus grand nombre entre la source et la destination pour savoir les 0 à ajouter
            increase = max([source, destination]) - (len(self._matrice_adjacence)-1)
            #contient le numéro du sommet ayant la plus grande valeur dans la liste
            maximum = max([source, destination])
            #on ajoute les cases manquantes aux sommets qui étaient déjà présents
            for liste in self._matrice_adjacence:
                i = 0
                while(i < increase):
                    liste.append(0)
                    i+=1
            #on ajoute les nouveaux sommets avec leurs cases
            while(increase > 0):
                self._matrice_adjacence.append([0]*(maximum+1))
                increase-=1
    #on va à l'emplacement associé à la liste source et on ajoute à l'emplacement associé au sommet 
    #destination le numéro 1.
        self._matrice_adjacence[source][destination] = 1
    #comme le graphe est non-orienté on fait la même chose de la destination vers la source
        self._matrice_adjacence[destination][source] = 1


    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1._matrice_adjacence
        [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes({(1,1),(1,2)}) 
        >>> g1._matrice_adjacence
        [[0, 0, 0], [0, 1, 1], [0, 1, 0]]
        """
        #on récupère chaque couple de sommet et on s'assure qu'il n'y a pas de valeurs négatives parmi eux
        # si il y y en a une on arrête tout
        for couple in iterable:
            if couple[0] < 0 or couple[1] < 0:
                print("Vous avez entré une valeur inférieure à 0, le programme s'arrête")
                return 
        #on récupère chaque couple de sommet et on applique la fonction ajouter arete avec les deux sommets
        for couple in iterable:
            self.ajouter_arete(couple[0], couple[1])
            

    def ajouter_sommet(self):
        """Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = MatriceAdjacence()
        >>> G.ajouter_sommet()
        0
        >>> G._matrice_adjacence
        [[0]]
        >>> G.ajouter_sommet()
        1
        >>> G._matrice_adjacence
        [[0, 0], [0, 0]]
        """
        #variable qui contient le nombre de 0 (donc de sommet) à ajouter dans chaque liste en plus
        #on augmentera de 1 la taille du graphe
        increase = 1
        #contient le numéro du sommet ayant la plus grande valeur dans la liste
        maximum = len(self._matrice_adjacence)
        #on ajoute les cases manquantes aux sommets qui étaient déjà présents
        for liste in self._matrice_adjacence:
            i = 0
            while(i < increase):
                liste.append(0)
                i+=1
        #on ajoute les nouveaux sommets avec leurs cases initialisées à 0
        while(increase > 0):
            self._matrice_adjacence.append([0]*(maximum+1))
            increase-=1

        return maximum
    
    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u)).
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1.aretes()
        [(1, 2)]
        
        """
        #liste qui contient le résultat final
        res = []
        #variable qui contient le sommet traité actuellement
        sommet = 0
        #pour chaque liste de la matrice on regarde les éléments
        for liste in self._matrice_adjacence:
            for i in range(0,len(liste)):
        #si le sommet "liste" (de numéro "sommet") est relié au sommet i (liste[i] == 1) alors on ajoute le couple
                if liste[i] == 1:
                    #on ajoute le couple ssi il n'est pas déjà dans la liste mais dans l'ordre inverse
                    if((i, sommet) not in res and (i != sommet)):
                        res.append((sommet,i))
        #on met à jour la valeur du sommet
            sommet+=1
        #on renvoie les couples
        return res
    
    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1.boucles()
        [(1, 1)]
        
        """
        #liste qui contient le résultat final
        res = []
        #variable qui contient le sommet traité actuellement
        sommet = 0
        #pour chaque liste de la matrice on regarde les éléments
        for liste in self._matrice_adjacence:
            for i in range(0,len(liste)):
        #si le sommet "liste" (de numéro "sommet") est relié au sommet i (liste[i] == 1) alors on ajoute le couple
                if liste[i] == 1:
                    #on ajoute le couple ssi il n'est pas déjà dans la liste mais dans l'ordre inverse
                    if((i, sommet) not in res and (i == sommet)):
                        res.append((sommet,i))
        #on met à jour la valeur du sommet
            sommet+=1
        #on renvoie les couples
        return res

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1.contient_arete(1,1)
        True
        >>> g1.contient_arete(1,2)
        True
        >>> g1.contient_arete(1,8)
        False
        """
        #cas où le user a entré des valeurs interdites on renvoie false
        if u < 0 or v < 0:
            return False
        #cas où on cherche une boucle
        if(u == v):
            #return False
            couple = self.boucles()
            if((u,v) in couple):
                return True
            else:
                return False
        else:
            couple = self.aretes()
            if((u,v) in couple or (v,u) in couple):
                return True
            else:
                return False
            
    def contient_sommet(self, u):
        """Renvoie True si le sommet (u) est existe. False sinon.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1.contient_sommet(1)
        True
        >>> g1.contient_sommet(2)
        True
        >>> g1.contient_sommet(8)
        False
        """
        #cas où le user a entré des valeurs interdites on renvoie
        if u < 0:
            return False
        #on regarde la taille de la liste pour savoir si le sommet y est
        #si la taille de la liste-1 est de taille supérieure ou égale au numéro du sommet alors oui
        if(len(self._matrice_adjacence)-1 >= u):
            return True
        #si la taille de la liste est de taille inférieure ou égale au numéro du sommet alors non
        else:
            return False

    def degre(self, sommet):
        """Renvoie le degré d'un sommet, c'est-à-dire le nombre de voisins
        qu'il possède.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2]]) 
        >>> g1.degre(1)
        2
        >>> g1.degre(2)
        1
        >>> g1.degre(8)
        0
        
        """
        #cas où le user a entré des valeurs interdites on renvoie 0
        if sommet < 0:
            print("le sommet que vous avez entré n'existe pas car il est négatif")
            return 0
        
        #variable qui contient le nombre de voisin du sommet
        voisin = 0
        #on récupère la sous-liste liste que l'on doit traiter en regardant l'emplacement 
        #"sommet" de self._matrice_adjacence
        if(sommet > len(self._matrice_adjacence)-1):
            return voisin
        liste = self._matrice_adjacence[sommet]
        for i in range(0,len(liste)):
        #si le sommet "liste" (de numéro "sommet") est relié au sommet i (liste[i] == 1) alors pn incrémente
        #de 1 le nombre de sommet voisins
            if liste[i] == 1:
        #on ajoute le couple ssi il n'est pas déjà dans la liste mais dans l'ordre inverse
                voisin+=1
        #on renvoie voisin (le nombre de voisin)
        return voisin

    def nombre_aretes(self):
        """renvoie le nombre total d'arète du graphe
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,9]]) 
        >>> g1.nombre_aretes()
        2
        """
        #on récupère l'ensemble des arêtes
        liste = self.aretes()
        #le nombre d'arête correspond au nombre de liste : c'est ce que l'on renvoie
        return len(liste)
        

    def nombre_boucles(self):
        """renvoie le nombre total d'arète du graphe
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,9]]) 
        >>> g1.nombre_boucles()
        1
        """
        #on récupère l'ensemble des boucles
        liste = self.boucles()
        #le nombre de boucle correspond au nombre de liste : c'est ce que l'on renvoie
        return len(liste)
    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe.

        >>> from random import randint
        >>> n = randint(0, 1000)
        >>> MatriceAdjacence(n).nombre_sommets() == n
        True
        """
        return len(self._matrice_adjacence)

    def retirer_arete(self, u, v):
        """retire l'arète qui a pour sommet le couple {u,v}
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,3]]) 
        >>> g1.retirer_arete(1,1)
        >>> g1._matrice_adjacence
        [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0]]
        >>> g1.retirer_arete(2,3)
        >>> g1._matrice_adjacence
        [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        """
        #cas où un sommet est inférieur à 0, il n'existe pas donc on sort
        if(u < 0 or v < 0):
            msg = "Erreur ce numéro d'arète n'existe pas: ("+ str(u) + "," + str(v) + ") : les nombres négatifs sont interdits"
            raise AreteErronee(msg)
        # on s'assure que la liste est de la bonne taille et qu'elle contient effectivement l'arète demandée
        if((len(self._matrice_adjacence)-1 >= max(u,v)) and self.contient_arete(u, v)) == True:
            #on regarde la liste numéro "u" (qui correspond au sommet u) et pour l'élément numéro "v"
            #(qui correspond au sommet "v") et on met un "0"
             #si elle est trop petite, on provoque volontairement une erreur
            self._matrice_adjacence[u][v] = 0
            self._matrice_adjacence[v][u] = 0
        #si l'arète n'existe pas, on provoque volontairement une erreur
        else:
            msg = "Erreur ce numéro d'arète n'existe pas : ("+ str(u) + "," + str(v) + ")"
            raise AreteErronee(msg)
            
    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,3]]) 
        >>> g1.retirer_aretes(((1,1), (2,3)))
        >>> g1._matrice_adjacence
        [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes({(1,1),(1,2), (2,3)}) 
        >>> g1.retirer_aretes({(1,1), (2,3)})
        >>> g1._matrice_adjacence
        [[0, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 0]]
        """
        #on regarde chaque liste de l'iterable 
        #on retire les arètes associées aux sommets en utilisant la fonction "safe"
        #cas où on a une valeur négative on arrête tout
        for liste in iterable:
            if(liste[0] < 0 or liste[1] < 0):
                print("Il y a une valeur négative, on arrête tout")
                return 
        #on regarde chaque liste de l'iterable 
        #on retire les arètes associées aux sommets en utilisant la fonction "safe"
        for liste in iterable:
            self.retirer_arete(liste[0], liste[1])
            
    def voisins(self, sommet):
        """Renvoie la liste des voisins d'un sommet.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,3]]) 
        >>> g1.retirer_aretes(((1,1), (2,3)))
        >>> g1.voisins(0)
        []
        >>> g1.voisins(2)
        [1]
        >>> g1.ajouter_aretes([[1,1],[1,2],[2,3]]) 
        >>> g1.voisins(2)
        [1, 3]
        """
        #cas où le sommet traité est inférieur à 0, il n'existe pas donc on sort
        if(sommet < 0):
            print("Un des nombres est inférieur à 0 donc on ne peut pas créer des graphes")
            return 
        #on récupère toutes les arètes
        liste = self.aretes()
        #on ajoute toutes les boucles
        for e in self.boucles():
            liste.append(e)
        res = []
        #on regarde chaque liste d'arète
        #si elle contient le nom du sommet alors on affiche le nom du deuxième sommet
        for sslist in liste:
            if sommet in sslist:
                #si le sommet est le premier élément de la sous-liste alors on ajoute le deuxième
                if(sommet == sslist[0]):
                    res.append(sslist[1])
                #si le sommet est le deuxième élément de la sous-liste alors on ajoute le premier
                else:
                    res.append(sslist[0])
        
        liste = self.boucles()
        return res
        
    #pb quand on retire le sommet numéro 0 est-ce que les autres sommets sont tous décalés de -1 vers la gauche
    #en d'autres termes est-ce que ça change la numérotation ? Ou ça crée un emplacement vide ?
    #
    def retirer_sommet(self, sommet):
        """Déconnecte un sommet du graphe et le supprime.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,2], [1,1]])
        >>> g1.retirer_sommet(0)
        >>> g1._matrice_adjacence
        [[1, 1], [1, 0]]
        """
        if(sommet < 0):
            printf("erreur ce sommet n'existe pas")
            return
        if(sommet > len(self._matrice_adjacence)-1):
            print("erreur : ce sommet n'existe pas")
            return
        #pour chaque sous liste on va retirer l'emplacement associé au sommet
        for liste in self._matrice_adjacence:
            del liste[sommet]
        #on retire le sommet de la liste
        del self._matrice_adjacence[sommet]
        
      
    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,2], [1,1]])
        >>> g1.retirer_sommets([1,0])
        >>> g1._matrice_adjacence
        [[0]]
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,2], [1,1]])
        >>> g1.retirer_sommets([0,1])
        >>> g1._matrice_adjacence
        [[0]]
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes(((1,2), (1,1)))
        >>> g1.retirer_sommets((0,1))
        >>> g1._matrice_adjacence
        [[0]]
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes(((1,2), (1,1)))
        >>> g1.retirer_sommets({0,1})
        >>> g1._matrice_adjacence
        [[0]]
        """
        #on arrête tout si on a un sommet interdit (une valeur inférieure 0)
        for sommet in iterable:
            if sommet < 0:
                print("Un des nombres est inférieur à 0 donc on ne peut pas créer des graphes")
                return
        #on classe les sommets à retirer dans l'ordre décroissant pour éviter des problèmes
        #de out of range
        iterable2 = []
        for ssliste in iterable:
            iterable2.append(ssliste)
        iterable2.sort(reverse=True)
        #on regarde chaque sommet de l'itérable
        #ensuite on applique sur chacun de ces sommets "retirer_sommet"
        
        for sommet in iterable2:
            self.retirer_sommet(sommet)
        

    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe.
        >>> g1 = MatriceAdjacence()
        >>> g1.ajouter_aretes([[1,2], [1,9]])
        >>> g1.sommets()
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        """
        liste = []
        for e in range(0,len(self._matrice_adjacence)):
            liste.append(e)
        return liste

    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné.
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes(((1,4), (1,3), (4,2), (2,0)))
        >>> G.sous_graphe_induit([1,3,0])
        [[0, 0, 0], [0, 0, 1], [0, 1, 0]]
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([[1,4], [1,3], [4,2], [2,0]])
        >>> G.sous_graphe_induit([1, 3])
        [[0, 1], [1, 0]]
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([[1,4], [1,3], [4,2], [2,0]])
        >>> G.sous_graphe_induit({1, 3})
        [[0, 1], [1, 0]]
        """
        for e in iterable:
            if e < 0:
                print("Un des nombres est inférieur à 0 donc on ne peut pas créer des graphes")
                return
        #on fait une copie profonde du graphe d'origine
        G = MatriceAdjacence()
        G._matrice_adjacence = copy.deepcopy(self._matrice_adjacence)
        #contient les numéros des sommets à retirer
        supprimer = []
        #on retire chaque sommet de ce graphe qui n'est pas dans l'itérable
        for e in range(0,len(self._matrice_adjacence)):
            if e not in iterable:
                supprimer.append(e)
        G.retirer_sommets(supprimer)
        return G._matrice_adjacence
    

    def export_dot(graphe):
        """Renvoie une chaîne encodant le graphe au format dot.
        >>> G = MatriceAdjacence()
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes(((1,4), (1,3), (4,2), (2,0)))
        >>> G.export_dot()
        'graph G {  0 ; 0 -- 2; 1 ; 1 -- 3; 1 -- 4; 2 ; 2 -- 4; 3 ; 4 ; }'
        >>> G = MatriceAdjacence()
        >>> G = MatriceAdjacence()
        >>> G.ajouter_aretes([[1,4], [1,3], [4,2], [2,0]])
        >>> G.export_dot()
        'graph G {  0 ; 0 -- 2; 1 ; 1 -- 3; 1 -- 4; 2 ; 2 -- 4; 3 ; 4 ; }'
        >>> G = MatriceAdjacence()
        >>> G.ajouter_sommet()
        0
        >>> G.ajouter_sommet()
        1
        >>> G.ajouter_sommet()
        2
        >>> G.ajouter_sommet()
        3
        >>> G.ajouter_sommet()
        4
        >>> G.export_dot()
        'graph G {  0 ; 1 ; 2 ; 3 ; 4 ; }'
        
        """
        #compteur contient le numéro du sommet traité
        compteur = 0
        traite = []
        res = "graph G { "
        
        for liste in graphe._matrice_adjacence:
            #on ajoute le sommet au cas où il s'avère qu'il serait seul par exemple quitte à faire des redites, car un seul parcours évite d'accroirtre la complexité
            res += " " + str(compteur) + " ;"
            #compteur2 contient le numéro du sommet relié à notre sommet
            compteur2 = 0
            #pour chaque lien dans la sous-liste, on créé une arète si la valeur vaut 1 (le lien existe)
            # et à condition qu'on est sur le plus petit sommet du lien (pour ne pas ajouter 2x le même lien)
            for lien in liste:
                if(lien == 1 and compteur < compteur2):
                    res += " "+ str(compteur) + " -- " + str(compteur2) + ";"
                compteur2+=1
            #une fois qu'on a terminé avec le sommet (compteur) on change de sommet
            compteur+=1
        res += " }"
        return res


def main():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()