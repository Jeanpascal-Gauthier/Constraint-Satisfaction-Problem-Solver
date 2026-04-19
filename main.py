import sys

def main():
    var_file = sys.argv[1]
    con_file = sys.argv[2]
    procedure = sys.argv[3]
     
    var_map = {}
    con_list = []
    
    con_lookup = {}

    with open(var_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(':')
            var_name = parts[0].strip()
            values = list(map(int, parts[1].strip().split()))
            var_map[var_name] = values

    with open(con_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            parts = line.split(' ')
            con_list.append(tuple(parts))

    for var in var_map:
        con_lookup[var] = []

    for con in con_list:
        var1, op, var2 = con
        con_lookup[var1].append(con)
        con_lookup[var2].append(con)

    assignment = {}
    order = []
    backtrack(var_map, con_lookup, assignment, order, procedure)


def variable_selection(var_map, con_lookup, assignment):
    unassigned = []
    for v in var_map:
        if v not in assignment:
            unassigned.append(v)

    min_domain = len(var_map[unassigned[0]])
    for var in unassigned:
        if len(var_map[var]) < min_domain:
            min_domain = len(var_map[var])

    candidates = []
    for var in unassigned:
        if len(var_map[var]) == min_domain:
            candidates.append(var)

    if len(candidates) == 1:
        return candidates[0]
    
    max_constraints = -1
    for var in candidates:
        count = count_unassigned_constraints(var, con_lookup, assignment)
        if count > max_constraints:
            max_constraints = count

    candidates2 = []
    for var in candidates:
        count = count_unassigned_constraints(var, con_lookup, assignment)
        if count == max_constraints:
            candidates2.append(var)

    if len(candidates2) == 1:
        return candidates2[0]
    
    candidates2.sort()

    return candidates2[0]

def count_unassigned_constraints(var, con_lookup, assignment):
    count = 0

    for con in con_lookup[var]:
        var1, op, var2 = con
        other = var2 if var1 == var else var1
        if other not in assignment:
            count += 1
    
    return count

def order_values(var, var_map, con_lookup, assignment):
    value_counts = []

    for val in var_map[var]:
        count = 0
        for con in con_lookup[var]:
            var1, op, var2 = con
            other = var2 if var1 == var else var1

            if other in assignment:
                continue

            for other_val in var_map[other]:
                if not check_values(var, val, other, other_val, con):
                    count += 1

        value_counts.append((count, val))

    value_counts.sort(key=lambda x: (x[0], x[1]))

    result = []
    for count, val in value_counts:
        result.append(val)
    
    return result

def check_values(var1, val1, var2, val2, con):
    con_var1, op, con_var2 = con

    if var1 == con_var2:
        val1, val2 = val2, val1

    if op == '=':
        return val1 == val2
    elif op == '!':
        return val1 != val2
    elif op == '>':
        return val1 > val2
    elif op == '<':
        return val1 < val2

def check_constraint(con, assignment):
    var1, op, var2 = con

    if var1 not in assignment or var2 not in assignment:
        return True

    val1 = assignment[var1]
    val2 = assignment[var2]

    if op == '=':
        return val1 == val2
    elif op == '!':
        return val1 != val2
    elif op == '>':
        return val1 > val2
    elif op == '<':
        return val1 < val2
    
def is_consistent(var, assignment, con_lookup):
    for con in con_lookup[var]:
        if not check_constraint(con, assignment):
            return False
    return True

def backtrack(var_map, con_lookup, assignment, order, procedure):
    if len(assignment) == len(var_map):
        print_branch(assignment, order, "solution")
        return True

    var = variable_selection(var_map, con_lookup, assignment)
    values = order_values(var, var_map, con_lookup, assignment)

    for val in values:
        assignment[var] = val
        order.append(var)

        if procedure == "fc":
            pruned = forward_check(var, val, var_map, con_lookup, assignment)
            if pruned is None:
                print_branch(assignment, order, "failure")
            else:
                if backtrack(var_map, con_lookup, assignment, order, procedure):
                    return True
                restore(var_map, pruned)
        else:
            if is_consistent(var, assignment, con_lookup):
                if backtrack(var_map, con_lookup, assignment, order, procedure):
                    return True
            else:
                print_branch(assignment, order, "failure")

        del assignment[var]
        order.remove(var)

    return False

def forward_check(var, val, var_map, con_lookup, assignment):
    pruned = {}

    for con in con_lookup[var]:
        var1, op, var2 = con
        other = var2 if var1 == var else var1

        if other in assignment:
            continue

        if other not in pruned:
            pruned[other] = []

        for other_val in var_map[other][:]:  
            if not check_values(var, val, other, other_val, con):
                var_map[other].remove(other_val)
                pruned[other].append(other_val)

        if len(var_map[other]) == 0:
            restore(var_map, pruned)
            return None

    return pruned

def restore(var_map, pruned):
    for var in pruned:
        for val in pruned[var]:
            var_map[var].append(val)
        var_map[var].sort()

def print_branch(assignment, order, status):
    parts = []
    for var in order:
        parts.append(var + "=" + str(assignment[var]))
    print(", ".join(parts) + "  " + status)

if __name__ == "__main__":
    main()