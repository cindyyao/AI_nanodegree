#from utils import *
assignments = []

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        for i in range(len(unit)):
            if len(values[unit[i]]) == 2:
                for j in range(i+1, len(unit)):
                    if values[unit[i]] == values[unit[j]]: #unit[i] and unit[j] are naked twins
                        values = eliminate_naked_twins(values, unit, i, j) # Eliminate the naked twins as possibilities for their peers
    return values


def eliminate_naked_twins(values, unit, i, j):
    """
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}
        unit(list of string): a list of box location 
        i, j: indices of naked twins 

    Return: 
        the values dictionary with the naked twins eliminated from peers.
    """
    # Eliminate values in ith and jth boxes in "unit" from their peers in the same unit
    for value in values[unit[i]]:
        for k in range(len(unit)):
            if k == i or k == j:
                continue
            else:
                values[unit[k]] = values[unit[k]].replace(value, '')
    return values


rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [s+t for s in a for t in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
diagonal1 = [a[0]+a[1] for a in zip(rows, cols)]
diagonal2 = [a[0]+a[1] for a in zip(rows, cols[::-1])]
diag_unitlist = [diagonal1, diagonal2]

unitlist = row_units + column_units + square_units + diag_unitlist
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_dict = dict()
    for i in range(len(grid)):
        key = boxes[i]
        if grid[i] == '.':
            grid_dict[key] = '123456789'
        else:
            grid_dict[key] = grid[i]
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    line = '+'.join(['-' * (width * 3)] * 3)
    for r in rows:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return


def eliminate(values):
    solved_boxes = list()
    for key in boxes:
        if len(values[key]) == 1:
            solved_boxes.append(key)
    for key in solved_boxes:
        for peer in peers[key]:
            values[peer] = values[peer].replace(values[key], '')
    return values

def only_choice(values):
    for unit in unitlist:
        for digit in '123456789':
            occurrence = []
            for box in unit:
                if digit in values[box]:
                    occurrence.append(box)
            if len(occurrence) == 1:
                values[occurrence[0]] = digit
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        values = naked_twins(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    values = reduce_puzzle(values)
    if values == False:
        return False
    # Choose one of the unfilled squares with the fewest possibilities
    if not isSolved(values):
        box = fewestPoss(values)
        for value in values[box]:
            values_temp = values.copy()
            values_temp[box] = value
            values_temp = search(values_temp)
            if isSolved(values_temp):
                return values_temp
        return False
    return values
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    # If you're stuck, see the solution.py tab!


def isSolved(values):
    if values == False:
        return False
    for box in boxes:
        if len(values[box]) > 1:
            return False
    return True


def fewestPoss(values):
    fbox = 'A1'
    minbox = 9
    for box in boxes:
        if len(values[box]) > 1 and len(values[box]) < minbox:
            fbox = box
            minbox = len(values[box])
    return fbox

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    values = grid_values(grid)
    solution = search(values)
    return solution

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
