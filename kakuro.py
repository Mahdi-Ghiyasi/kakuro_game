from csp import *
from itertools import permutations


class Kakuro(Csp):

    def __init__(self, kakuro_puzzle):
        variables = []
        domains = {}
        neighbors = {}
        constraints = {}
        binary_constraints = {}
        self.puzzle = kakuro_puzzle

        for i in range(len(kakuro_puzzle)):
            for j in range(len(kakuro_puzzle[i])):
                # Find empty cells
                if kakuro_puzzle[i][j] == "":
                    var = (i, j)
                    variables.append(var)
                    neighbors[var] = []
                    domains[var] = list(map(str, list(range(1, 10))))

                    # Find all neighbors of var
                    for k in range(j, len(kakuro_puzzle[i])):
                        if kakuro_puzzle[i][k] == "":
                            nei = (i, k)
                            if nei != var:
                                neighbors[var].append(nei)
                        else:
                            break
                    for k in reversed(range(0, j)):
                        if kakuro_puzzle[i][k] == "":
                            nei = (i, k)
                            if nei != var:
                                neighbors[var].append(nei)
                        else:
                            break
                    for m in range(i, len(kakuro_puzzle)):
                        if kakuro_puzzle[m][j] == "":
                            nei = (m, j)
                            if nei != var:
                                neighbors[var].append(nei)
                        else:
                            break
                    for m in reversed(range(0, i)):
                        if kakuro_puzzle[m][j] == "":
                            nei = (m, j)
                            if nei != var:
                                neighbors[var].append(nei)
                        else:
                            break

                # Find slash cells
                if kakuro_puzzle[i][j] != '' and kakuro_puzzle[i][j] != 'X':

                    # Sum of cells down
                    if kakuro_puzzle[i][j][0] != "":
                        constraint = "C_d" + str(i) + "," + str(j)
                        constraints[constraint] = [[], []]
                        constraints[constraint][0] = int(kakuro_puzzle[i][j][0])

                        cell_counter = 0
                        for m in range(i + 1, len(kakuro_puzzle)):
                            if kakuro_puzzle[m][j] != "":
                                break
                            nei = (m, j)
                            constraints[constraint][1].append(nei)
                            cell_counter += 1
                        perms = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], cell_counter)
                        possible_perms = []
                        for perm in perms:
                            if sum(perm) == constraints[constraint][0]:
                                possible_perms.append(perm)

                        for perm in possible_perms:
                            for p in range(len(constraints[constraint][1])):
                                for q in range(len(constraints[constraint][1])):
                                    if p != q:
                                        key = (constraints[constraint][1][p], constraints[constraint][1][q])
                                        if key not in binary_constraints:
                                            binary_constraints[key] = {(perm[p], perm[q])}
                                        else:
                                            binary_constraints[key].add((perm[p], perm[q]))
                                        key = (constraints[constraint][1][q], constraints[constraint][1][p])
                                        if key not in binary_constraints:
                                            binary_constraints[key] = {(perm[q], perm[p])}
                                        else:
                                            binary_constraints[key].add((perm[q], perm[p]))

                    # Sum of cells right
                    if kakuro_puzzle[i][j][1] != "":
                        constraint = "C_r" + str(i) + "," + str(j)
                        constraints[constraint] = [[], []]
                        constraints[constraint][0] = int(kakuro_puzzle[i][j][1])
                        cell_counter = 0
                        for k in range(j + 1, len(kakuro_puzzle[i])):
                            if kakuro_puzzle[i][k] != "":
                                break
                            nei = (i, k)
                            constraints[constraint][1].append(nei)
                            cell_counter += 1

                        perms = permutations([1, 2, 3, 4, 5, 6, 7, 8, 9], cell_counter)
                        possible_perms = []
                        for perm in perms:
                            if sum(perm) == constraints[constraint][0]:
                                possible_perms.append(perm)

                        for perm in possible_perms:
                            for p in range(len(constraints[constraint][1])):
                                for q in range(len(constraints[constraint][1])):
                                    if p != q:
                                        key = (constraints[constraint][1][p], constraints[constraint][1][q])
                                        if key not in binary_constraints:
                                            binary_constraints[key] = {(perm[p], perm[q])}
                                        else:
                                            binary_constraints[key].add((perm[p], perm[q]))
                                        key = (constraints[constraint][1][q], constraints[constraint][1][p])
                                        if key not in binary_constraints:
                                            binary_constraints[key] = {(perm[q], perm[p])}
                                        else:
                                            binary_constraints[key].add((perm[q], perm[p]))

        Csp.__init__(self, variables, domains, neighbors, constraints, binary_constraints, self.is_consistant,
                     self.puzzle)

    def is_consistant(self, val, constraint, assignments):
        if assignments == {}:
            return True
        sum = int(val)
        count = 1
        for nei in constraint[1]:
            if nei in assignments:
                sum += int(assignments[nei])
                count += 1

        if (sum > constraint[0]) or ((count == len(constraint[1])) and (sum != constraint[0])
                                     or ((count < len(constraint[1])) and (sum == constraint[0]))):
            return False

        return True
