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


def variable_selection(var, con_lookup, assignment):
    unassigned = []
    for var in var_map:
        if var not in assignment:
            unassigned.append(var)

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

if __name__ == "__main__":
    main()