
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
    ##         Rule 1

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
                        if(in_warehouse(warehouse,x,y) and not target_warehouse(warehouse,x,y)):      
                            taboo_list.append((x,y))
                #check down
                if((x, y+1) in walls_list):
                     if((x, y) not in walls_list):
                        #check not a wall
                       if(in_warehouse(warehouse,x,y) and not target_warehouse(warehouse,x,y)): 
                            taboo_list.append((x,y))

            if((x + 1, y) in walls_list):
                #check right
                if((x, y-1) in walls_list):
                    #check top
                    if((x,y) not in walls_list):
                        #check not a wall
                        if(in_warehouse(warehouse,x,y) and not target_warehouse(warehouse,x,y)): 
                            taboo_list.append((x,y))
                if((x, y+1) in walls_list):
                    #check down
                    if((x,y) not in walls_list):
                        #check not a wall
                        if(in_warehouse(warehouse,x,y) and not target_warehouse(warehouse,x,y)): 
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
                    if(target_warehouse(warehouse, z[0], y)):
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
                   if(target_warehouse(warehouse, y, z[1])):
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
        wh_string += "\n"
        for i in range(warehouse.ncols):
            if((i, z) in walls_list):
                wh_string += "#"
            elif ((i, z) in taboo_list_copy):
                    wh_string += "X"
            else:
                wh_string += " "

                    
    print(wh_string)
    print("\n")
    return(wh_string)    
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
        
        return None

    def actions(self, warehouse):
        """
        Return the list of actions that can be executed in the given state.
        
        """
        worker = warehouse.worker
        L = []
        if (worker[0], worker[1]+1) not in warehouse.walls:
            #down is not a wall
            L.append("Down")
        if (worker[0], worker[1]-1) not in warehouse.walls:
            #up is not a wall
            L.append("Up")
        if (worker[0]-1, worker[1]) not in warehouse.walls:
            #left is not a wall
            L.append("Left")
        if (worker[0]+1, worker[1]) not in warehouse.walls:
            #right is not a wall
            L.append("Right")
        return L

    def result(self, warehouse, action):
        cloned_warehouse = warehouse.copy()
        worker = warehouse.worker
        if action == "Down":
            if(action in self.actions(warehouse)):
                warehouse.worker = (worker[0], worker[1]+1)
        if action == "Up":
            if(action in self.actions(warehouse)):
                warehouse.worker = (worker[0], worker[1]-1)
        if action == "Left":
            if(action in self.actions(warehouse)):
                warehouse.worker = (worker[0]-1, worker[1])
        if action == "Right":
            if(action in self.actions(warehouse)):
                warehouse.worker = (worker[0]+1, worker[1])
        return warehouse


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

    cloned = warehouse.copy()
    boxes = cloned.boxes
    worker = cloned.worker
    walls = cloned.walls
    (x,y) = worker
    boxno = 0
    boxFound = False


    for action in action_seq:
        #check which action is taken
        if action == "Left":
            boxFound = False
            #check for boxes next to worker
            for box in boxes:
                #if box not found add to counter
                if ((x-1,y) != box):
                    boxno += 1
                elif ((x-1, y) == box):
                    # if box found change to true no box statement skips
                    boxFound = True
                    # check if box collides with box
                    for box in boxes:
                        if((x-2,y) == box):
                            return print('impossible')
                    # check if box collides with wall
                    for wall in walls:
                        if((x-2,y) == wall):
                            return print('impossible')
                # save coord information for box one and player
                    boxes[boxno] = (x-2,y)
                    (x,y) = (x,y)
                    boxno = 0
                    break

            if boxFound != True:
                # check if player collides with wall
                for wall in walls:
                    if((x-1,y) == wall):
                        return print('impossible')
            # if no wall hit detected record coords
            (x,y) = (x-1,y)
            boxno = 0

        elif action == "Right":
            boxFound = False
            #check for boxes next to worker
            for box in boxes:
                #if box not found add to counter
                if ((x+1,y) != box):
                    boxno += 1
                elif ((x+1, y) == box):
                    # if box found change to true no box statement skips
                    boxFound = True
                    # check if box collides with box
                    for box in boxes:
                        if((x+2,y) == box):
                            return print('impossible1')
                    # check if box collides with wall
                    for wall in walls:
                        if((x+2,y) == wall):
                            return print('impossible2')
                # save coord information for box one and player
                    boxes[boxno] = (x+2,y)
                    (x,y) = (x+1,y)
                    boxno = 0
                    break

            if boxFound != True:
                # check if player collides with wall
                for wall in walls:
                    if((x+1,y) == wall):
                        return print('impossible3')
            # if no wall hit detected record coords
            (x,y) = (x+1,y)

        elif action == "Up":
            boxFound = False
            #check for boxes next to worker
            for box in boxes:
                #if box not found add to counter
                if ((x,y-1) != box):
                    boxno += 1
                elif ((x, y-1) == box):
                    # if box found change to true no box statement skips
                    boxFound = True
                    # check if box collides with box
                    for box in boxes:
                        if((x,y-2) == box):
                            return print('impossible')
                    # check if box collides with wall
                    for wall in walls:
                        if((x,y-2) == wall):
                            return print('impossible')
                # save coord information for box one and player
                    boxes[boxno] = (x,y-2)
                    (x,y) = (x,y-1)
                    boxno = 0
                    break

            if boxFound != True:
                # check if player collides with wall
                for wall in walls:
                    if((x,y-1) == wall):
                        return print('impossible')
            # if no wall hit detected record coords
            (x,y) = (x,y-1)
            boxno = 0

        elif action == "Down":
            boxFound = False
            #check for boxes next to worker
            for box in boxes:
                #if box not found add to counter
                if ((x,y+1) != box):
                    boxno += 1
                elif ((x, y+1) == box):
                    # if box found change to true no box statement skips
                    boxFound = True
                    # check if box collides with box
                    for box in boxes:
                        if((x,y+2) == box):
                            return print('impossible')
                    # check if box collides with wall   
                    for wall in walls:
                        if((x,y+2) == wall):
                            return print('impossible')
                # save coord information for box one and player
                    boxes[boxno] = (x,y+2)
                    (x,y) = (x,y+1)
                    boxno = 0
                    break

            if boxFound != True:
                # check if player collides with wall
                for wall in walls:
                    if((x,y+1) == wall):
                        return print('impossible')
            # if no wall hit detected record coords
                (x,y) = (x,y+1)
                boxno = 0

        else:
            return print("Action is invalid.")

    ##         "INSERT YOUR CODE HERE"
    worker = (x,y)
    output = warehouse.copy(worker, boxes)
    return print(output)

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
    taboos = taboo_cells(wh)
    
    return "test"
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

if __name__ == "__main__":
    wh = sokoban.Warehouse();
    wh.load_warehouse("./warehouses/warehouse_19.txt")
    
    solve_weighted_sokoban(wh)

    print(dir(wh))
    print(wh.worker)
    print(wh)
    sokoban = SokobanPuzzle(wh)
    print(sokoban.actions(wh))
    print(sokoban.result(wh, "Up"))
    # print(f"cols {wh.ncols}")
    # print(f"rows {wh.nrows}")
    # taboo_cells(wh)

    # print(wh)
    # print(target_warehouse(wh, 4, 4))