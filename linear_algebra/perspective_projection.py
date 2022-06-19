import pygame,sys
from math import *
import numpy as np

FPS = 60

points = []
bounds = (3,1)
for x in bounds:
    for y in bounds:
        for z in (0,2):
            points.append(np.matrix([x,y,z,1]))

projection_matrix = [
    [],
    [],
    [],
    []
]

projected_points = [
    [n,n] for n in range(len(points))
]

pygame.init()
clock = pygame.time.Clock()

WIDTH,HEIGHT = 1000,800
SCALE = 100;
CENTER = [WIDTH/2,HEIGHT/2]
angle = 0
fov = pi/2

def make_perspective(fov,aspect,znear,zfar):
    # make the perspective projection matrix
    m = [
        [aspect/tan(fov/2), 0           , 0                 , 0                         ],
        [0                , 1/tan(fov/2), 0                 , 0                         ],
        [0                , 0           , zfar/(zfar-znear) , -zfar*znear/(zfar-znear)  ],
        [0                , 0           , 1                 , 0                         ]
    ]

    return m

def multiply_projection(projection_matrix,pos):
    # projection
    result = np.dot(projection_matrix,pos)

    # perspective divide
    if (result[3]!=0.0):
        result[0]/=result[3]
        result[1]/=result[3]
        result[2]/=result[3]

    return result

def rotate(angle,pos):
    rotate_x = np.matrix([
        [1,0,0,0],
        [0,cos(angle),-sin(angle),0],
        [0,sin(angle),cos(angle),0],
        [0,0,0,1]
    ])

    rotate_y = np.matrix([
        [cos(angle),0,sin(angle),0],
        [0,1,0,0],
        [-sin(angle),0,cos(angle),0],
        [0,0,0,1]
    ])

    rotate_z = np.matrix([
        [cos(angle),-sin(angle),0,0],
        [sin(angle),cos(angle),0,0],
        [0,0,1,0],
        [0,0,0,1]
    ])

    rotated2d = np.dot(rotate_z,pos)
    # rotated2d = np.dot(rotate_y,rotated2d)
    # rotated2d = np.dot(rotate_z,rotated2d)

    return rotated2d

projection_matrix = make_perspective(fov,HEIGHT/WIDTH,0,4)

WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
YELLOW = (255,255,0)

display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("cube with perspective")

def connect_points(a,b,c,d,col,points):
    pygame.draw.polygon(display,col,[(points[a][0],points[a][1]),(points[b][0],points[b][1]),(points[c][0],points[c][1]),(points[d][0],points[d][1])])
    # pygame.draw.line(display,WHITE,(points[i][0],points[i][1]),(points[j][0],points[j][1]))

while True:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
    
    display.fill(BLACK)

    angle+=0.01

    for index,point in enumerate(points):
        rotated2d = rotate(angle,point.reshape((4,1)))
        projected2d = multiply_projection(projection_matrix,rotated2d)
        x = int(projected2d[0][0]*SCALE) + CENTER[0]
        y = int(projected2d[1][0]*SCALE) + CENTER[1]
        projected_points[index] = [x,y]
        pygame.draw.circle(display,WHITE,(x,y),5)

    connect_points(1,3,7,5,YELLOW,projected_points)
    if abs(bounds[0])<abs(bounds[1]):
        connect_points(4,5,7,6,GREEN,projected_points)
        connect_points(2,3,7,6,CYAN,projected_points)
        connect_points(0,1,5,4,BLUE,projected_points)
        connect_points(0,1,3,2,RED,projected_points)
    else:
        connect_points(0,1,3,2,RED,projected_points)
        connect_points(0,1,5,4,BLUE,projected_points)
        connect_points(4,5,7,6,GREEN,projected_points)
        connect_points(2,3,7,6,CYAN,projected_points)
    connect_points(0,2,6,4,MAGENTA,projected_points)
    pygame.display.update()