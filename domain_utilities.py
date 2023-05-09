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
    x_low, x_up = int( Nx*x_range[0]), int(Nx*x_range[1])
    y_low, y_up = int( Ny*y_range[0]), int(Ny*y_range[1])
    for xx in range(x_low, x_up):
        for yy in range(y_low, y_up):

            A[yy, xx] = depth

    return A

def create_curve_section(A, depth, centre, radius, angle, Nx, Ny, N_circle):
    '''
    In this function we will add in the curved sections

    Input:

    Output:

    Assumptions:
    '''

    # centre of circle:
    a, b = Nx*centre[0], Ny*centre[1]
    theta_range = np.linspace( angle[0], angle[1], N_circle )
    r_range = np.linspace(radius[0], radius[1], N_circle)

    for r in r_range:
        for theta in theta_range:

            xx = a + Nx*r*np.cos(theta)
            yy = b + Ny*r*np.sin(theta)

            A[int(np.ceil(yy)), int(np.ceil(xx))] = depth
            A[int(np.floor(yy)), int(np.floor(xx))] = depth
            A[int(np.ceil(yy)), int(np.floor(xx))] = depth
            A[int(np.floor(yy)), int(np.ceil(xx))] = depth 

    return A





def create_wetropolis_DtM(X_disc, Y_disc, coeff, river_depth, FP_depth, N_circle):
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
    create_river_section(A, river_depth, coeff['River section 1 x range'], 
                         coeff['River section 1 y range'], X_disc, Y_disc)
    # river section 2
    create_river_section(A, river_depth, coeff['River section 2 x range'], 
                         coeff['River section 2 y range'], X_disc, Y_disc)
    # river section 3
    create_river_section(A, river_depth, coeff['River section 3 x range'], 
                         coeff['River section 3 y range'], X_disc, Y_disc)
    # river section 4
    create_river_section(A, river_depth, coeff['River section 4 x range'], 
                         coeff['River section 4 y range'], X_disc, Y_disc)
    
    # computing the flood plane sections
    # FP section 1
    create_river_section(A, FP_depth, coeff['FP section 1 x range'], 
                         coeff['FP section 1 y range'], X_disc, Y_disc)
    # FP section 2
    create_river_section(A, FP_depth, coeff['FP section 2 x range'], 
                         coeff['FP section 2 y range'], X_disc, Y_disc)
    # FP section 3
    create_river_section(A, FP_depth, coeff['FP section 3 x range'], 
                         coeff['FP section 3 y range'], X_disc, Y_disc)
    # FP section 4
    create_river_section(A, FP_depth, coeff['FP section 4 x range'], 
                         coeff['FP section 4 y range'], X_disc, Y_disc)


    # computing the curves
    # Rivers
    # curve 1
    create_curve_section(A, river_depth, coeff['Curve 1 centre'], 
                         coeff['Curve 1 river radius range'], 
                         coeff['Curve 1 theta range'], X_disc, 
                         Y_disc, N_circle)
    
    # curve 2
    create_curve_section(A, river_depth, coeff['Curve 2 centre'], 
                         coeff['Curve 2 river radius range'], 
                         coeff['Curve 2 theta range'], X_disc, 
                         Y_disc, N_circle)
    
    # curve 3
    create_curve_section(A, river_depth, coeff['Curve 3 centre'], 
                         coeff['Curve 3 river radius range'], 
                         coeff['Curve 3 theta range'], X_disc, 
                         Y_disc, N_circle)

    # Flood plains
    # curve 1
    create_curve_section(A, FP_depth, coeff['Curve 1 centre'], 
                         coeff['Curve 1 FP radius range'], 
                         coeff['Curve 1 theta range'], X_disc, 
                         Y_disc, N_circle)
    
    # curve 2
    create_curve_section(A, FP_depth, coeff['Curve 2 centre'], 
                         coeff['Curve 2 FP radius range'], 
                         coeff['Curve 2 theta range'], X_disc, 
                         Y_disc, N_circle)
    
    # curve 3
    create_curve_section(A, FP_depth, coeff['Curve 3 centre'], 
                         coeff['Curve 3 FP radius range'], 
                         coeff['Curve 3 theta range'], X_disc, 
                         Y_disc, N_circle)

    return A