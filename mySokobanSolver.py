
'''

    Sokoban assignment


The functions and classes defined in this module will be called by a marker script. 
You should complete the functions and classes according to their specified interfaces.

No partial marks will be awarded for functions that do not meet the specifications
of the interfaces.

You are NOT allowed to change the defined interfaces.
In other words, you must fully adhere to the specifications of the 
functions, their arguments and returned values.
Changing the interfacce of a function will likely result in a fail 
for the test of your code. This is not negotiable! 

You have to make sure that your code works with the files provided 
(search.py and sokoban.py) as your code will be tested 
with the original copies of these files. 

Last modified by 2022-03-27  by f.maire@qut.edu.au
- clarifiy some comments, rename some functions
  (and hopefully didn't introduce any bug!)

'''

# You have to make sure that your code works with 
# the files provided (search.py and sokoban.py) as your code will be tested 
# with these files
import  sokoban as warehouse
import search 
import sokoban
import random
import time



# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    return [(10464174, 'Constantine', 'Aspromourgos'), (10748849, 'Calum', 'Hathaway'), (10789511, 'Hari', 'Markonda Patnaikuni')]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A "taboo cell" is by definition
    a cell inside a warehouse such that whenever a box get pushed on such 
    a cell then the puzzle becomes unsolvable. 
    
    Cells outside the warehouse are not taboo. It is a fail to tag an 
    outside cell as taboo.
    
    When determining the taboo cells, you must ignore all the existing boxes, 
    only consider the walls and the target  cells.  
    Use only the following rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: 
        a Warehouse object with the worker inside the warehouse

    @return
       A string representing the warehouse with only the wall cells marked with 
       a '#' and the taboo cells marked with a 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE"    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
    #
    #         "INSERT YOUR CODE HERE"
    #
    #     Revisit the sliding puzzle and the pancake puzzle for inspiration!
    #
    #     Note that you will need to add several functions to 
    #     complete this class. For example, a 'result' method is needed
    #     to satisfy the interface of 'search.Problem'.
    #
    #     You are allowed (and encouraged) to use auxiliary functions and classes
   
    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
         # index of the blank
        i_blank = state.index(0)
        L = []  # list of legal actions
         # UP: if blank not on top row, swap it with tile above it
        if i_blank >= self.ncols:
            L.append('U')
        # DOWN: If blank not on bottom row, swap it with tile below it
        if i_blank < self.ncols*(self.nrows-1):
            L.append('D')
        # LEFT: If blank not in left column, swap it with tile to the left
        if i_blank % self.ncols > 0:
            L.append('L')
        # RIGHT: If blank not on right column, swap it with tile to the right
        if i_blank % self.ncols < self.ncols-1:
            L.append('R')
        return L
        raise NotImplementedError
        
    def result(self, state, action):
        """
        Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state).
        """
        # index of the blank
        next_state = list(state)  # Note that  next_state = state   would simply create an alias
        i_blank = state.index(0)  # index of the blank tile
        assert action in self.actions(state)  # defensive programming!
        # UP: if blank not on top row, swap it with tile above it
        if action == 'U':
            i_swap = i_blank - self.ncols
        # DOWN: If blank not on bottom row, swap it with tile below it
        if action == 'D':
            i_swap = i_blank + self.ncols
        # LEFT: If blank not in left column, swap it with tile to the left
        if action == 'L':
            i_swap = i_blank - 1
        # RIGHT: If blank not on right column, swap it with tile to the right
        if action == 'R':
            i_swap = i_blank + 1
        next_state[i_swap], next_state[i_blank] = next_state[i_blank], next_state[i_swap] 
        return tuple(next_state)  # use tuple to make the state hashable


    def random_state(self, s, n=20):
        """
        Returns a state reached by N random sliding actions generated by
        successor_function starting from state s
        """
        
        for i in range(n):
            a = random.choice(self.actions(s))
            s = self.result(s,a)
        return s
        




    def __init__(self,
               warehouse, goal = None, initial = None, N = 20): 
   
        if goal is None:
            self.goal = tuple(range(warehouse))
        else:
            assert set(goal)==set(range(warehouse))
            self.goal = goal
        if initial:
            self.initial = initial
        else:
            self.initial = self.random_state(self.goal, N)
        self.initial = tuple(self.initial)
        self.goal = tuple(self.goal)


        raise NotImplementedError()   

    def print_solution(self, goal_node):
        """
            Shows solution represented by a specific goal node.
            For example, goal node could be obtained by calling 
                goal_node = breadth_first_tree_search(problem)
        """
        # path is list of nodes from initial state (root of the tree)
        # to the goal_node
        path = goal_node.path()
        # print the solution
        print( "Solution takes {0} steps from the initial state\n".format(len(path)-1) )
        self.print_state(path[0].state)
        print( "to the goal state\n")
        self.print_state(path[-1].state)
        print( "Below is the sequence of moves\n")
        for node in path:
            self.print_node(node)

    def print_node(self, node):
        """Print the action and resulting state"""
        if node.action:
            print("Move "+node.action)
        self.print_state(node.state)

    def print_state(self, s):
        """Print the state s"""
        for ri in range(self.warehouse):
            print ('\t', end='')
            for ci in range(self.warehouse):
                t = s[ri*self.warehouse+ci] # tile label
                print ('  ' if t==0 else '{:>2}'.format(t),end=' ')
            print ('\n')                

    def h(self, node):
        """Heuristic for the sliding puzzle: returns 0"""
        return 0



if __name__ == "__main__":

    sp = SokobanPuzzle(warehouse, N=6)

    t0 = time.time()

    sol_ts = search.breadth_first_tree_search(sp)
    
#    sol_ts = search.depth_first_tree_search(sp)
#    sol_ts = search.iterative_deepening_search(ssp)


    t1 = time.time()
    sp.print_solution(sol_ts)

    print ("Solver took ",t1-t0, ' seconds')






                    



        

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_elem_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Impossible', if one of the action was not valid.
           For example, if the agent tries to push two boxes at the same time,
                        or push a box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_weighted_sokoban(warehouse):
    '''
    This function analyses the given warehouse.
    It returns the two items. The first item is an action sequence solution. 
    The second item is the total cost of this action sequence.
    
    @param 
     warehouse: a valid Warehouse object

    @return
    
        If puzzle cannot be solved 
            return 'Impossible', None
        
        If a solution was found, 
            return S, C 
            where S is a list of actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
            C is the total cost of the action sequence C

    '''
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

