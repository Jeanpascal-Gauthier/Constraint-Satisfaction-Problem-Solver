import sys

def main():
    var_file = sys.argv[1]
    con_file = sys.argv[2]
    procedure = sys.argv[3]
     
    var_map = {}
    con_list = []

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

    

if __name__ == "__main__":
    main()