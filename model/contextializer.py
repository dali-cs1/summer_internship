import numpy as np
import matplotlib.pyplot as plt
tree_radius = 9.5/2
def tree(array,position,scale,property):
    modifiedarray = array
    a = position[0]
    b = position[1]
    for x in range(np.shape(array)[0]):
        for y in range(np.shape(array)[1]):
            if abs((x-a)**2 + (y-b)**2) < ((tree_radius*scale)**2):
                array[x][y] = property
    return modifiedarray
def land_patch(position,scale,cab,cw,array=np.zeros((270,150))):
    cab_patch = np.zeros_like(array)
    cw_patch = np.zeros_like(array)
    for i, j, k, m in zip(position,scale,cab,cw):
        cab_patch = tree(cab_patch,i,j,k)
        cw_patch = tree(cw_patch,i,j,m)
    return cab_patch, cw_patch


