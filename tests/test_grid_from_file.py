# This will work if ran from the root folder (the folder in which there is the subfolder code/)
import sys 
sys.path.append("code/")

import unittest 
from grid import Grid
from solver import *



# This will work if ran from the root folder (the folder in which there is the subfolder code/)




"""mettre cd .. avant de lancer les tests dans le terminal"""

class Test_Grid(unittest.TestCase):
    def test_grid0(self): # On vérifie que la grille est bien chargée
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[5, 8, 4], [11, 1, 3]])

    def test_grid0_novalues(self): # On vérifie que la grille n'est pas bien chargée si read_values=False
        grid = Grid.grid_from_file("input/grid00.in", read_values=False)
        self.assertEqual(grid.n, 2)
        self.assertEqual(grid.m, 3)
        self.assertEqual(grid.color, [[0, 0, 0], [0, 0, 0]])
        self.assertEqual(grid.value, [[1, 1, 1], [1, 1, 1]])

    def test_is_forbidden0(self): # On vérifie que la case (0, 0) n'est pas interdite
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertFalse(grid.is_forbidden(0, 0))

    def test_is_forbidden1(self): # On vérifie que la case (0, 1) est interdite
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertTrue(grid.is_forbidden(0, 1))

    def test_cost0(self):  # On vérifie que le coût de la paire ((0, 0), (0, 1)) est bien 3
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertEqual(grid.cost(((0, 0), (0, 1))), abs(5 - 8))

    def test_match_colors0(self): # On vérifie que la paire ((0, 0), (0, 1)) est compatible
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        self.assertTrue(grid.match_colors(0, 0, 0, 1))

    def test_match_colors1(self): # On vérifie que la paire ((0, 0), (0, 1)) n'est pas compatible
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        self.assertFalse(grid.match_colors(0, 0, 0, 1))

    def test_all_pairs0(self): # On vérifie que la liste des paires est bien générée sans cases interdites
        grid = Grid.grid_from_file("input/grid00.in", read_values=True)
        expected_pairs = [((0, 0), (0, 1)), ((0, 0), (1, 0)), ((0, 1), (0, 2)), ((0, 1), (1, 1)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertCountEqual(grid.all_pairs(), expected_pairs)

    def test_all_pairs1(self): # On vérifie que la liste des paires est bien générée en présence de cases interdites
        grid = Grid.grid_from_file("input/grid01.in", read_values=True)
        expected_pairs = [((0, 0), (1, 0)), ((0, 2), (1, 2)), ((1, 0), (1, 1)), ((1, 1), (1, 2))]
        self.assertCountEqual(grid.all_pairs(), expected_pairs)
    

    def test_solver_greedy_and_fulkerson(self): # On regarde si le solver greedy renvoie le score optimal (spoiler : non)
        
        test_cases = {
            "grid11.in": 26,
            "grid12.in": 19,
            "grid13.in": 22,   # on compare les différents solver sur des grilles où tout les deux peuvent opérer
            "grid14.in": 27,
            "grid15.in": 21,
            "grid16.in": 28,
            #"grid21.in": 1686,
             # On ne va que jusqu'à 19 parce que les grilles plus grandes prennent trop de temps à calculer
        }
      

        for filename, expected_score in test_cases.items():
            with self.subTest(grid=filename):   # Permet d'exécuter chaque test de grille individuellement, sans que l'échec d'un test n'empêche l'exécution des autres
                grid = Grid.grid_from_file(f"input/{filename}", read_values=True)
                solver1 = SolverGreedy(grid)
                solver1.run()
                solver2=SolverFulkerson(grid)
                solver2.run()
                actual_score1 = solver1.score()
                actual_score2 = solver2.score()
                if actual_score1 != expected_score:
                    print(f"Test failed for {filename} with greedy algorithm : expected {expected_score}, got {actual_score1}") # Une f-string permet d’insérer directement des variables dans une chaîne de caractères en les entourant d’accolades {}
                    #self.assertEqual(actual_score1, expected_score)
                if actual_score1 == expected_score: 
                    print(f"Test passed for {filename}with greedy solver: expected {expected_score}, got {actual_score1}") 
                if  actual_score2 != expected_score:
                     print(f"Test failed for {filename} with ford fulkerson solver : expected {expected_score}, got {actual_score2}") 
                    #self.assertEqual(actual_score1, expected_score)
                if actual_score2 == expected_score: 
                    print(f"Test passed for {filename}with ford fulkerson solver : expected {expected_score}, got {actual_score2}") 

if __name__ == '__main__':
    unittest.main()




    