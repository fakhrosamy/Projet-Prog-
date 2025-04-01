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
        (dico_graphe,dico_valeur)=Graph.create_oriented(self)
        pairs=[]
        chemin=Graph.parcours(self, dico_graphe, dico_valeur)
        while len(chemin)>0:
            print(chemin)
            for i in range(1,len(chemin)):
                if i%2==1:
                    pairs.append((chemin[i],chemin[i-1]))
                    dico_valeur[chemin[i-1],(-2,-2)]=0
                    dico_valeur[chemin[i],chemin[i-1]]=0
                    dico_valeur[chemin[i-1],chemin[i]]=1
                else:
                    pairs.remove((chemin[i-1],chemin[i]))
                    dico_valeur[chemin[i],chemin[i-1]]=0
                    dico_valeur[chemin[i-1],chemin[i]]=1
            dico_valeur[((-1,-1),chemin[-1])]=0
            chemin = Graph.parcours(self, dico_graphe, dico_valeur)
        
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



class SolverHongrois(Solver):
    """
    Solver qui utilise l'algorithme hongrois (que l'on n'a pas codé)
   
    """
 
    def _init_(self, grid):
        super()._init_(grid)
        self.grid = grid

    def score(self, pairs):
        """Permet de calculer le score total d'une liste de paires."""
        used_cells = []
        score = 0
        
        # On somme les différences absolues des valeurs de chaque paire
        for pair in pairs:
            score += Grid.cost(self, pair)
            used_cells.append(pair[0])
            used_cells.append(pair[1])
        
        # On somme ensuite les valeurs des cellules non appariées sauf celles de couleur noire
        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i, j) not in used_cells and not self.grid.is_forbidden(i, j):
                    score += self.grid.value[i][j]
        return score

    def run(self):
        """
        Output:
        -------
        tuple (pairs, score)
          pairs: list[tuple[tuple[int]]]
          score: int
        """
        # On construit ensuite la matrice de coûts 
        pairs = self.grid.all_pairs()
        even_cells = []
        odd_cells = []
        for pair in pairs:
            cell1, cell2 = pair
            if (cell1[0]+cell1[1])%2 == 0: # On fait un test sur la parité de la cellule
                if not cell1 in even_cells:
                    even_cells.append(cell1)
                if not cell2 in odd_cells: 
                    odd_cells.append(cell2)
            else:
                if not cell1 in odd_cells:
                    odd_cells.append(cell1)
                if not cell2 in even_cells:
                    even_cells.append(cell2)

        # On veut récupérer les indices des cellules 
        even_cells_indices = {cell: idx for idx, cell in enumerate(even_cells)}
        odd_cells_indices = {cell: idx for idx, cell in enumerate(odd_cells)}

        matrice_cout = np.full((len(even_cells), len(odd_cells)), 0)
        for (i1, j1) in even_cells:
            for (i2, j2) in odd_cells:
                if max(abs(i1-i2),abs(j1-j2)) == 1 and min(abs(i1-i2),abs(j1-j2)) == 0: # On s'assure que les cellules sont adjacentes
                    if ((i1,j1),(i2,j2)) in pairs or ((i2,j2),(i1,j1)) in pairs: # On évite de faire le calcul deux fois pour la même paire 
                        cost = -(self.grid.value[i1][j1] + self.grid.value[i2][j2] - abs(self.grid.value[i1][j1] - self.grid.value[i2][j2])) # On met un signe - devant pour revenir à un problème de maximisation
                        matrice_cout[even_cells_indices[(i1, j1)], odd_cells_indices[(i2, j2)]] = cost
        
        # On applique à ce niveau l'algorithme hongrois qui va nous permettre d'obtenir l'affectation optimale des pairs avec la matrice coût précédente
        resultat = algo_hongrois(matrice_cout)
        
        # On calcule enfin le score final
        pairs = []
        used_cells = []
        for i, j in resultat:
            if matrice_cout[i,j] != 0:
                cell1 = even_cells[i]
                cell2 = odd_cells[j]
                if cell1 not in used_cells and cell2 not in used_cells:
                    pairs.append((cell1, cell2))
                    used_cells.append(cell1)
                    used_cells.append(cell2)
        self.pairs = pairs.copy()
        return self.pairs, self.score(self.pairs)


