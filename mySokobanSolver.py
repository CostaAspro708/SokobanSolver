
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
from array import array
from cgi import test
from os import stat_result
import re
from tabnanny import check
from tkinter import N
from turtle import distance
import search 
import sokoban
iteration = 0
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
def validCoord(x, y, n, m):
    if x < 0 or y < 0:
        return 0
    if x >= n or y >= m:
        return 0
    return 1

def inside_wh(wh):

    worker = wh.worker
    n = wh.nrows
    m = wh.ncols
    array_wh = [[0 for i in range(n)] for j in range(m)]
    for z in range(n):
       
        for i in range(m):
            if((i, z) in wh.walls):
                array_wh[i][z] = "#"
            elif ((i, z) == wh.worker):
                    array_wh[i][z] = "@"
            else:
                array_wh[i][z] = " "
    
    # Creating queue for bfs
    obj = []
    # Pushing pair of {x, y}
    X = worker[0]
    Y = worker[1]
    obj.append([X ,Y])


    in_wh = []
    # Marking worker as in warehouse
    in_wh.append(worker)
    # Until queue is empty
    while len(obj) > 0:

        # Extracting front pair
        coord = obj[0]
        x = coord[0]
        y = coord[1]

        # Popping front pair of queue
        obj.pop(0)

        # For Upside Pixel or Cell
        if validCoord(x + 1, y, n, m) == 1 and (x+1, y) not in in_wh and array_wh[x + 1][y] != "#":
            obj.append([x + 1, y])
            in_wh.append((x+1, y))

        # For Downside Pixel or Cell
        if validCoord(x - 1, y, n, m) == 1 and (x-1, y) not in in_wh and array_wh[x - 1][y] != "#":
            obj.append([x - 1, y])
            in_wh.append((x-1, y))
       
        # For Right side Pixel or Cell
        if validCoord(x, y + 1, n, m) == 1 and (x, y+1) not in in_wh and array_wh[x][y + 1] != "#":
            obj.append([x, y + 1])
            in_wh.append((x, y+1))
       
        # For Left side Pixel or Cell
        if validCoord(x, y - 1, n, m) == 1 and (x, y-1) not in in_wh and array_wh[x][y - 1] != "#":
            obj.append([x, y - 1])
            in_wh.append((x, y-1))
    return tuple(in_wh)

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
    ##         Rule 1

    inside_warehouse = inside_wh(warehouse)


    walls_list = []
    walls_list = warehouse.walls.copy()
    taboo_list = []
    for x in range(warehouse.ncols):
        for y in range(warehouse.nrows):
            if((x-1, y) in walls_list):
                    #check left
                if((x, y-1) in walls_list):
                    #check top
                    if((x, y) not in walls_list):
                        #check not a wall
                        #print(f"{x} , {y} has wall left and top")
                        if((x,y) in inside_warehouse and (x, y) not in warehouse.targets):      
                            taboo_list.append((x,y))
                #check down
                if((x, y+1) in walls_list):
                     if((x, y) not in walls_list):
                        #check not a wall
                       if((x,y) in inside_warehouse and (x, y) not in warehouse.targets):      
                            taboo_list.append((x,y))

            if((x + 1, y) in walls_list):
                #check right
                if((x, y-1) in walls_list):
                    #check top
                    if((x,y) not in walls_list):
                        #check not a wall
                        if((x,y) in inside_warehouse and (x, y) not in warehouse.targets): 
                            taboo_list.append((x,y))
                if((x, y+1) in walls_list):
                    #check down
                    if((x,y) not in walls_list):
                        #check not a wall
                        if((x,y) in inside_warehouse and (x, y) not in warehouse.targets): 
                            taboo_list.append((x,y))
    
    #check for walls between taboo points 
    taboo_list_copy = taboo_list.copy()
    for z in taboo_list:
        for x in taboo_list:
           if(z[0] == x[0] and z != x):
               l_count = 0
               r_count = 0
               d_count = 0
               u_count = 0
               
               for y in range(z[1], x[1]):
                    #print(f"path ({z[0]},{y})")
                    #left wall
                    if((z[0]-1,y) in walls_list):
                        l_count += 1
                    #right wall
                    if((z[0]+1, y) in walls_list):
                        r_count += 1
                    if((z[0], y) in warehouse.targets):
                        l_count = 0
                        r_count = 0
                    if(l_count == (x[1]-z[1])):
                        #print(f"we have a n x between {z} and {x}")
                        taboo_list_copy = taboo_helper_0(z,x,taboo_list_copy)
                    if(r_count == (x[1]-z[1])):
                        taboo_list_copy = taboo_helper_0(z,x,taboo_list_copy)
           if(z[1] == x[1] and z != x):
               #print(f"same row {z}, {x}")
               d_count = 0
               u_count = 0
               for y in range(z[0], x[0]):
                   #print(f"path row ({z[0]},{y})")
                   #top
                   if((y, z[1]+1) in walls_list):
                       u_count += 1
                   if((y, z[1]-1) in walls_list):
                       d_count += 1
                   if((y, z[1] in warehouse.targets)):
                        u_count = 0
                        d_count = 0

                   if(d_count == (x[0]-z[0])):
                        #print(f"we have a n x between {z} and {x}")
                        taboo_list_copy = taboo_helper_1(z,x,taboo_list_copy)
                        
                   if(u_count == (x[0]-z[0])):
                        #print(f"we have a n x between {z} and {x}")
                        taboo_list_copy = taboo_helper_1(z,x,taboo_list_copy)
                       
            

    ##Do to print new warehouse with taboo cells marked X
    wh_string = ""
    warehouse.taboo = taboo_list
    for z in range(warehouse.nrows):
       
        for i in range(warehouse.ncols):
            if((i, z) in walls_list):
                wh_string += "#"
            elif ((i, z) in taboo_list_copy):
                    wh_string += "X"
            else:
                wh_string += " "
        wh_string += "\n"

                    
    return(wh_string)    

