import time


class Csp:

    def __init__(self, variables, domains, neighbors, constraints, binary_constraints, check_constraints, board):

        self.variables = variables
        self.domains = domains
        self.neighbors = neighbors
        self.constraints = constraints
        self.binary_constraints = binary_constraints
        self.check_constraints = check_constraints
        self.curr_domains = None
        self.num_assigns = 0
        self.num_backtrack = 0
        self.board = board
        self.assignments = {}

    def assign(self, var, val):
        self.assignments[var] = val
        self.board[var[0]][var[1]] = val
        self.num_assigns += 1

    def un_assign(self, var):
        if var in self.assignments:
            del self.assignments[var]
        self.board[var[0]][var[1]] = ''

    def has_conflict(self, var, val):
        for var2 in self.neighbors.get(var):
            val2 = None
            if self.assignments.__contains__(var2):
                val2 = self.assignments[var2]
            if val == val2:
                return True

        for key, value in self.constraints.items():
            if var in value[1]:
                if not self.check_constraints(val, value, self.assignments):
                    return True
        return False

    def num_conflicts(self, var, val):
        num_conf = 0
        for var2 in self.neighbors.get(var):
            val2 = None
            if self.assignments.__contains__(var2):
                val2 = self.assignments[var2]
            num_conf += 1 if val == val2 else 0

        for key, value in self.constraints.items():
            if var in value[1]:
                sum = int(val)
                count = 1
                for nei in value[1]:
                    if nei in self.assignments:
                        sum += int(self.assignments[nei])
                        count += 1

                if (sum > value[0]) or ((count == len(value[1])) and (sum != value[0])):
                    num_conf += 1
        return num_conf

    def support_pruning(self):
        if self.curr_domains is None:
            self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

    def change_domain(self, var, value):
        self.support_pruning()
        removals = [(var, a) for a in self.curr_domains[var] if a != value]
        self.curr_domains[var] = [value]
        return removals

    def prune(self, var, value, removals):
        self.curr_domains[var].remove(value)
        if removals is not None:
            removals.append((var, value))

    def restore(self, removals):
        for B, b in removals:
            self.curr_domains[B].append(b)

    def has_values(self, var1, val1, var2, val2):
        for key, value in self.binary_constraints.items():
            if key == (var1, var2):
                if (int(val1), int(val2)) in value:
                    return True
        return False


# Constraint Propagation with AC-3

def AC3(csp, queue=None, removals=None):
    if queue is None:
        queue = [(Xi, Xk) for Xi in csp.variables for Xk in csp.neighbors[Xi]]
    csp.support_pruning()
    while queue:
        (Xi, Xj) = queue.pop()
        if revise(csp, Xi, Xj, removals):
            if not csp.curr_domains[Xi]:
                return False
            for Xk in csp.neighbors[Xi]:
                if Xk != Xi:
                    queue.append((Xk, Xi))
    return True


def revise(csp, Xi, Xj, removals):
    revised = False
    for x in csp.curr_domains[Xi][:]:
        # If Xi=x conflicts with Xj=y for every possible y, eliminate Xi=x
        if all(not csp.has_values(Xi, x, Xj, y) for y in csp.curr_domains[Xj]):
            csp.prune(Xi, x, removals)
            revised = True
    return revised


# Variable ordering
def first_unassigned_variable(csp):
    for var in csp.variables:
        if var not in csp.assignments:
            return var


def mcv_inference(csp):
    const_min = {}
    for var in csp.variables:
        if var not in csp.assignments.keys():
            for key, value in csp.constraints.items():
                if var in value[1]:
                    if var in const_min:
                        if value[0] < const_min[var]:
                            const_min[var] = value[0]
                    else:
                        const_min[var] = value[0]

    const = sorted(const_min.items(), key=lambda x: x[1])[:10]
    size = []
    for var in const:
        size.append(num_legal_values(csp, var[0]))
    return const[size.index(min(size))][0]


def num_legal_values(csp, var):
    if csp.curr_domains:
        return len(csp.curr_domains[var])
    else:
        count = 0
        for val in csp.domains[var]:
            if not csp.has_conflict(var, val):
                count += 1
        return count


# Value ordering

def unordered_domain_values(var, csp):
    return (csp.curr_domains or csp.domains)[var]


def lcv(var, csp):
    return sorted((csp.curr_domains or csp.domains)[var], key=lambda val: csp.num_conflicts(var, val))


# Inference

def no_inference(csp, var, removals):
    return True


def forward_checking(csp, var, removals):
    for nei in csp.neighbors[var]:
        if nei not in csp.assignments:
            for b in csp.curr_domains[nei][:]:
                if csp.has_conflict(nei, b):
                    csp.prune(nei, b, removals)
            if not csp.curr_domains[nei]:
                return False
    return True


def mac(csp, var, removals):
    return AC3(csp, [(X, var) for X in csp.neighbors[var]], removals)


# Backtracking search
def backtracking_search(csp, select_variable, order_values, inference, slow=False):
    def backtrack():
        if len(csp.assignments) == len(csp.variables):
            return csp.assignments
        var = select_variable(csp)
        for value in order_values(var, csp):
            if not csp.has_conflict(var, value):
                csp.assign(var, value)
                if slow:
                    time.sleep(0.1)
                removals = csp.change_domain(var, value)
                if inference(csp, var, removals):
                    result = backtrack()
                    if result is not None:
                        return result
                    else:
                        csp.num_backtrack += 1
                csp.restore(removals)
                csp.un_assign(var)
        return None

    result = backtrack()
    return result
