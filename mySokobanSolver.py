
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
import search 
import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    
    '''
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    return [(10464174, 'Constantine', 'Aspromourgos')]
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
    ##If a cell is in a corner and not a target it is taboo

    walls_list = []
    walls_list = warehouse.walls.copy()
    taboo_list = []
    for row in range(warehouse.ncols):
        for col in range(warehouse.nrows):
            if((row-1, col) in walls_list):
                    #check left
                if((row, col-1) in walls_list):
                    #check top
                    if((row, col) not in walls_list):
                        #check not a wall

                        if(in_warehouse(warehouse,row,col) and not target_warehouse(warehouse,row,col)):      
                            taboo_list.append((row,col))
                #check down
                if((row, col+1) in walls_list):
                     if((row, col) not in walls_list):
                        #check not a wall
                       if(in_warehouse(warehouse,row,col) and not target_warehouse(warehouse,row,col)): 
                            taboo_list.append((row,col))

            if((row + 1, col) in walls_list):
                #check right
                if((row, col-1) in walls_list):
                    #check top
                    if((row,col) not in walls_list):
                        #check not a wall
                        if(in_warehouse(warehouse,row,col) and not target_warehouse(warehouse,row,col)): 
                            taboo_list.append((row,col))
                if((row, col+1) in walls_list):
                    #check down
                    if((row,col) not in walls_list):
                        #check not a wall
                        if(in_warehouse(warehouse,row,col) and not target_warehouse(warehouse,row,col)): 
                            taboo_list.append((row,col))
    
    #check for walls between taboo points if along and edge add between cells to taboo list 
    taboo_list_copy = taboo_list.copy()
    for taboo1 in taboo_list:
        for taboo2 in taboo_list:
           if(taboo1[0] == taboo2[0] and taboo1 != taboo2):
               
               l_count = 0
               r_count = 0
               d_count = 0
               u_count = 0
               
               for y in range(taboo1[1], taboo2[1]):
                    #left wall
                    if((taboo1[0]-1,y) in walls_list):
                        l_count += 1
                    #right wall
                    if((taboo1[0]+1, y) in walls_list):
                        r_count += 1
                    if(target_warehouse(warehouse, taboo1[0], y)):
                        l_count = 0
                        r_count = 0
                        
                    if(l_count == (taboo2[1]-taboo1[1])):
                        taboo_list_copy = between_two_corners_row(taboo1,taboo2,taboo_list_copy)
                    if(r_count == (taboo2[1]-taboo1[1])):
                        taboo_list_copy = between_two_corners_row(taboo1,taboo2,taboo_list_copy)
           if(taboo1[1] == taboo2[1] and taboo1 != taboo2):

               d_count = 0
               u_count = 0
               for y in range(taboo1[0], taboo2[0]):

                   #top
                   if((y, taboo1[1]+1) in walls_list):
                       u_count += 1
                   #down
                   if((y, taboo1[1]-1) in walls_list):
                       d_count += 1
                   if(target_warehouse(warehouse, y, taboo1[1])):
                        u_count = 0
                        d_count = 0
                    
                   if(d_count == (taboo2[0]-taboo1[0])):

                        taboo_list_copy = between_two_corners_col(taboo1,taboo2,taboo_list_copy)
                        
                   if(u_count == (taboo2[0]-taboo1[0])):

                        taboo_list_copy = between_two_corners_col(taboo1,taboo2,taboo_list_copy)
                       
            

    ##Make string with taboo cells marked X
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

                    

    return wh_string
def target_warehouse(warehouse,x,y):
    for i in range(len(warehouse.targets)):
        if(warehouse.targets[i] == (x, y)):
            return True
    return False
def in_warehouse(warehouse, x, y):
    rows = warehouse.ncols
    cols = warehouse.nrows

    wall_up = 0
    wall_down = 0
    wall_left = 0
    wall_right = 0

    for i in range(x, rows):
        if((i, y) in warehouse.walls):
             wall_right += 1
    for i in range(0, x):
        if((i, y) in warehouse.walls):
             wall_left += 1
    for i in range(y, cols):
        if((x, i) in warehouse.walls):
             wall_down += 1
    for i in range(0, y):
        if((x, i) in warehouse.walls):
           wall_up += 1

    if(wall_right == 0 or wall_left == 0 or wall_up == 0 or wall_right == 0):
        return False   
    return True

##Given two points add area between to taboo array (for Up and down)
def between_two_corners_row(point1, point2, taboo_list):
     taboo_list_copy = taboo_list.copy()
     for y in range(point1[1], point2[1]):
         taboo_list_copy.append((point1[0], y))
     return taboo_list_copy

##Given two points add area between to taboo array (for left and right)
def between_two_corners_col(point1, point2, taboo_list):
    taboo_list_copy = taboo_list.copy()
    for y in range(point1[0], point2[0]):
        taboo_list_copy.append((y, point1[1]))
    return taboo_list_copy

class SokobanPuzzle(search.Problem):
    '''
    An instance of the class 'SokobanPuzzle' represents a Sokoban puzzle.
    An instance contains information about the walls, the targets, the boxes
    and the worker.

    Your implementation should be fully compatible with the search functions of 
    the provided module 'search.py'. 
    
    '''
    
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
        """
        return set(self.goal) == set(state[1])

    def actions(self, state):
        """
        Return the list of all possible actions for given state
            -If action is to a taboo cell it will not be counted
        """
        wh = self.warehouse
        worker = state[0]
        boxes = state[1]
        taboo = self.taboo
        L = []

        #Case 1 check if not walls around worker
        if (worker[0], worker[1]+1) not in wh.walls:
            if not ((worker[0], worker[1]+1) in boxes and ((worker[0], worker[1]+1+1) in boxes or (worker[0], worker[1]+1+1) in wh.walls or (worker[0], worker[1]+1+1) in taboo)):
            #Case 2 check if two boxes or box is not in a taboo or wall cell
                L.append("Down")
        if (worker[0], worker[1]-1) not in wh.walls:
           #Case 2 check if two boxes or box is not in a taboo or wall cell
            if not ((worker[0], worker[1]-1) in boxes and ((worker[0], worker[1]-1-1) in boxes or (worker[0], worker[1]-1-1) in wh.walls or (worker[0], worker[1]-1-1) in taboo)):
                L.append("Up")
        if (worker[0]-1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box is not in a taboo or wall cell
            if not ((worker[0]-1, worker[1]) in boxes and ((worker[0]-1-1, worker[1]) in boxes or (worker[0]-1-1, worker[1]) in wh.walls or (worker[0]-1-1, worker[1]) in taboo)):
            #Case 2 check if two boxes or box is not in a taboo or wall cell
                L.append("Left")
        if (worker[0]+1, worker[1]) not in wh.walls:
            #Case 2 check if two boxes or box is not in a taboo or wall cell
            if not ((worker[0]+1, worker[1]) in boxes and ((worker[0]+1+1, worker[1]) in boxes or (worker[0]+1+1, worker[1]) in wh.walls or (worker[0]+1+1, worker[1]) in taboo)):
                L.append("Right")
        return L
            
            
    
    def result(self, state, action):
        'Return the state that is acheived from a given action'

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
            
            #Update box
            index = boxes_state.index(worker_state)
            boxes_state[index] = next_box_state

        #Return the new worker and box states
        return worker_state, tuple(boxes_state)

    def path_cost(self, c, state1, action, state2):

        if state1[1] != state2[1]: #A box has been pushed

            index = state1[1].index(state2[0])
            cost = self.weights[index]

            return c + cost + 1
        else: # No box has been pushed default cost is 1
            return c + 1
    

    def h(self, n):
        '''
            Return heuristic value for a given node, n
            The Value of the heuristic is the total estimated costs for each box
        '''
        boxes = n.state[1]
        
        worker = n.state[0]
        targets = self.targets
        weights = self.weights
        heuristic = 0


       
        for idx, box in enumerate(boxes):
            min = float('inf')

            distance_to_worker = abs(box[0] - worker[0]) + abs(box[1] - worker[1])
            for target in targets:
                cost = abs(box[0] - target[0]) + abs(box[1] - target[1]) * (weights[idx] + 1)
                if cost < min:
                    min = cost
            heuristic += distance_to_worker
            heuristic += min
        return heuristic


    

    
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
def test_taboo(wh_path, expected):
    print(f'Testing {wh_path}')
    start_time = time.time()
    wh = sokoban.Warehouse()    
    wh.load_warehouse(wh_path)
    answer = taboo_cells(wh)
    print('<<  test_taboo_cells >>')
    if answer==expected:
        print(' Answer as expected!  :-)')
    else:
        print('unexpected answer!  :-(\n')
        print('Expected ');print(expected)
        print('But, received ');print(answer)
    print("--- finished in %s seconds --- \n" % (time.time() - start_time))

def test_check_elem(wh_path, seq, expected):
    print(f'Testing {wh_path}')
    wh = sokoban.Warehouse()
    wh.load_warehouse(wh_path)
    solved_seq = check_elem_action_seq(wh,seq)
    print('<<  test_check_element_action_sequence >>')
    if solved_seq==expected:
        print(' Answer as expected!  :-)')
    else:
        print('unexpected answer!  :-(\n')
        print('Expected ');print(expected)
        print('But, received ');print(solved_seq)
    print("--- finished in %s seconds --- \n" % (time.time() - start_time))

def test_solve_weighted_sokoban(warehouse_path, expected_answer, expected_cost):
    print(f'Testing {warehouse_path}')
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

def solve_unit_tests():
    print("Test taboo_cells")
    test_taboo("./warehouses/warehouse_8a.txt", "   ######    \n###XXXXXX### \n#X         X#\n#X          #\n############ \n")
    test_taboo("./warehouses/warehouse_09.txt", "##### \n#  X##\n#X  X#\n##X  #\n ##X #\n  ## #\n   ###\n")
    test_taboo("./warehouses/warehouse_47.txt", "  #######  \n###XXXXX#  \n#X     X#  \n#X### #####\n#X       X#\n#XXX###XXX#\n#####X#####\n")
    test_taboo("./warehouses/warehouse_81.txt", " #####\n #XXX#\n #  X#\n##  X#\n#X  ##\n#X  ##\n##  X#\n #XXX#\n #####\n")
    test_taboo("./warehouses/warehouse_5n.txt", " #### #### \n##XX###XX##\n#X  #X#  X#\n#X       X#\n###     ###\n #XXXXXXX# \n###########\n")

    
    print("Testing check_elem_action_seq\n")
    test_check_elem("./warehouses/warehouse_09.txt", ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right','Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left'],
     "##### \n#*@ ##\n#    #\n##   #\n ##  #\n  ##*#\n   ###")
    test_check_elem("./warehouses/warehouse_47.txt", ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up',
'Up', 'Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left',
'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left',
'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Down',
'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left', 'Down', 'Left',
'Left', 'Up', 'Right', 'Right'],
     "  #######  \n###     #  \n#       #  \n# ### #####\n#  @* *   #\n#   ###   #\n##### #####")
    print("finished tests!")
    test_check_elem("./warehouses/warehouse_81.txt", ['Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Left', 'Down', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left',
'Down', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down',
'Down', 'Right', 'Down', 'Down', 'Left', 'Down', 'Down', 'Right', 'Up', 'Up', 'Up', 'Down', 'Left', 'Left', 'Up', 'Right'], " #####\n #   #\n # * #\n## * #\n# @*##\n#   ##\n##   #\n #   #\n #####")
    test_check_elem("./warehouses/warehouse_81.txt", ['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left'], "Impossible")


    print("Testing test_solve_weighted_sokoban\n")
    test_solve_weighted_sokoban("./warehouses/warehouse_8a.txt", ['Up', 'Left', 'Up', 'Left', 'Left', 'Down', 'Left', 'Down', 'Right', 'Right', 'Right', 'Up', 'Up', 'Left', 'Down', 'Right', 'Down', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right'], 431)
    test_solve_weighted_sokoban("./warehouses/warehouse_09.txt", ['Up', 'Right', 'Right', 'Down', 'Up', 'Left', 'Left', 'Down', 'Right', 'Down', 'Right', 'Left', 'Up', 'Up', 'Right', 'Down', 'Right','Down', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left', 'Down', 'Left', 'Up', 'Right', 'Up', 'Left'] , 396)
    test_solve_weighted_sokoban("./warehouses/warehouse_47.txt", ['Right', 'Right', 'Right', 'Up', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Right', 'Down', 'Down', 'Left', 'Left', 'Left', 'Left', 'Up',
'Up', 'Right', 'Right', 'Up', 'Right', 'Right', 'Right', 'Right', 'Down', 'Left', 'Up', 'Left', 'Down', 'Down', 'Up', 'Up', 'Left', 'Left',
'Down', 'Left', 'Left', 'Down', 'Down', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left',
'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Right', 'Up', 'Right', 'Down', 'Down',
'Up', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Right', 'Left', 'Left', 'Down', 'Left',
'Left', 'Up', 'Right', 'Right'], 179)
    test_solve_weighted_sokoban("./warehouses/warehouse_81.txt", ['Left', 'Up', 'Up', 'Up', 'Right', 'Right', 'Down', 'Left', 'Down', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left',
'Down', 'Left', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Right', 'Up', 'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down',
'Down', 'Right', 'Down', 'Down', 'Left', 'Down', 'Down', 'Right', 'Up', 'Up', 'Up', 'Down', 'Left', 'Left', 'Up', 'Right'], 376)
    test_solve_weighted_sokoban("./warehouses/warehouse_5n.txt", "Impossible", "None")
    test_solve_weighted_sokoban("./warehouses/warehouse_03_impossible.txt", "Impossible", "None")
    test_solve_weighted_sokoban("./warehouses/warehouse_07.txt", ['Up', 'Up', 'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Down', 'Right', 'Up', 'Down', 'Right', 'Down', 'Down', 'Left', 'Up',
'Down', 'Left', 'Left', 'Up', 'Left', 'Up', 'Up', 'Right'], 26)
    test_solve_weighted_sokoban("./warehouses/warehouse_147.txt", ['Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Down', 'Right', 'Down',
'Down', 'Left', 'Down', 'Left', 'Left', 'Up', 'Up', 'Down', 'Down', 'Right', 'Right', 'Up', 'Right', 'Up', 'Up', 'Left', 'Left', 'Left',
'Down', 'Left', 'Up', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Right', 'Right',
'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down', 'Down', 'Down', 'Right', 'Right', 'Up', 'Left',
'Down', 'Left', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Right', 'Left', 'Left', 'Left', 'Left', 'Left', 'Down',
'Down', 'Down', 'Down', 'Right', 'Down', 'Down', 'Right', 'Right', 'Up', 'Up', 'Right', 'Up', 'Left', 'Left', 'Left', 'Down', 'Left',
'Up', 'Up', 'Up', 'Left', 'Up', 'Right', 'Right', 'Right', 'Right', 'Right', 'Down', 'Right', 'Down', 'Right', 'Right', 'Up', 'Left',
'Right', 'Right', 'Up', 'Up', 'Left', 'Left', 'Down', 'Left', 'Left', 'Left', 'Left', 'Left', 'Left', 'Right', 'Right', 'Right', 'Right', 'Right',
'Right', 'Up', 'Right', 'Right', 'Down', 'Down', 'Left', 'Down', 'Left', 'Left', 'Up', 'Right', 'Right', 'Down', 'Right', 'Up', 'Left',
'Left', 'Up', 'Left', 'Left'], 521)

if __name__ == "__main__":

    start_time = time.time()
    solve_unit_tests()
    print("--- finished all tests in %s seconds --- \n" % (time.time() - start_time))

