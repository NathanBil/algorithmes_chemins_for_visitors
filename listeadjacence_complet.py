#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Implémentation d'un graphe à l'aide d'une liste d'adjacence. Les n sommets
sont identifiés par de simples naturels (0, 1, 2, ..., n-1)."""

import copy

class AreteErronee(Exception):
    """Exception raised for errors in the input iterable.

    Attributes:
        erreur -- message d'erreur explicatif
    """

class ListeAdjacence(object):
    def __init__(self, num=0):
        """Initialise un graphe sans arêtes sur num sommets.

        >>> G = ListeAdjacence()
        >>> G._liste_adjacence
        []
        """
        self._liste_adjacence = [list() for _ in range(num)]

    def ajouter_arete(self, source, destination):
        """Ajoute l'arête {source, destination} au graphe, en créant les
        sommets manquants le cas échéant.
        >>> G = ListeAdjacence()
        >>> G.ajouter_arete(1,2)
        >>> G._liste_adjacence
        [[], [2], [1]]
        >>> G.ajouter_arete(1,0)
        >>> G._liste_adjacence
        [[1], [2, 0], [1]]
        
        """
        #cas où le user a entré des valeurs interdites on sort
        if source < 0 or destination < 0:
            print("Vous avez entré une valeur inférieure à 0, le programme s'arrête")
            return 
        #si l'un des sommets n'est pas présent, on l'ajoute à la liste en créant le nombre de sommet nécessaire
        if(len(self._liste_adjacence)-1 < destination or len(self._liste_adjacence)-1 < source):
            #variable qui contient le nombre de liste, (donc de sommet) à ajouter dans la grande liste
            #on récupère le plus grand nombre entre la source et la destination pour savoir le nombre de 
            #sous-liste à ajouter
            increase = max([source, destination]) - (len(self._liste_adjacence)-1)
            #on ajoute les nouveaux sommets avec leurs cases
            while(increase > 0):
                self._liste_adjacence.append([])
                increase-=1
    #on va dans la liste "source" (qui correspond au sommet source) et on ajoute le sommet
    #destination
        if(destination not in self._liste_adjacence[source]):
            self._liste_adjacence[source].append(destination)
     #on va dans la liste "destination" (qui correspond au sommet destination) et on ajoute le sommet
     #source
        if(source not in self._liste_adjacence[destination]):
            self._liste_adjacence[destination].append(source)

    def ajouter_aretes(self, iterable):
        """Ajoute toutes les arêtes de l'itérable donné au graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples de naturels.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G._liste_adjacence
        [[], [2], [1]]
        >>> G.ajouter_aretes([[4,1],[1,0]])
        >>> G._liste_adjacence
        [[1], [2, 4, 0], [1], [], [1]]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes({(1,2)})
        >>> G._liste_adjacence
        [[], [2], [1]]
        >>> G.ajouter_aretes({(4,1),(1,0)})
        >>> G._liste_adjacence
        [[1], [2, 0, 4], [1], [], [1]]
        
        """
        #on récupère chaque couple de sommet et on s'assure qu'il n'y a pas de valeurs négatives parmi eux
        for couple in iterable:
            if couple[0] < 0 or couple[1] < 0:
                print("Vous avez entré une valeur inférieure à 0, le programme s'arrête")
                return 
        #on récupère chaque couple de sommet et on applique la fonction ajouter arete avec les deux sommets
        for couple in iterable:
            self.ajouter_arete(couple[0], couple[1])

    def ajouter_sommet(self):
        """Ajoute un nouveau sommet au graphe et renvoie son identifiant.

        >>> G = ListeAdjacence()
        >>> G.ajouter_sommet()
        0
        >>> G._liste_adjacence
        [[]]
        >>> G.ajouter_sommet()
        1
        >>> G._liste_adjacence
        [[], []]
        """
        #on ajoute une liste à l'ensemble des listes
        self._liste_adjacence.append([])
        return len(self._liste_adjacence)-1

    def aretes(self):
        """Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u)).
        >>> G = ListeAdjacence()
        >>> G.aretes()
        []
        >>> G.ajouter_aretes([(1,2)])
        >>> G.aretes()
        [(1, 2)]
        >>> G.ajouter_aretes([[4,1],[1,0]])
        >>> G.aretes()
        [(0, 1), (1, 2), (1, 4)]
        """
        #Liste qui contient le résultat final
        res = []
        #Variable qui contient le sommet traité actuellement
        sommet = 0
        #Pour chaque liste de la matrice on regarde les éléments
        for liste in self._liste_adjacence:
        #on peut avoir un sommet de numéro qui correspond au plus au nombre total de sous-liste
            for i in range(0,len(self._liste_adjacence)):
        #Si le sommet "i" est dans la liste "liste" alors on ajoute le couple
                if i in liste:
                    #on ajoute le couple ssi il n'est pas déjà dans la liste mais dans l'ordre inverse
                    if((i, sommet) not in res and (i != sommet)):
                        res.append((sommet,i))
        #on met à jour la valeur du sommet
            sommet+=1
        #on renvoie les couples
        return res

    def boucles(self):
        """Renvoie les boucles du graphe, c'est-à-dire les arêtes reliant un
        sommet à lui-même."""
        """Renvoie l'ensemble des arêtes du graphe sous forme de couples (si on
        les stocke sous forme de paires, on ne peut pas stocker les boucles,
        c'est-à-dire les arêtes de la forme (u, u)).
        >>> G = ListeAdjacence()
        >>> G.boucles()
        []
        >>> G.ajouter_aretes([(1,2)])
        >>> G.boucles()
        []
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.boucles()
        [(0, 0), (1, 1)]
        
        """
        #Liste qui contient le résultat final
        res = []
        #Variable qui contient le sommet traité actuellement
        sommet = 0
        #Pour chaque liste de la matrice on regarde les éléments
        for liste in self._liste_adjacence:
        #on peut avoir un sommet de numéro qui correspond au plus au nombre total de sous-liste
            for i in range(0,len(self._liste_adjacence)):
        #Si le sommet "i" est dans la liste "liste" alors on ajoute le couple
                if i in liste:
                    #on ajoute le couple ssi il n'est pas déjà dans la liste mais dans l'ordre inverse
                    if((i, sommet) not in res and (i == sommet)):
                        res.append((sommet,i))
        #on met à jour la valeur du sommet
            sommet+=1
        #on renvoie les couples
        return res

    def contient_arete(self, u, v):
        """Renvoie True si l'arête {u, v} existe, False sinon.
        >>> G = ListeAdjacence()
        >>> G.contient_arete(1,2)
        False
        >>> G.ajouter_aretes([(1,2)])
        >>> G.contient_arete(1,2)
        True
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.contient_arete(0,0)
        True
        
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
        #cas où on gère une arète
        else:
            couple = self.aretes()
            if((u,v) in couple or (v,u) in couple):
                return True
            else:
                return False

    def contient_sommet(self, u):
        """Renvoie True si le sommet u existe, False sinon.
        >>> G = ListeAdjacence()
        >>> G.contient_sommet(33)
        False
        >>> G.ajouter_aretes([(1,2)])
        >>> G.contient_sommet(2)
        True
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.contient_sommet(44)
        False
        """
        #cas où le user a entré des valeurs interdites on renvoie
        if u < 0:
            return False
        
        #on regarde la taille de la liste pour savoir si le sommet y est
        #si la taille de la liste-1 est de taille supérieure ou égale au numéro du sommet alors oui
        if(len(self._liste_adjacence)-1 >= u):
            return True
        #si la taille de la liste est de taille inférieure ou égale au numéro du sommet alors non
        else:
            return False

    def degre(self, sommet):
        """Renvoie le degré d'un sommet, c'est-à-dire le nombre de voisins
        qu'il possède.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G.degre(2)
        1
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.degre(2)
        1
        >>> G.degre(1)
        2
        >>> G.degre(0)
        1
        """       
        #cas où le user a entré des valeurs interdites on renvoie 0
        if sommet < 0:
            print("le sommet que vous avez entré n'existe pas car il est négatif")
            return 0
        
        #on vérifie que le numéro du sommet n'est pas trop grand
        if(sommet > len(self._liste_adjacence)-1):
            return 0
        else:
            return len(self._liste_adjacence[sommet])

    def nombre_aretes(self):
        """Renvoie le nombre d'arêtes du graphe.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G.nombre_aretes()
        1
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.nombre_aretes()
        1
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.nombre_aretes()
        4
        """
        return len(self.aretes())

    def nombre_boucles(self):
        """Renvoie le nombre d'arêtes de la forme {u, u}.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G.nombre_boucles()
        0
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.nombre_boucles()
        2
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.nombre_boucles()
        2
        """
        return len(self.boucles())

    def nombre_sommets(self):
        """Renvoie le nombre de sommets du graphe.

        >>> from random import randint
        >>> n = randint(0, 1000)
        >>> ListeAdjacence(n).nombre_sommets() == n
        True
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G.nombre_sommets()
        3
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.nombre_sommets()
        3
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.nombre_sommets()
        5
        """
        #le nombre de sommet correspond au nombre de sous-liste
        return len(self._liste_adjacence)
    
    def retirer_arete(self, u,v):
        """Retire l'arête {u, v} si elle existe; provoque une erreur sinon.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2)])
        >>> G.retirer_arete(1,2)
        >>> G._liste_adjacence
        [[], [], []]
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.retirer_arete(0,0)
        >>> G._liste_adjacence
        [[], [2, 1], [1]]
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.retirer_arete(3,0)
        >>> G._liste_adjacence
        [[], [2, 1, 4, 3], [1], [1], [1]]
        
        """
        #cas où un sommet est inférieur à 0, il n'existe pas donc on sort
        if(u < 0 or v < 0):
            msg = "Erreur ce numéro d'arète n'existe pas: ("+ str(u) + "," + str(v) + ") : les nombres négatifs sont interdits"
            raise AreteErronee(msg)
        # on s'assure que la liste est de la bonne taille et qu'elle contient effectivement l'arète demandée
        if((len(self._liste_adjacence)-1 >= max(u,v)) and self.contient_arete(u, v)) == True:
            #on regarde la liste numéro "u" (qui correspond au sommet u) et on supprime l'élément v
            #qui correspond au sommet v
            #si elle est trop petite, on provoque volontairement une erreur
            #cas où on a une arète
            if(u != v):
                self._liste_adjacence[u].remove(v)
                self._liste_adjacence[v].remove(u)
            #cas où on a une boucle
            else:
                self._liste_adjacence[v].remove(u)
        #si l'arète n'existe pas, on provoque volontairement une erreur
        else:
            msg = "Erreur ce numéro d'arète n'existe pas : ("+ str(u) + "," + str(v) + ")"
            raise AreteErronee(msg)

    def retirer_aretes(self, iterable):
        """Retire toutes les arêtes de l'itérable donné du graphe. N'importe
        quel type d'itérable est acceptable, mais il faut qu'il ne contienne
        que des couples d'éléments (quel que soit le type du couple).
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.retirer_aretes([[1,2], [0,0], [3,0]])
        >>> G._liste_adjacence
        [[], [1, 4, 3], [], [1], [1]]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.retirer_aretes({(1,2), (0,0), (3,0)})
        >>> G._liste_adjacence
        [[], [1, 4, 3], [], [1], [1]]
        """
        #on regarde chaque liste de l'iterable 
        #on retire les arètes associées aux sommets en utilisant la fonction "safe"
        #cas où on a une valeur négative on arrête tout
        for liste in iterable:
            if(liste[0] < 0 or liste[1] < 0):
                print("Il y a une valeur négative, on arrête tout")
                return 
        for liste in iterable:
            self.retirer_arete(liste[0], liste[1])
    
    def sommets(self):
        """Renvoie l'ensemble des sommets du graphe.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,2), (0,0), (1,1)])
        >>> G.ajouter_aretes([(1,4), (3,0), (3,1)])
        >>> G.sommets()
        [0, 1, 2, 3, 4]
        """
        liste = []
        for e in range(0,len(self._liste_adjacence)):
            liste.append(e)
        return liste

    def retirer_sommet(self, sommet):
        """Déconnecte un sommet du graphe et le supprime.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,1), (2,0), (1,3)])
        >>> G.retirer_sommet(3)
        >>> G._liste_adjacence
        [[2], [1], [0]]
        >>> G.ajouter_aretes([(1,1), (2,0), (1,3)])
        >>> G.retirer_sommet(0)
        >>> G._liste_adjacence
        [[0, 2], [], [0]]
        """
        #cas où un sommet est inférieur à 0, il n'existe pas donc on sort
        if(sommet < 0):
            print(" le sommet a une valeur inférieure à 0, on sort")
            return 
        #pour chaque liste (sommet x) on retire le sommet (y) que l'on va retirer du graphe
        for liste in self._liste_adjacence:
            #on s'assure que le sommet est dans la liste
            if sommet in liste:
                liste.remove(sommet)
            #pour chaque sommet relié à mon sommet on va le décaler de 1 si sa valeur était
            #plus grande que celle du sommet que l'on a retiré
            #pour cela on retire cette valeur et on ajoute la même valeur -1
            for i in range(0,len(liste)):
                if liste[i] > sommet:
                    liste[i] = liste[i]-1
                
        del self._liste_adjacence[sommet]
        
    def voisins(self, sommet):
        """Renvoie la liste des voisins d'un sommet.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,1), (2,0), (1,3)])
        >>> G.retirer_sommet(3)
        >>> G.voisins(1)
        [1]
        >>> G.ajouter_aretes([(1,1), (2,0), (1,3)])
        >>> G.retirer_sommet(0)
        >>> G.voisins(0)
        [2, 0]
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

    
    def retirer_sommets(self, iterable):
        """Efface les sommets de l'itérable donné du graphe, et retire toutes
        les arêtes incidentes à ces sommets.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([[1,1], [2,0], [1,3]])
        >>> G.retirer_sommets([3,0])
        >>> G._liste_adjacence
        [[0], []]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes(((1,1), (2,0), (1,3)))
        >>> G.retirer_sommets((3,0))
        >>> G._liste_adjacence
        [[0], []]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes(((1,1), (2,0), (1,3)))
        >>> G.retirer_sommets({0,3})
        >>> G._liste_adjacence
        [[0], []]
        """
        #on classe les sommets à retirer dans l'ordre décroissant pour éviter des problèmes
        #de out of range
        
        #on arrête tout si on a un sommet interdit (une valeur inférieure 0)
        for e in iterable:
            if e < 0:
                print("Un des nombres est inférieur à 0 donc on ne peut pas retirer de sommet du graphe")
                return
        iterable2 = []
        for ssliste in iterable:
            iterable2.append(ssliste)
        iterable2.sort(reverse=True)
        for sommet in iterable2:
            self.retirer_sommet(sommet)

    
    def sous_graphe_induit(self, iterable):
        """Renvoie le sous-graphe induit par l'itérable de sommets donné.
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,4), (1,3), (4,2), (2,0)])
        >>> G.sous_graphe_induit([1,3,0])
        [[], [2], [1]]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,4), (1,3), (4,2), (2,0)])
        >>> G.sous_graphe_induit([1,3])
        [[1], [0]]
        >>> G = ListeAdjacence()
        >>> G.ajouter_aretes([(1,4), (1,3), (4,2), (2,0)])
        >>> G.sous_graphe_induit({1,3})
        [[1], [0]]
        """
        for e in iterable:
            if e < 0:
                print("Un des nombres est inférieur à 0 donc on ne peut pas créer des graphes")
                return
                
        #on fait une copie profonde du graphe d'origine
        G = ListeAdjacence()
        G._liste_adjacence = copy.deepcopy(self._liste_adjacence)
        #contient les numéros des sommets à retirer
        supprimer = []
        #on retire chaque sommet de ce graphe qui n'est pas dans l'itérable
        for e in range(0,len(self._liste_adjacence)):
            if e not in iterable:
                supprimer.append(e)
            
        G.retirer_sommets(supprimer)
        return G._liste_adjacence
    
    
    


def main():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()