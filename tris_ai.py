#checks if an action is legal
def is_legal(mat, action):
    if action >= 9 or action<0:return False
    if mat[action//3][action % 3] == 0:
        return True

    return False

#checks if the game is over
def is_final_state(mat):
    end = True
    #more moves?
    for i in range(3):
        for j in range(3):
            if mat[i][j] == 0:
                end=False

    #vertical win
    for i in range(3):
        if mat[1][i] == mat[2][i] and mat[0][i] == mat[1][i] and mat[0][i] != 0:
            return True
        
    #horizontal win
    for x in mat:
        if x[0] == x[1] and x[0] == x[2] and x[0] != 0:
            return True

    #diagonal win
    if ((mat[0][0] == mat[1][1] and mat[0][0] == mat[2][2]) or (mat[0][2] == mat[1][1] and mat[1][1] == mat[2][0])) and mat[1][1] != 0:
        return True
    
    return end

#returns the utility of a state (mat)
def utility(mat):
    for x in mat:
        if x[0] == x[1] and x[0] == x[2] and x[0] != 0:   
            if x[0] == 'O':
                return 1
            else: return -1
        
    for i in range(3):
        if mat[1][i] == mat[2][i] and mat[0][i] == mat[1][i] and mat[0][i] != 0:
            if mat[0][i] == 'O':
                return 1
            else: return -1

    if ((mat[0][0] == mat[1][1] and mat[0][0] == mat[2][2]) or (mat[0][2] == mat[1][1] and mat[1][1] == mat[2][0])) and mat[1][1] != 0:
        if mat[1][1] == 'O':
            return 1
        else: return -1
    
    return 0

def max_val(mat, alpha, beta):
    if is_final_state(mat): return (utility(mat), 0)

    v = -10
    res = None
    for a in range(9):
        if is_legal(mat, a):
            mat[a//3][a%3] = 'O'
            (mval, _) = min_val(mat, alpha, beta)
            if mval > v:
                v = mval
                res = a

            mat[a//3][a%3] = 0
        
            if v >= beta : return (v, res)
            if v > alpha: alpha=v
    
    return (v, res)
        
def min_val(mat, alpha, beta):
    if is_final_state(mat): return (utility(mat), 0)

    v = 10
    res = None
    for a in range(9):
        if is_legal(mat, a):
            mat[a//3][a%3] = 'X'
            (mval, _) = max_val(mat, alpha, beta)
            if mval < v:
                v = mval
                res = a
            
            mat[a//3][a%3] = 0

            if v <= alpha: return (v, res)
            if v< beta: beta=v
    
    return (v, res)

def alpha_beta_pruning(mat):
    return max_val(mat, -10, 10)