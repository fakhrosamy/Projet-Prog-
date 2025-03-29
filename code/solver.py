from grid import Grid
from graph import Graph
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




class SolverFulkerson(Solver):

    """
    Implémente un solveur basé sur l'algorithme de Ford-Fulkerson pour trouver un appariement maximal.
    Cette approche fonctionne uniquement lorsque toutes les valeurs des cellules sont égales à 1.
    """
    
    def run(self):
        grid=self.grid
        (dico_graphe,dico_capacite)=Graph.create_oriented(self)
        pairs=[]
        chemin=Graph.parcours(self, dico_graphe, dico_capacite)
        while len(chemin)>0:
            print(chemin)
            for k in range(1,len(chemin)):
                if k%2==1:
                    pairs.append((chemin[k],chemin[k-1]))
                    dico_capacite[chemin[k-1],(-2,-2)]=0
                    dico_capacite[chemin[k],chemin[k-1]]=0
                    dico_capacite[chemin[k-1],chemin[k]]=1
                else:
                    pairs.remove((chemin[k-1],chemin[k]))
                    dico_capacite[chemin[k],chemin[k-1]]=0
                    dico_capacite[chemin[k-1],chemin[k]]=1
            dico_capacite[((-1,-1),chemin[-1])]=0
            chemin = Graph.parcours(self, dico_graphe, dico_capacite)
        
        self.pairs = pairs
        return pairs
    
    def score(self):
        """
        Puisque toutes les valeurs sont égales à 1, le score final est simplement le nombre de cells non appariées.
        """
        used_cells = {cell for pair in self.pairs for cell in pair}
        total_unpaired = sum(1 for i in range(self.grid.n) for j in range(self.grid.m)
                             if (i, j) not in used_cells and not self.grid.is_forbidden(i, j))
        return total_unpaired



