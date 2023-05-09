# functions needed for wetropolis domain
import numpy as np
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

def create_river_section(A, depth, x_range, y_range, Nx, Ny):
    '''
    In this function we will add the river section (or flood plain) at a specific depth, 
    from the coefficients for the desired discretisation Nx, Ny

    Inputs:

    Outputs:

    Assumptions:

    '''

    for xx in range(x_range):
        for yy in range(y_range):
            xj = int(Nx*xx)
            yj = int(Ny*yy)

            A[yj, xj] = depth

    return A

def create_wetropolis_DtM(X_disc, Y_disc, coeff, river_depth, FP_depth):
    '''
    In this function we will produce a matrix of the wetropolis given the coefficients for 
    any given discetisation (X_disc, Y_disc).

    Inputs:

    Outputs:
        A, the matrix reresenting the Wetropolis

    '''
    # initialising matrix
    A = np.zeros((Y_disc, X_disc))

    # computing the river sections
    # river section 1
    create_river_section(A, river_depth, coeff['River section 1 x range'], coeff['River section 1 y range'], X_disc, Y_disc)
    # river section 2
    create_river_section(A, river_depth, coeff['River section 2 x range'], coeff['River section 2 y range'], X_disc, Y_disc)
    # river section 3
    create_river_section(A, river_depth, coeff['River section 3 x range'], coeff['River section 3 y range'], X_disc, Y_disc)
    # river section 4
    create_river_section(A, river_depth, coeff['River section 4 x range'], coeff['River section 4 y range'], X_disc, Y_disc)
    
    # computing the flood plane sections
    # river section 1
    create_river_section(A, river_depth, coeff['FP section 1 x range'], coeff['FP section 1 y range'], X_disc, Y_disc)
    # river section 2
    create_river_section(A, river_depth, coeff['FP section 2 x range'], coeff['FP section 2 y range'], X_disc, Y_disc)
    # river section 3
    create_river_section(A, river_depth, coeff['FP section 3 x range'], coeff['FP section 3 y range'], X_disc, Y_disc)


    # computing the curves