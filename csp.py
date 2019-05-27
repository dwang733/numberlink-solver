from constraint import *


def node_neighbor_constraint(*args):
    node = args[0]
    neighbors_arg = args[1:]
    return sum([neighbor == node for neighbor in neighbors_arg]) == 2  # Nodes must have only 2 same-colored neighbors


def source_neighbor_constraint(*args):
    node = args[0]
    neighbors_arg = args[1:]
    return sum([neighbor == node for neighbor in neighbors_arg]) == 1  # Sources must have only 1 same-colored neighbor


def no_kinks_constraint(*args):
    return len(set(args)) > 1


puzzle_name = "puzzles/regular_7x7_01.txt"
with open(puzzle_name) as f:
    puzzle = f.readlines()
    puzzle = list(map(str.rstrip, puzzle))

n = len(puzzle)
domain = list(set(''.join(puzzle)))  # Get all unique characters in puzzle
domain.remove('.')

problem = Problem()
for i, line in enumerate(puzzle):
    for j, char in enumerate(line):
        if char == '.':
            problem.addVariable(f'{i}{j}', domain)
        else:
            problem.addVariable(f'{i}{j}', [char])  # Sources can only be themselves

# Add constraints so flows are properly linked
for i, line in enumerate(puzzle):
    for j, char in enumerate(line):
        constraint_args = [f'{i}{j}']  # Node we're constraining on
        if i - 1 >= 0:
            constraint_args.append(f'{i - 1}{j}')
        if i + 1 < n:
            constraint_args.append(f'{i + 1}{j}')
        if j - 1 >= 0:
            constraint_args.append(f'{i}{j - 1}')
        if j + 1 < n:
            constraint_args.append(f'{i}{j + 1}')

        if char == '.':
            problem.addConstraint(node_neighbor_constraint, constraint_args)
        else:
            problem.addConstraint(source_neighbor_constraint, constraint_args)

# Don't allow 2x2 "kinks" in flows (is this necessary?)
for i in range(n - 1):
    for j in range(n - 1):
        problem.addConstraint(no_kinks_constraint, [f'{i}{j}', f'{i + 1}{j}', f'{i}{j + 1}', f'{i + 1}{j + 1}'])

problem.setSolver(RecursiveBacktrackingSolver())
solution_dict = problem.getSolution()
print(solution_dict)
solution = [[0] * n for _ in range(n)]
for k, v in solution_dict.items():
    row = int(k[0])
    col = int(k[1])
    solution[row][col] = v

for line in solution:
    print(line)
