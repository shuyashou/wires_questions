from typing import List, Set, Tuple

WIRE_CHARACTERS = {'|', '-'}
INPUT_CHARACTERS = ('A', 'B')
GATE_CHARACTER = 'G'
OUTPUT_CHARACTER = 'X'

def get_board(opname: str) -> str:
    # Read board from file

    with open(f"./circuits/{opname}.txt") as f:
        return f.read()

def gridify_board(board: str) -> List[List[str]]:
    # Return 2D char array representation of board

    return list(list(line) for line in board.split('\n'))

def nand_gate(a: bool, b: bool) -> bool:
    '''
    simulate a NAND gate
    '''
    return not(a and b)

def get_input(grid: List[List[str]], x: int, y: int, a_value: bool, b_value: bool, visited: Set[Tuple[int, int]]) -> bool:
    '''
    return the closest input of a gate
    '''
    if not (0<=x<len(grid)) or not(0<=y<len(grid[x])) or grid[x][y] == ' ':
        return None

    if(grid[x][y] == 'A'):
        return a_value
    elif(grid[x][y] == 'B'):
        return b_value
    elif(grid[x][y] == 'G'):
        return get_gate_value(grid, x, y, a_value, b_value, visited)

    # check if the exploring coordinate is in current path, if not add it to the current path.
    if((x,y) in visited):
        return None
    visited.add((x, y))

    if(grid[x][y] == '|'): # Explore in 3 possible directions
        up_result = get_input(grid, x-1, y, a_value, b_value, visited)
        if(up_result is not None):
            return up_result
        down_result = get_input(grid, x+1, y, a_value, b_value, visited)
        if(down_result is not None):
            return down_result
        left_result = get_input(grid, x, y-1, a_value, b_value, visited)
        if(left_result is not None):
            return left_result
    elif(grid[x][y] == '-'): # Explore to the left
        left_result = get_input(grid, x, y-1, a_value, b_value, visited)
        if(left_result is not None):
            return left_result
    return None
    

def get_gate_value(grid: List[List[str]], x: int, y: int, a_value: bool, b_value: bool, visited: Set[Tuple[int, int]]) -> bool:
    '''
    return the output of a gate with coordianate (x, y)
    '''
    i1 = get_input(grid, x-1, y-1, a_value, b_value, visited.copy())
    i2 = get_input(grid, x+1, y-1, a_value, b_value, visited.copy())
    return nand_gate(i1, i2)

def find_output(grid: List[List[str]], output: str) -> Tuple[int, int]:
    '''
    return the coordinate of circuit output (x, y)
    '''
    for i, row in enumerate(grid):
        for j in range(len(row)):
            if row[j] == output:
                return i, j

    return -1, -1

def evaluate_function(board: str, *inputs: bool) -> bool:
    # Given a board string, evaluate the boolean function with the
    # given inputs

    grid = gridify_board(board)
    x_pos, y_pos = find_output(grid, 'X')
    if x_pos == -1 or y_pos == -1:
        raise ValueError("output not found")
    x = x_pos 
    y = y_pos
    while(grid[x][y] != 'G'):
        y = y-1

    visited = set()
    if(len(inputs) == 2):
        output_value = get_gate_value(grid, x, y, inputs[0], inputs[1], visited)
    else:
        output_value = get_gate_value(grid, x, y, inputs[0], inputs[0], visited)

    return output_value


