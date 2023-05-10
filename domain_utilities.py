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

def create_exit_curve(A, coeff, river_depth, N_disc, Nx, Ny):
    '''
    In this function we will compute the exit curve and model it as the curve y =-tan(x)
    for a range of angles x.
    '''

    x_range = np.linspace(coeff['Exit curve x linspace'][0],
                    coeff['Exit curve x linspace'][1], N_disc)
    
   
    y_low = int(Ny*coeff['Exit curve y range'][0])
    y_up = int(Ny*coeff['Exit curve y range'][1])



    c_horz = Ny*coeff['Horizontal scaling coeff']/np.max(x_range)
    c_vert = Nx*coeff['Vertical shift coeff']/np.tan(np.max(x_range))

    x_pos_min = int(np.floor(Nx*coeff['Exit curve x range'][0]))
    x_pos_max = int(np.floor(Nx*coeff['Exit curve x range'][1]))

    for xx in x_range:
        for y_pos in range(y_low, y_up):
                for x_pos in range(x_pos_min, x_pos_max):
                    xj = int(x_pos + c_vert*np.tan(xx))
                    yj = int(y_pos + xx*c_horz)

                    #     
                    if xj < Nx:  
                        A[yj, xj] = river_depth

    return A



def create_wetropolis_DtM(X_disc, Y_disc, coeff, river_depth, FP_depth, north_town_depth, 
                          south_town_depth, N_circle, N_disc, slope):
    '''
    In this function we will produce a matrix of the wetropolis given the coefficients for 
    any given discetisation (X_disc, Y_disc).

    Inputs:

    Outputs:
        A, the matrix reresenting the Wetropolis

    '''
    # initialising matrix
    A = np.ones((Y_disc, X_disc))
 
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
    
    # adding town
    # north
    create_river_section(A, north_town_depth, coeff['Town north x range'], 
                         coeff['Town north y range'], X_disc, Y_disc)

    #south
    create_river_section(A, south_town_depth, coeff['Town south x range'], 
                         coeff['Town south y range'], X_disc, Y_disc)
    
    # exit curve

    create_exit_curve(A, coeff, river_depth, N_disc, X_disc, Y_disc)


    # now adding the slope on the whole domain

    basic_slope = np.linspace(0, -slope, Y_disc)

    for count, value in enumerate(basic_slope):
        A[count, :] = A[count, :] + value  

      
    return A

def matrix_to_ascii(mat, xll, yll, dx, fname, extension):
    '''
    This is mainly pseudocode, describing roughly how this is done.
    In this function we are converting a matrix to an ascii file.

    Attempting to follow guidance from:
    https://www.loc.gov/preservation/digital/formats/fdd/fdd000422.shtml

    Inputs:
        mat, the matrix we want to convert
        xll, the lower left corner x coordinate (should be 0 due to construction of problem)
        yll, the lower left corner y coordinate (should be 0 due to construction of problem)
        dx, step size
        fname, filename for new ascii file
        extension, always .asc ??

    Outputs:
        asciifile, the matrix in ascii form! 
    '''
    ncols, nrows = np.shape(mat)  # discretisation in y and x direction.
    temp_file = np.array(np.shape(mat)) # initialising the size

    # temp_file = fname + extension  ## TODO: How do you add an extension to the file name, or is this done at the end???

    # unbsure correct way of adding here
    # Here we want to write the header
    header = 'fptr', 'isflt', nrows, ncols, -100, xll, yll, 'dx', 'use_edge_cell', 'format'
    with open(temp_file, 'w') as file:
        file.write(header + '\n')

    
    # Now we want to add the data, work from the top and go down
    # Now I think we need to read each line of the empty asdii file

    j = 0 # counter for counting down the rows.
    with open(temp_file, 'w') as file:
        for line in file:
            
            line.write(str(mat[:, nrows-j])) # add line by information from matrix to ascii file
            j +=1