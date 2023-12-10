import numpy as np
import matplotlib.pyplot as plt
from itertools import cycle
import matplotlib_inline as mi
mi.backend_inline.set_matplotlib_formats('retina')
plt.rcParams['font.family'] = 'serif'

def plot_base(size = 5):
    fig, axs = plt.subplots(1, 2, figsize = (12, 5))
    
    lim = np.array([-size, size])
    for ax in axs:
        ax.set_xlim(lim)
        ax.set_ylim(lim)
        ax.set_aspect('equal')
    half_span = np.arange(1, size + 1, 1) if size % 1 == 0 else np.arange(1, size, 1)
    line_values = np.r_[-half_span[::-1], half_span] # np.r_ concatenates slices
    for position in line_values:
        axs[0].axhline(position, 0, 1, c = '0.7', linewidth = 1)
        axs[0].axvline(position, 0, 1, c = '0.7', linewidth = 1)
        axs[1].axhline(position, 0, 1, c = '0.9', linewidth = 1)
        axs[1].axvline(position, 0, 1, c = '0.9', linewidth = 1)
    axs[0].axhline(0, 0, 1, c = '0.4')
    axs[0].axvline(0, 0, 1, c = '0.4')
    axs[1].axhline(0, 0, 1, c = '0.8')
    axs[1].axvline(0, 0, 1, c = '0.8')
    
    return fig, axs

def plot_fx(X, Y, intercept = 0, ax = None, size = 5): # plot y as a function of x, intercept on y axis
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(X, Y, c = '0.4')
    if intercept != 0: # if det == 0, 2D vector space collapses to 1D subspace, no need to plot more
        i = intercept
        k = 0 # line counter
        while min(Y) + i <= size and k <= 50:
            # if the lower-end of Y plus multiple intercepts is above the upper bound of the span
            ax.plot(X, Y + i, c = '0.7', linewidth = 1)
            ax.plot(X, Y - i, c = '0.7', linewidth = 1)
            i += intercept
            k += 1
    return ax

def plot_fy(X, Y, intercept = 0, ax = None, size = 5): # plot x as a function of y, intercept on x axis
    if ax is None:
        fig, ax = plt.subplots()
    ax.plot(X, Y, c = '0.4')
    if intercept != 0:
        i = intercept
        k = 0
        while min(X) + i <= size and k <= 50:
            # if the lower-end of X plus multiple intercepts is above the upper bound of the span
            ax.plot(X + i, Y, c = '0.7', linewidth = 1)
            ax.plot(X - i, Y, c = '0.7', linewidth = 1)
            i += intercept
            k += 1
    return ax

def plot_vectors(vectors, ax = None):
    artist_list = []
    if ax is None:
        fig, ax = plt.subplots()
    cyl = cycle(plt.rcParams['axes.prop_cycle'].by_key()['color'])
    for vector, color in zip(vectors, cyl):
        if vector[0] == vector[1] == 0:
            quiver, = ax.plot(0, 0, '.', zorder = 2) # ',' is necessary
            annotation = ax.annotate(text = '(0, 0)', xy = (0, 0), xytext = (0.2, -0.2))
        else:
            quiver = ax.quiver(0, 0, vector[0], vector[1], #quiver x location, y location, x direction, y direction
                               angles = 'xy', scale_units = 'xy', scale = 1, # settings needed to scale quiver to data
                               color = color,
                               zorder = 2) 
            # line2D has zorder of 2, to draw on top of those, need to set quiver's zorder = 2 or higher

            norm = np.sqrt(vector[0]**2 + vector[1]**2)
            text = '(' + ', '.join(str(int(x)) if x%1 == 0 else str(round(x, 2)) for x in vector) +')'
            t_x = -2.3*len(text) + 3.5*len(text)*vector[0]/norm # see note about centering and moving text boxes
            t_y = -3 + 6*vector[1]/norm
            xytext = (t_x, t_y)

            annotation = ax.annotate(text = text,
                        xy = vector, # location of the annotation
                        xycoords = 'data', # with respect of data (not axes or pixels)
                        xytext = xytext, # position of the textbox
                        textcoords = 'offset points') # w.r.t the location of annotation by offset points given by above
        artist_list.extend([quiver, annotation])
    return ax, artist_list

