# artificial_intelligence_9_puzzle

This is a 9 Puzzle Game solver using the following uninformed and informed search methods:
- Breadth-First-Search (bfs)
- Depth_first_Search (dfs)
- A* (ast)
- Iterative-Deepening A* (ida)

### Description

The 9 Puzzle Game is a sliding blocks game that takes place on a 3 X 3 grid with 8 tiles each numbered from 1 to 8. The task is to reposition the tiles in the proper order. For this purpose, the number 0 is used to represent a blank space.

So for example, the following puzzle:

5 1 2  
3 4 0  
6 7 8

needs to be repositioned to:

0 1 2  
3 4 5  
6 7 8

Tiles may slide in the blank space (0) to reposition the rest accordingly. Tiles may not be moved diagonally.

### Usage Example
To solve the following puzzle with the BFS method:
  
5 1 2  
3 4 0  
6 7 8

enter the following in the command line:

`python driver.py bfs 5,1,2,3,4,0,6,7,8`

The 1st argument is the method desired (bfs, dfs, ast, ida) and the 2nd is the puzzle.

### Output example (displayed on console and written to output.txt file)

path_to_goal: ['Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Down', 'Left', 'Left', 'Up']  
cost_of_path: 11  
nodes_expanded: 884  
fringe_size: 573  
max_fringe_size: 575  
search_depth: 11  
running_time: 0.04104710  
max_ram_usage: 8.97433600

path_to_goal explains the moves of the 0 taken to solve the puzzle
