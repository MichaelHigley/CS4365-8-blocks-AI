#Reads in input of 8 numbers and one * as blank space in to a 2d array
#Input is space seperated and in input files
#Must use the following 4 algorithms:
#Depth-first search, Iterative deepening search, A* using two different heuristics

#python homework1.py <algorithm_name> <input_file_path>
from sys import argv
import numpy as np
import abc
import copy
import heapq

MAX_SEARCH_DEPTH = 10


class Solver(abc.ABC):
    def __init__(self, start_state):
        self.path = []
        self.start_state = start_state
        self.states_q = 0
        
    def get_options(self, start_pos, prev_pos):
        options = []
        (x,y) = start_pos
        for (dx,dy) in (
            (0,-1),
            (-1,0),
            (0,1),
            (1,0),
        ):
            new_pos = (x + dx, y + dy)
            if not new_pos == prev_pos and not self.check_is_oob(new_pos):
                options.append(new_pos)

        return options
    
    def findPos(self, state):
        for i in range(len(state)):
            for j in range(len(state[i])):
                if state[i][j] == '*':
                    return (i,j)

    def check_is_oob(self, new_pos):
        (x,y) = new_pos       
        return (x > 2 or x < 0 or y > 2 or y < 0)

    def is_states_equal(self, state_one, state_two):
        for i in range(len(state_one)):
            for j in range(len(state_one[i])):
                if state_one[i][j] != state_two[i][j]:
                    return False
        
        return True

    def pretty_matrix(self, mat):
        print("\n".join([" ".join(row) for row in mat ]))

    @abc.abstractmethod
    def solve(self, goal_state):
        pass

class DFSSovler(Solver):
    def __init__(self, start_state):
        super().__init__(start_state)

    def solve(self, goal_state):
        return self._solver(self.start_state, self.start_state, goal_state)

    def _solver(self, prev_state, start_state, goal_state, depth = 0):
        start_pos = self.findPos(start_state)
        prev_pos = self.findPos(prev_state)

        self.states_q += 1
        self.path.append(start_state)

        if self.is_states_equal(start_state, goal_state):
            #print("solved")
            print("\n\n".join(["\n".join([" ".join(row) for row in mat ]) for mat in self.path]))
            print("States enqueued : ", self.states_q)
            print("Moves taken: ", len(self.path) - 1)
            return True

        if depth < MAX_SEARCH_DEPTH:
            (x,y) = start_pos
            for new_pos in self.get_options(start_pos, prev_pos):
                new_state = copy.deepcopy(start_state)
                # swap based on move
                temp = new_state[x][y]
                new_state[x][y] = new_state[new_pos[0]][new_pos[1]]
                new_state[new_pos[0]][new_pos[1]] = temp

                if self._solver(start_state, new_state, goal_state, depth=depth + 1):
                    return True
                
        self.path.pop()
        return False


class IDSSovler(Solver):

    def __init__(self, start_state):
        super().__init__(start_state)

    def flippy(self, state, depth):
        if depth <= 1:
            return [state]
        # find parent 
        # if no parent
        # else return list + 
        else:
            parent = [y for x,y in self.states_queue[depth] if self.is_states_equal(x, state)][0]
            b = self.flippy(parent, depth - 1) 
            b.append(state)
            return b

    def solve(self, goal_state):
        depthlimit = 1
        self.states_queue = { 1: [(self.start_state, self.start_state)] }
        self.states_q += 1

        while len(self.states_queue) > 0 and depthlimit < MAX_SEARCH_DEPTH:

            depthlimit += 1
            self.states_queue[depthlimit] = list()

            for child, parent in self.states_queue[depthlimit - 1]:
                if self._solver(self.states_queue[depthlimit], child, parent, goal_state, depthlimit):
                    # here is where you have to trace the 
                    # leaf nodes to find the path                        
                    #print("solved")
                    self.path = self.flippy(child, depthlimit - 1)
                    print("\n\n".join(["\n".join([" ".join(row) for row in mat ]) for mat in self.path]))
                    print("States enqueued : ", self.states_q)
                    print("Moves taken: ", len(self.path) - 1)
                    return True

        return False

    def _solver(self, states_queue, start_state, parent_state, goal_state, depthlimit, depth = 0):
        start_pos = self.findPos(start_state)
        prev_pos = self.findPos(parent_state)

        if self.is_states_equal(start_state, goal_state):
            return True

        if depth < depthlimit:
            (x,y) = start_pos
            for new_pos in self.get_options(start_pos, prev_pos):
                new_state = copy.deepcopy(start_state)
                # swap based on move
                temp = new_state[x][y]
                new_state[x][y] = new_state[new_pos[0]][new_pos[1]]
                new_state[new_pos[0]][new_pos[1]] = temp

                states_queue.append((new_state, start_state))
                self.states_q += 1
                
        return False

class astar1Sovler(Solver):
    def __init__(self, start_state):
        super().__init__(start_state)

    def solve(self, goal_state):
        pass
        

class astar2Sovler(Solver):
    def __init__(self, start_state):
        super().__init__(start_state)

    def solve(self, goal_state):
        pass
    
def get_start(directory):
    start_state = []
    for _ in range(3):
        start_state.append([])

    with open(directory) as start_state_file:
        for k,v in enumerate(start_state_file.read().split()):
            start_state[k // 3].append(v)

    return start_state

if __name__ == "__main__":

    (_, algorithm_name, input_file_path) = argv

    start_state = get_start(input_file_path)
    goal_state = np.array([['7','8','1'],['6','*','2'],['5','4','3']])
    
    #Testers keep commented
    #One move tester
    #goal_state = np.array([['6','7','1'],['8','2','*'],['5','4','3']])
    #Hardest problem tester
    #goal_state = np.array([['3','4','5'],['2','*','6'],['1','8','7']])
    if algorithm_name == "DFS":
        solver = DFSSovler(start_state)
        if not solver.solve(goal_state):
            print("No solution found")
    elif algorithm_name == "IDS":
        solver = IDSSovler(start_state)
        if not solver.solve(goal_state):
            print("No solution found")
    elif algorithm_name == "astar1":
        solver = astar1Sovler(start_state)
        if not solver.solve(goal_state):
            print("No solution found")
    elif algorithm_name == "astar2":
        solver = astar2Sovler(start_state)
        if not solver.solve(goal_state):
            print("No solution found")


    # print(input_state)
    # print('\n')
    # print(goal_state)

