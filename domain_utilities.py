# functions needed for wetropolis domain

def river_section_param_construct(A, depth, x_low, x_up, y_low, y_up, Nx, Ny, X_max, Y_max):
    '''
    In this function we will be editing the domain matrix A in the region between the 
    lower and upper x and y values and changing the matrix to a depth, depth. Nx and Ny 
    the discretisation variables for the number of points required.

    Input

    Output

    '''
    #TODO: Insert check to make sure that x_low < x_up etc??
    for xx in range(x_low, x_up):
        for yy in range(y_low, y_up):
            xj = int(Nx*xx/X_max)
            yj = int(Ny*yy/Y_max)

            A[yj, xj] = depth

    return A 