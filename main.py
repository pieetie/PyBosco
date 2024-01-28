#!/usr/bin/python3
import numpy as np
import matplotlib.pyplot as plt 
import matplotlib.animation as animation

N = 100 #taille de la grille (size)
ON = 255
OFF = 0

PAUSE = False #contrôle de la pause

def on_key_press(event):
    global PAUSE
    if event.key == 'p':
        PAUSE = not PAUSE

def add_color(grid):
    '''
    Ajoute de la couleur aux cellules (add color)
    Cool colors : https://pigment.shapefactory.co/?d=0&s=0&a=DE2D43&b=E5E3E8
    '''
    color_grid = np.zeros((grid.shape[0], grid.shape[1], 3), dtype=np.uint8)
    color_grid[grid == ON] = np.array([222, 45, 67])
    color_grid[grid == OFF] = np.array([253, 253, 254])
    return color_grid

def update(frameNum, img, grid, N):
    '''
    Fonction update (update function)
    '''
    global PAUSE
    if PAUSE:
        return img,
    nouvGrid = grid.copy()
    for a in range(N):
        for b in range(N):
            total = int((grid[a,(b-1)%N]+grid[a,(b+1)%N]+grid[(a-1)%N,b]+grid[(a+1)%N,b]+grid[(a-1)%N,(b-1)%N]+grid[(a-1)%N,(b+1)%N]+grid[(a+1)%N,(b-1)%N]+grid[(a+1)%N,(b+1)%N])/255)
            if grid[a, b]  == ON:
                if (total < 2) or (total > 3):
                    nouvGrid[a,b] = OFF
            else:
                if total == 3:
                    nouvGrid[a,b] = ON

    img.set_data(add_color(nouvGrid))
    grid[:] = nouvGrid[:]
    return img,

def main():
    '''
    Fonction principale (main function)
    '''
    global PAUSE
    vals = [ON, OFF]
    grid = np.random.choice(vals, N*N, p=[0.2, 0.8]).reshape(N,N) #génération de départ aleatoire (random generation)

    #animation
    fig, ax = plt.subplots()

    #enlever les axes (remove axes) - visuellement (visually)
    #ax.axis('off')
    #ax.set_xticks([])
    #ax.set_yticks([])

    img = ax.imshow(add_color(grid), interpolation='nearest')

    ani = animation.FuncAnimation(fig,update,fargs=(img,grid,N,),frames= 10,interval= 60)

    #pause/play
    fig.canvas.mpl_connect('key_press_event', on_key_press)

    plt.show()
    return ani
  
if __name__ == "__main__":
    main()