class matrix_transformation:
    
    def __init__(self):
        self.basis_artists_ = []
        self.vector_artists_ = []
        self.matrix_ = None
        self.det_ = None # determinant of the matrix
        self.fig_ = None
        self.axs_ = None
        
    def fit(self, matrix = np.array([[1, 0], [0, 1]]), size = 5):
        self.matrix_ = matrix
        span = np.array([-size, size])
        
        x_x = matrix[0][0]
        x_y = matrix[1][0]
        y_x = matrix[0][1]
        y_y = matrix[1][1]
        
        unit_x = np.sqrt(x_x**2 + x_y**2) #unit length
        unit_y = np.sqrt(y_x**2 + y_y**2)

        self.det_ = x_x * y_y - x_y * y_x #determinant

        if x_x == 0: #theta_x == 90
            tan_x = np.nan
            cot_x = 0
        elif x_y == 0: #theta_x == 0
            tan_x = 0
            cot_x = np.nan
        else:
            tan_x = x_y/x_x
            cot_x = x_x/x_y

        if y_y == 0: #theta_y == 90
            tan_y = np.nan
            cot_y = 0
        elif y_x == 0: #theta_y == 0
            tan_y = 0
            cot_y = np.nan
        else:
            tan_y = y_x/y_y
            cot_y = y_y/y_x
        
        self.fig_, self.axs_ = plot_base(size = size)
        
        if abs(x_x) >= abs(x_y): # 0 <= theta_x <= 45
            if x_x != 0: # won't plot X transformation if x_x == x_y == 0
                X_X = span # draw X_Y as a function of X_X
                X_Y = tan_x * X_X # tan_x is the y-over-x slope
                X_intercept = abs(y_y - y_x * tan_x) # intercept on y asix, see notes
                self.axs_[1] = plot_fx(X_X, X_Y, X_intercept, ax = self.axs_[1], size = size)
        else: # 45 < theta_x <= 90
            X_Y = span # draw X_X as a function of X_Y
            X_X = cot_x * X_Y # cot_x is the x-over-y slope
            X_intercept = abs(y_x - y_y * cot_x) # intercept on x axis, see notes
            self.axs_[1] = plot_fy(X_X, X_Y, X_intercept, ax = self.axs_[1], size = size)
        if abs(y_y) >= abs(y_x): # 0 <= theta_y <= 45
            if y_y != 0: # won't plot Y transformation if y_y == y_x == 0
                Y_Y = span # draw Y_X as a function of Y_Y
                Y_X = tan_y * Y_Y # tan_y is the x-over-y slope
                Y_intercept = abs(x_x - x_y * tan_y) # intercept on x asix, see notes
                self.axs_[1] = plot_fy(Y_X, Y_Y, Y_intercept, ax = self.axs_[1], size = size)
        else: # 45 < theta_x <= 90
            Y_X = span # draw X_X as a function of X_Y
            Y_Y = cot_y * Y_X # cot_y is the y-over-x slope
            Y_intercept = abs(x_y - x_x * cot_y) # intercept on y axis, see notes
            self.axs_[1] = plot_fx(Y_X, Y_Y, Y_intercept, ax = self.axs_[1], size = size)
        
        self.remove_basis()
        self.clear_vectors()
        self.plot_basis()
            
    def plot_basis(self):
        if len(self.basis_artists_) == 0:
            for vector, color, name in zip(np.array([[1, 0], [0, 1]]), ['r', 'b'], ['i', 'j']):
                quiver = self.axs_[0].quiver(0, 0, vector[0], vector[1], 
                                            angles = 'xy', scale_units = 'xy', scale = 1,
                                            color = color, zorder = 2)
                t_x = -2 + 4*vector[0]
                t_y = -4 + 10*vector[1]
                xytext = (t_x, t_y)
                annotation = self.axs_[0].annotate(name, xy = vector, xycoords = 'data', 
                                                  xytext = xytext, textcoords = 'offset points',
                                                  color = color, fontsize = 14, fontweight = 'bold', fontstyle = 'italic')
                self.basis_artists_.extend([quiver, annotation])

            new_i = np.matmul(self.matrix_, [1, 0])
            new_j = np.matmul(self.matrix_, [0, 1])
            for vector, color, name in zip(np.array([new_i, new_j]), ['r', 'b'], ['i', 'j']):
                if vector[0] == vector[1] == 0:
                    quiver, = self.axs_[1].plot(0, 0, '.', color = color, zorder = 2)
                    annotation = self.axs_[1].annotate(text = name, xy = (0, 0), xytext = (0.2, -0.2),
                                                      color = color, fontsize = 14, fontweight = 'bold', fontstyle = 'italic')
                else:
                    quiver = self.axs_[1].quiver(0, 0, vector[0], vector[1], 
                                                angles = 'xy', scale_units = 'xy', scale = 1,
                                                color = color, zorder = 2)
                    norm = np.sqrt(vector[0]**2 + vector[1]**2)
                    t_x = -2 + 4*vector[0]/norm
                    t_y = -4 + 10*vector[1]/norm
                    xytext = (t_x, t_y)
                    annotation = self.axs_[1].annotate(name, xy = vector, xycoords = 'data', 
                                                      xytext = xytext, textcoords = 'offset points',
                                                      color = color, fontsize = 14, fontweight = 'bold', fontstyle = 'italic')
                self.basis_artists_.extend([quiver, annotation])
            return self.fig_
    
    def remove_basis(self):
        if len(self.basis_artists_) > 0:
            for artist in self.basis_artists_:
                artist.remove()
            self.basis_artists_ = []
            return self.fig_
            
    def transform(self, vectors):
        if not isinstance(vectors[0], (np.ndarray, list)):
            vectors = np.array([vectors])
        ax, artist_list = plot_vectors(vectors, ax = self.axs_[0])
        self.vector_artists_.extend(artist_list)
        
        new_vectors = np.array([np.matmul(self.matrix_, vector) for vector in vectors])
        ax, artist_list = plot_vectors(new_vectors, ax = self.axs_[1])
        self.vector_artists_.extend(artist_list)
        return self.fig_
    
    def clear_vectors(self):
        if len(self.vector_artists_) > 0:
            for artist in self.vector_artists_:
                artist.remove()
            self.vector_artists_ = []
            return self.fig_
