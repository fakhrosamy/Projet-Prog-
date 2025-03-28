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

class SolverFulkerson(Solver):

    """
    Implémente un solveur basé sur l'algorithme de Ford-Fulkerson pour trouver un appariement maximal.
    Cette approche fonctionne uniquement lorsque toutes les valeurs des cellules sont égales à 1.
    """
    def run(self):
        """
        Exécute l'algorithme de Ford-Fulkerson pour trouver un matching maximal dans le graphe biparti de la grille.
        """
        self.pairs = []
        
        # Construire le graphe biparti des paires valides
        even_cells = [] #cellules paires
        odd_cells = [] #cellules impaires
        adj_dict = {} #dictionnaire où chaque clé représente une cellule paire, et la valeur est une liste des cellules impaires adjacentes.

        for i in range(self.grid.n):
            for j in range(self.grid.m):
                if (i + j) % 2 == 0:
                    even_cells.append((i, j))
                else:
                    odd_cells.append((i, j))

        for elt2 in even_cells:
            L=[]
            for i in range (self.grid.n):
                for j in range (self.grid.m):
                    if self.grid.color[i][j]==0: #on associe les blanches à toutes les autres cases sauf les noires
                        if i>1:
                            if self.grid.is_forbidden(i-1,j)==False:
                                L.append(((i-1,j)))
                                
                        if i<self.grid.n-1:
                            if self.grid.is_forbidden(i+1,j)==False:
                                L.append(((i+1,j)))

                        if j>1 : 
                            if self.grid.is_forbidden(i,j-1)==False:
                                L.append(((i,j-1)))

                        if j<self.grid.n-1:
                            if self.grid.is_forbidden(i,j+1)==False:
                                L.append(((i,j+1)))

                    elif self.grid.color[i][j]==1: #on associe les rouges aux rouges et aux bleues
                        if i>1:
                            if self.grid.color[i-1][j]==1 or self.grid.color[i-1][j]==2:
                                L.append(((i-1,j)))

                        if i<self.grid.n-1:
                            if self.grid.color[i+1][j]==1 or self.grid.color[i+1][j]==2:
                                L.append(((i+1,j)))

                        if j>1 : 
                            if self.grid.color[i][j-1]==1 or self.grid.color[i][j-1]==2:
                                L.append(((i,j-1)))

                        if j<self.grid.n-1:
                            if self.grid.color[i][j+1]==1 or self.grid.color[i][j+1]==2:
                                L.append(((i,j+1)))

                    elif self.grid.color[i][j]==2: #on associe les bleues aux bleues
                        if i>1:
                            if self.grid.color[i-1][j]==2:
                                L.append(((i-1,j)))

                        if i<self.grid.n-1:
                            if self.grid.color[i+1][j]==2:
                                L.append(((i+1,j)))

                        if j>1 : 
                            if self.grid.color[i][j-1]==2:
                                L.append(((i,j-1)))

                        if j<self.grid.n-1:
                            if self.grid.color[i][j+1]==2:
                                L.append(((i,j+1)))

                    elif self.grid.color[i][j]==3: #on associe les vertes aux vertes
                        if i>1:
                            if self.grid.color[i-1][j]==3:
                                L.append(((i-1,j)))

                        if i<self.grid.n-1:
                            if self.grid.color[i+1][j]==3:
                                L.append(((i+1,j)))

                        if j>1 : 
                            if self.grid.color[i][j-1]==3:
                                L.append(((i,j-1)))

                        if j<self.grid.n-1:
                            if self.grid.color[i][j+1]==3:
                                L.append(((i,j+1)))

            adj_dict[elt2]=L
        
        # Fonction récursive pour trouver un chemin augmentant
        def find_augmenting_path(cell, visited, matching):
            for neighbor in adj_dict[cell]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    if neighbor not in matching or find_augmenting_path(matching[neighbor], visited, matching):
                        matching[neighbor] = cell
                        matching[cell] = neighbor
                        return True
            return False
        
        # Trouver l'appariement maximal avec Ford-Fulkerson
        matching = {}
        for cell in adj_dict:
            if cell not in matching:
                find_augmenting_path(cell, set(), matching)

        # Extraire les paires de l'appariement
        self.pairs = [(cell, matching[cell]) for cell in matching if isinstance(matching[cell], tuple) and cell < matching[cell]]

    
    def score(self):
        """
        Puisque toutes les valeurs sont égales à 1, le score final est simplement le nombre de cellules non appariées.
        """
        used_cells = {cell for pair in self.pairs for cell in pair}
        total_unpaired = sum(1 for i in range(self.grid.n) for j in range(self.grid.m)
                             if (i, j) not in used_cells and not self.grid.is_forbidden(i, j))
        return total_unpaired