def taboo_helper_0(point1, point2, taboo_list):
     taboo_list_copy = taboo_list.copy()
     for y in range(point1[1], point2[1]):
         taboo_list_copy.append((point1[0], y))
     return taboo_list_copy

def taboo_helper_1(point1, point2, taboo_list):
    taboo_list_copy = taboo_list.copy()
    for y in range(point1[0], point2[0]):
        taboo_list_copy.append((y, point1[1]))
    return taboo_list_copy

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

    
    def __init__(self, warehouse):
        self.warehouse = warehouse
        self.initial =  warehouse.worker, tuple(warehouse.boxes)
        self.taboo = list(sokoban.find_2D_iterator(taboo_cells(warehouse).splitlines(), "X"))
        self.goal = warehouse.targets
        self.targets = warehouse.targets
        self.weights = warehouse.weights

    def goal_test(self, state):
        """
        Return True if the state is a goal. 
        Overide the default method
        If all the boxes is in the target, return True
        """
        return set(self.goal) == set(state[1])

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        wh = self.warehouse
        worker = state[0]
        boxes = state[1]
        taboo = self.taboo
        L = []

        #Case 1 check if not walls around worker
        if (worker[0], worker[1]+1) not in wh.walls:
            if not ((worker[0], worker[1]+1) in boxes and ((worker[0], worker[1]+1+1) in boxes or (worker[0], worker[1]+1+1) in wh.walls or (worker[0], worker[1]+1+1) in taboo)):
            #Case 2 check if two boxes or box and wall 
                L.append("Down")
        if (worker[0], worker[1]-1) not in wh.walls:
           #Case 2 check if two boxes or box and wall 
            if not ((worker[0], worker[1]-1) in boxes and ((worker[0], worker[1]-1-1) in boxes or (worker[0], worker[1]-1-1) in wh.walls or (worker[0], worker[1]-1-1) in taboo)):
                L.append("Up")
        if (worker[0]-1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box and wall 
            if not ((worker[0]-1, worker[1]) in boxes and ((worker[0]-1-1, worker[1]) in boxes or (worker[0]-1-1, worker[1]) in wh.walls or (worker[0]-1-1, worker[1]) in taboo)):
            #Case 2 check if two boxes or box and wall 
                L.append("Left")
        if (worker[0]+1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box and wall 
            if not ((worker[0]+1, worker[1]) in boxes and ((worker[0]+1+1, worker[1]) in boxes or (worker[0]+1+1, worker[1]) in wh.walls or (worker[0]+1+1, worker[1]) in taboo)):
                L.append("Right")
        return L
            
            
    
    def result(self, state, action):
        global iteration
        iteration = iteration + 1
        #print(iteration)
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""

        # make a copy of the state of worker and boxes
        worker_state = state[0]
        boxes_state = list(state[1])
    
        # assume and calculate the next worker state
        if (action == "Up"):
            direction = (0, -1)
        elif (action == "Down"):
            direction = (0, 1)
        elif(action == "Left"):
            direction = (-1, 0)
        elif(action == "Right"):
            direction = (1, 0)

        worker_state = (worker_state[0] + direction[0], worker_state[1] + direction[1])

        #Check if there is a box 
        if worker_state in boxes_state:

           #Move box in same direction 
            next_box_state =  (worker_state[0] + direction[0], worker_state[1] + direction[1])
            
            #Update boxstate
            box_index = boxes_state.index(worker_state)
            boxes_state[box_index] = next_box_state

        #New State
        return worker_state, tuple(boxes_state)

    def path_cost(self, c, state1, action, state2):

        if state1[1] != state2[1]: # box is pushed
            box_index = state1[1].index(state2[0])
            box_cost = self.weights[box_index]
            return c + box_cost + 1
        else: # box is pushed
            return c + 1

    def h(self, node):
        '''
        The value of the heurtistic by Taxicab Geometry (Manhattan Distance).
        
        The sum of the manhattan distance of 
            - each box to it's nearest target
        '''
        boxes = node.state[1]
        targets = self.targets
        
        h = 0

        for box in boxes:
            distance = 0
            for target in targets:
                a = abs(box[0] - target[0]) 
                b = abs(box[1] - target[1])

                manhattan = (a + b) 
                distance += manhattan
            h += distance

        return h



    


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
def actions_seq(wh, state):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        worker = state[0]
        boxes = state[1]
        L = []

        #Case 1 check if not walls around worker
        if (worker[0], worker[1]+1) not in wh.walls:
            if not ((worker[0], worker[1]+1) in boxes and ((worker[0], worker[1]+1+1) in boxes or (worker[0], worker[1]+1+1) in wh.walls)):
            #Case 2 check if two boxes or box and wall 
                L.append("Down")
        if (worker[0], worker[1]-1) not in wh.walls:
           #Case 2 check if two boxes or box and wall 
            if not ((worker[0], worker[1]-1) in boxes and ((worker[0], worker[1]-1-1) in boxes or (worker[0], worker[1]-1-1) in wh.walls)):
                L.append("Up")
        if (worker[0]-1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box and wall 
            if not ((worker[0]-1, worker[1]) in boxes and ((worker[0]-1-1, worker[1]) in boxes or (worker[0]-1-1, worker[1]) in wh.walls)):
            #Case 2 check if two boxes or box and wall 
                L.append("Left")
        if (worker[0]+1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box and wall 
            if not ((worker[0]+1, worker[1]) in boxes and ((worker[0]+1+1, worker[1]) in boxes or (worker[0]+1+1, worker[1]) in wh.walls)):
                L.append("Right")
        return L

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
    check_seq = SokobanPuzzle(warehouse)
    state = check_seq.initial
    
    for action in action_seq:

        if(action not in actions_seq(warehouse,state)):
            return 'Impossible'
        state = check_seq.result(state, action)
    
    warehouse.worker = state[0]
    warehouse.boxes = state[1]

    return warehouse.__str__()
     

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
    # new class of SokobanPuzzle 
    my_sokoban = SokobanPuzzle(warehouse)
    # Apply astar_graph_search() to find solution
    solution = search.astar_graph_search(my_sokoban)
    
    if solution is None:
        return "Impossible","None"
    else:
        S = solution.solution()
        C = solution.path_cost
        # return solution path. 
        

    return S, C


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
import time

def test_check_elem(wh_path, expected_seq):
    wh = sokoban.Warehouse()
    wh.load_warehouse(wh_path)
    solved_seq = check_elem_action_seq(wh,expected_seq)
    print(solved_seq)

def test_solve_weighted_sokoban(warehouse_path, expected_answer, expected_cost):
    start_time = time.time()
    wh = sokoban.Warehouse()    
    wh.load_warehouse(warehouse_path)
    answer, cost = solve_weighted_sokoban(wh)
    print('<<  test_solve_weighted_sokoban >>')
    if answer==expected_answer:
        print(' Answer as expected!  :-)')
    else:
        print('unexpected answer!  :-(\n')
        print('Expected ');print(expected_answer)
        print('But, received ');print(answer)
        print('Your answer is different but it might still be correct')
        print('Check that you pushed the right box onto the left target!')
    print(f'Your cost = {cost}, expected cost = {expected_cost}')
    print("--- finished in %s seconds --- \n" % (time.time() - start_time))

def unit_tests():
    print("testing warehouse 8a")
    test_solve_weighted_sokoban("./warehouses/warehouse_8a.txt", ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right'], 431)
    print("testing warehouse 09")
    test_solve_weighted_sokoban("./warehouses/warehouse_09.txt", ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right','Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left'] , 396)
    print("testing warehouse 47")
    test_solve_weighted_sokoban("./warehouses/warehouse_47.txt", ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up',
'Up', 'Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left',
'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left',
'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Down',
'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left', 'Down', 'Left',
'Left', 'Up', 'Right', 'Right'], 179)
    #print("testing warehouse 5n")
    #test_solve_weighted_sokoban("./warehouses/warehouse_5n.txt", "Impossible", "None")
    #test_solve_weighted_sokoban("./warehouses/warehouse_07.txt", "Impossible", "None")

    print("Testing check_elem_action_seq: will display completed puzzle if valid")
    test_check_elem("./warehouses/warehouse_47.txt", ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up',
'Up', 'Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left',
'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left',
'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Down',
'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left', 'Down', 'Left',
'Left', 'Up', 'Right', 'Right'])
    test_check_elem("./warehouses/warehouse_8a.txt", ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right'])
    test_check_elem("./warehouses/warehouse_09.txt", ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right','Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left'])
    print("finished tests!")

if __name__ == "__main__":
    wh = sokoban.Warehouse()    
    wh.load_warehouse("./warehouses/warehouse_09.txt")
    #print(taboo_cells(wh))
    # tester  = inside_wh(wh)
    # for i in range(len(tester)):
    #     print(in_warehouse(wh, tester[i][0], tester[i][1]))
    unit_tests()
    # start_time = time.time()
    # print(solve_weighted_sokoban(wh))
    # print("--- finished in %s seconds --- \n" % (time.time() - start_time))
    print(check_elem_action_seq(wh, ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right',
'Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left']  ))