#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation
import scipy.signal

N = 50 #taille de la grille (size)
x, y = 20, 20 #position du motif au départ (pattern position)
ON = 1
OFF = 0

PAUSE = False #contrôle de la pause

def on_key_press(event):
    global PAUSE
    if event.key == 'p':
        PAUSE = not PAUSE

#motifs (patterns)
pattern = {}
pattern["bosco"] = {"name":"Bosco","R":5,"b1":34,"b2":45,"s1":34,"s2":58,
  "cells":[[0,0,0,1,1,1,0,0,0,0], 
           [0,0,1,1,1,1,1,1,0,0], 
           [0,1,0,0,1,1,1,1,1,1], 
           [1,0,0,0,0,1,1,1,1,1], 
           [1,0,0,0,0,0,1,1,1,1], 
           [1,1,0,0,0,0,1,1,1,1], 
           [1,1,1,1,0,1,1,1,1,1], 
           [1,1,1,1,1,1,1,1,1,0], 
           [0,1,1,1,1,1,1,1,0,0], 
           [0,0,1,1,1,1,1,0,0,0], 
           [0,0,0,1,1,1,0,0,0,0]]
}

def add_color(grid):
    '''
    Ajoute de la couleur aux cellules (add color)
    Cool colors : https://pigment.shapefactory.co/?d=0&s=0&a=DE2D43&b=E5E3E8
    '''
    color_grid = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
    color_grid[grid == ON] = np.array([222, 45, 67])
    color_grid[grid == OFF] = np.array([253, 253, 254])
    return color_grid

def main():
    '''
    Fonction principale (main function)
    '''
    global PAUSE
    grid = np.zeros((N, N), dtype=int) #initialisation de la grille (grid initialization)
    params = pattern["bosco"] #paramètres du motif (pattern parameters)
    globals().update(params)

    C = np.asarray(params['cells'])
    grid[x:x+C.shape[0], y:y+C.shape[1]] = C

    # Appliquer la couleur dès le début
    colored_grid = add_color(grid)

    K = np.ones((2*params['R']+1, 2*params['R']+1)) #noyau (kernel)

    #animation
    fig, ax = plt.subplots()

    img = ax.imshow(colored_grid, interpolation='nearest', cmap='binary')

    def growth(U):
        '''
        Règle de croissance (growth rule)
        '''
        return 0 + ((U >= params['b1']) & (U <= params['b2'])) - ((U < params['s1']) | (U > params['s2']))

    def update(i):
        '''
        Mise à jour de la grille (grid update)
        '''
        nonlocal grid
        if PAUSE:
            return img, 
        U = scipy.signal.convolve2d(grid, K, mode='same', boundary='wrap')
        grid = np.clip(grid + growth(U), 0, 1).astype(int)
        colored_grid = add_color(grid)
        img.set_array(colored_grid)
        return img,

    ani = animation.FuncAnimation(fig, update, frames=200, interval=50)

    #pause/play
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    plt.show()
    return ani

if __name__ == "__main__":
    main()