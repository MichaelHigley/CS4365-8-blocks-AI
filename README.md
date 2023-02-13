1. To run the program, the format for the terminal is 
"python CS4365Assignment1.py <algorithm_name> <input_file_path>"
algorithm_name can be any of the following "DFS", "IDS", "astar1", "astar2" 
DFS - Depth First Search
IDS - Iterative Deepening Search
astar1 - A* algorithm with missing tiles heuristic (Not implemented)
astar2 - A* algorithm with Manhattan distance (Not implemented)
input_file_path - path of file with 8 numbers and one * space seperated (example is included .csv)

2. An example input and output is below
Output is the path from the start state to the goal state as well as number of states enqueued and moves taken. First state printed will always be the start state

python CS4365Assignment1.py DFS input_file_8_blocks.csv  
6 7 1\
8 2 \*\
5 4 3\

6 7 1\
8 \* 2\
5 4 3\

6 7 1\
\* 8 2\
5 4 3\

\* 7 1\
6 8 2\
5 4 3\

7 \* 1\
6 8 2\
5 4 3\

7 8 1\
6 \* 2\
5 4 3\
States enqueued :  32
Moves taken:  5

3. While I didn't have a* fully implemented, I can provide a short analysis of the two heuristics that were planned to be used. If we say x is missing tiles and y is Manhattan distance, it would be true to say that y is a better approximater of actual distance because it takes into account how "wrong" a certain tile is compared to x. x can tell us how many tiles are wrong, but it can't factor in how far away the values are from the goal state. y will generate fewer states enqueued and reach the goal state faster than x as it can more accurately predict how far away the goal state is.