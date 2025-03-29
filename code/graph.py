# Création d'une classe graph utilisé dans la suite par Ford Fulkerson

from grid import Grid

class Graph () :
    
    def __init__(self):
        pass
    def create_oriented(self):
        """Créer un graphe orienté pour utiliser la méthode des flots
        
        dico_capacite: contient la capacité des arètes, dans la cas présent 0 ou 1
        dico_graphe: similaire à une liste d'adjacence
        
        (-1,-1) est le sommet source du graphe biparti
        (-2,-2) est le sommet puit du graphe biparti"""
        L=self.grid.all_pairs()
        dico_capacite={}
        dico_graphe={}
        dico_graphe[(-1,-1)]=[]
        for k in range(len(L)):
            if sum(L[k][0])%2==0:   # on vérifie que le sommet est pair, il s'agit du critère de partition de notre graphe biparti
                t1=L[k][0]
                t2=L[k][1]
            else:
                t2=L[k][0]
                t1=L[k][1]

            dico_capacite[(t1,t2)]=1
            dico_capacite[((t2,t1))]=0
            dico_capacite[((t2,(-2,-2)))]=1
            dico_capacite[(((-1,-1),t1))]=1

            if t1 not in dico_graphe:
                dico_graphe[t1]=[t2]
            else:
                dico_graphe[t1].append(t2)

            if t2 not in dico_graphe:
                dico_graphe[t2]=[t1]
            else:
                dico_graphe[t2].append(t1)
            
            if t1 not in dico_graphe[(-1,-1)]:
                dico_graphe[(-1,-1)].append(t1)
            if (-2,-2) not in dico_graphe[t2]:
                dico_graphe[t2].append((-2,-2))

        return (dico_graphe,dico_capacite)
    
    def trajet(self, parent,sommet):
        # Pour retrouver le chemin augmentant trouvé dans le graphe par le parcours en profondeur
        L=[]
        while sommet!=(-1,-1):
            L.append(sommet)
            sommet=parent[sommet]
        return L

    def parcours(self,dico_graphe,dico_capacite):
        """Parcours en largeur pour la méthode des flots
        On cherche un chemin entre (-1,-1) le sommet source et (-2,-2) le sommet target.
        Le parcours en largeur est classique si ce n'est qu'il faut vérifier que la capacité
        d'une arète est non nulle"""
        a_parcourir=[(-1,-1)]
        parent={}
        while len(a_parcourir)>0:
            sommet=a_parcourir.pop(0)
            for k in range(len(dico_graphe[sommet])):
                if dico_graphe[sommet][k]==(-2,-2) and dico_capacite[(sommet,dico_graphe[sommet][k])]==1:
                    return Graph.trajet(self, parent,sommet)
                else:
                    if dico_graphe[sommet][k] not in parent and dico_capacite[(sommet,dico_graphe[sommet][k])]==1:
                        parent[dico_graphe[sommet][k]]=sommet
                        a_parcourir.append(dico_graphe[sommet][k])
        return []



