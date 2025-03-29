from grid import Grid
class Solver:
    """
    A solver class. 

    Attributes: 
    -----------
    self: self
        The self
    pairs: list[tuple[tuple[int]]]
        A list of pairs, each being a tuple ((i1, j1), (i2, j2))
    """

    def __init__(self, grid):
        """
        Initializes the solver.

        Parameters: 
        -----------
        self: self
            The self
        """
        self.grid = grid
        self.pairs = list()

    def score(self):
        """
        Computes the of the list of pairs in self.pairs
        """
        return "Method not implemented yet"

class SolverEmpty(Solver):
    def run(self):
        """
        Exécute l'algorithme glouton pour sélectionner les paires minimisant le coût.
        """
        self.pairs = []
        used_cells = set()
        
        # Récupérer toutes les paires valides et les trier par coût croissant
        valid_pairs = Grid.all_pairs(self.grid)
        sorted_pairs = sorted(valid_pairs, key=lambda pair: self.grid.cost(pair))
        
        for pair in sorted_pairs:
            (i1, j1), (i2, j2) = pair
            if (i1, j1) not in used_cells and (i2, j2) not in used_cells:
                self.pairs.append(pair)
                used_cells.add((i1, j1))
                used_cells.add((i2, j2))
        
    def score(self):
        """
        Calcule le score total basé sur les paires sélectionnées et les cellules non appariées.
        """
        total_score = sum(self.grid.cost(pair) for pair in self.pairs)
        used_cells = {cell for pair in self.pairs for cell in pair}
        # Ajouter les valeurs des cellules non appariées (sauf les noires)
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in used_cells and not self.grid.is_forbidden(i, j):
                    total_score += self.grid.value[i][j]
        
        return total_score


class Graph () :

    def __init__(self,listVertices):

        



    def create_oriented(self):
        """Créer un graphe orienté pour utiliser la méthode des flots
        
        dico_capacite: contient la capacité des arètes
        dico_graphe: similaire à une liste d'adjacence
        
        (-1,-1) est le sommet source du graphe biparti
        (-2,-2) est le sommet puit du graphe biparti"""
        l=self.all_pairs()
        dico_capacite={}
        dico_graphe={}
        dico_graphe[(-1,-1)]=[]
        for k in range(len(l)):
            if sum(l[k][0])%2==0:
                t1=l[k][0]
                t2=l[k][1]
            else:
                t2=l[k][0]
                t1=l[k][1]

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
    
    def trajet(self,pere,sommet):
        """Retrouver le chemin dans le graphe
        Utilisé après dans parcours"""
        l=[]
        while sommet!=(-1,-1):
            l.append(sommet)
            sommet=pere[sommet]
        return l

    def parcours(self,dico_graphe,dico_capacite):
        """Parcours en largeur pour la méthode des flots
        On cherche un chemin entre (-1,-1) le sommet source et (-2,-2) le sommet puit.
        Le parcours en largeur est classique si ce n'est qu'il faut vérifier que la capacité
        d'une arète est non nulle"""
        a_parcourir=[(-1,-1)]
        pere={}
        while len(a_parcourir)>0:
            sommet=a_parcourir.pop(0)
            for k in range(len(dico_graphe[sommet])):
                if dico_graphe[sommet][k]==(-2,-2) and dico_capacite[(sommet,dico_graphe[sommet][k])]==1:
                    return self.trajet(pere,sommet)
                else:
                    if dico_graphe[sommet][k] not in pere and dico_capacite[(sommet,dico_graphe[sommet][k])]==1:
                        pere[dico_graphe[sommet][k]]=sommet
                        a_parcourir.append(dico_graphe[sommet][k])
        return []











class SolverFulkerson(Solver):

    """
    Implémente un solveur basé sur l'algorithme de Ford-Fulkerson pour trouver un appariement maximal.
    Cette approche fonctionne uniquement lorsque toutes les valeurs des cellules sont égales à 1.
    """
    

    def Matrice_équipée(self):  #crée une matrice équipée d'un sommet de départ et d'arrivée
          m=len(self.M)
          Mat_équipée=[[0 for i in range (m+2)] for i in range (m+2)] #la matrice est plus grande pour y inclure le départ et l'arrivée
          for i in range(m):
               for j in range(m):
                    Mat_équipée[i][j]=self.M[i][j]
          for i in range (m):  #ici l'avant dernière colonne correspond au sommet de départ et la dernière à l'arrivée
               if (self.S[i][0]+self.S[i][1])%2==0 :
                    Mat_équipée[m][i]=1
               else :
                    Mat_équipée[i][m+1]=1
          return Mat_équipée
    
    def Ford_Fulkerson(self):
         Mat=self.Matrice_équipée()
         m=len(self.M)
         L = Graph.liste_chemins(Mat,[m],[m+1])
         Solution=[]
         
         while L!=[] :    #tant qu'il existe des chemins dans mon graphe
              print("...")
              for k in range (len(L[0])-1):    
                   i=L[0][k]
                   j=L[0][k+1]
                   Solution.append((i,j))  #j'ajoute un de ces chemins à ma solution
                   Mat[i][j]=0 #je l'enlève de mon graphe, ce qui veut dire que je ne peux plus faire la paire ajoutée à la solution
              # Marquer les arêtes inverses à supprimer
              to_remove = set()
              for elt in Solution:
                  if (elt[1], elt[0]) in Solution:
                      to_remove.add(elt)
                      to_remove.add((elt[1], elt[0]))

                # Supprimer les arêtes inverses
              Solution = [elt for elt in Solution if elt not in to_remove]

                # Inverser les arêtes dans le graphe résiduel
              for i, j in to_remove:
                  Mat[j][i] = 1
              L = Graph.liste_chemins(Mat,[m],[m+1])
         return Solution


def Mat_adj_graphbiparti (self) : 

    L = Grid.all_pairs()
    M = [[0 for i in range (self.grid.n)] for i in range (self.grid.m)]
    for elt in L : 
        c1,c2=L[elt]
        M[c1][c2]=1
    
    return M
    


