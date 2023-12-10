# visualizing_matrix

## Introduction
Inspired by the YouTube channel “3blue1brown”, I decided to use python and matplotlib to make a simple script that can help with the visualization of matrix transformations. 

The script is called *matrix_visualizer*. It accepts a 2 × 2 matrix and visualizes its effect on the coordinate system (gridlines), the basis vectors, and any other random vectors. In this repo, I will demonstrate the matrix_visualizer with a brief introduction of matrices, and examples of classic geometric transformations by matrices. I may add a few more use cases of the matrix_visualizer in the future but viewer are welcomed to download the module and try for themselves.

At the core of this module is the matrix_transformation class, which includes fit, transform, plot_basis, remove_basis, and clear_vectors functions. The fit function accepts a 2 × 2 matrix as input, and plots the 2D space before and after applying the matrix with corresponding basis vectors **i** and **j**. The transform function takes a list of 2D vectors, plots them, and plots the corresponding vectors that are mapped by the matrix. The user can remove the basis for better visualization, and clear the vectors without having to create a new class instance.

## Class matrix_transformation()
### Parameters: None
### Attributes:
**matrix_**: the 2 × 2 matrix used in fit method.<br />
**det_**: the determinant of the matrix.<br />
**fig_**: the figure on which axs reside.<br />
**axs_**: canvases where all the vectors, gridlines are plotted.<br />
**basis_artists_**: list of artists including the quivers and annotations drawn during plot_basis.<br />
**vector_artists_**: list of artists including the quivers and annotations drawn during transform.
### Methods: 
`fit(matrix = np.array([[1, 0], [0, 1]]), size = 5)`: draws a coordinate system with the span of `x` and `y = [-size, size]`, and basis vectors **i** and **j** on the left; draws the transformed coordinate system and the transformed basis vectors on the right.<br />
`transform(vectors)`: draws vectors on the original space and transformed vectors on the transformed space.<br />
`remove_basis()`: erases the basis vectors from both the original and transformed spaces.<br />
`clear_vectors()`: erases vectors from both the original and transformed spaces.<br />
`plot_basis()`: plots the original and transformed basis vectors.
### Helper functions:
`plot_base(size = 5)`: creates a figure and two axes, and plots two identical coordinate systems side by side with the span of `x` and `y = [-size, size]`, returns figure and axes.<br />
`plot_fx(X, Y, intercept = 0, ax = None, size = 5)`: plots `Y` as a function of `X`, returns axes.<br />
`plot_fy(X, Y, intercept = 0, ax = None, size = 5)`: plots `X` as a function of `Y`, returns axes.<br />
`plot_vectors(vectors, ax = None)`: plots vectors as quiver objects and annotates the data points around the heads of the quivers, for all-zero vectors a point (line 2D object) is plotted instead, returns axes and artist_list.<br />

