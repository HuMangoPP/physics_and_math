import pygame,sys
from math import *
import numpy as np

FPS = 60

points = []
bounds = (-1,1)
for x in bounds:
    for y in bounds:
        for z in (1,3):
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
font = pygame.font.Font('../font/joystix.ttf',20)
WIDTH,HEIGHT = 800,800
SCALE = 100;
CENTER = [WIDTH/2,HEIGHT/2]
angle = 0
fov = pi/3

def debug(display, debug_msg, font):
    text = font.render(debug_msg, False, 'blue')
    text_box = text.get_rect(topleft = (100,100)).inflate(20, 20)
    display.blit(text, text_box)

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
    # apply a translation to origin before rotation
    translate_to_origin = np.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,-2],
        [0,0,0,1]
    ])
    rotated2d = np.dot(translate_to_origin,pos)

    # apply rotation
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

    rotated2d = np.dot(rotate_x,rotated2d)
    rotated2d = np.dot(rotate_y,rotated2d)
    rotated2d = np.dot(rotate_z,rotated2d)

    # apply translation back to the original position
    translate_to_pos = np.matrix([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,2],
        [0,0,0,1]
    ])
    rotated2d = np.dot(translate_to_pos,rotated2d)
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

def draw_planes(a,b,c,d,col,points):
    pygame.draw.polygon(display,col,[(points[a][0],points[a][1]),(points[b][0],points[b][1]),(points[c][0],points[c][1]),(points[d][0],points[d][1])])

def connect_points(i,j,points):
    if i==0 or j==0:
        pygame.draw.line(display,RED,(points[i][0],points[i][1]),(points[j][0],points[j][1]))
    elif i==3 or j==3:
        pygame.draw.line(display,GREEN,(points[i][0],points[i][1]),(points[j][0],points[j][1]))
    elif i==5 or j==5:
        pygame.draw.line(display,BLUE,(points[i][0],points[i][1]),(points[j][0],points[j][1]))
    else:
        pygame.draw.line(display,WHITE,(points[i][0],points[i][1]),(points[j][0],points[j][1]))

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
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        angle+=0.01
    elif keys[pygame.K_LEFT]:
        angle-=0.01
    else:
        angle+=0.01
    
    display.fill(BLACK)

    debug(display,str(angle),font)

    for index,point in enumerate(points):
        rotated2d = rotate(angle,point.reshape((4,1)))
        projected2d = multiply_projection(projection_matrix,rotated2d)
        x = int(projected2d[0][0]*SCALE) + CENTER[0]
        y = int(projected2d[1][0]*SCALE) + CENTER[1]
        projected_points[index] = [x,y]
        pygame.draw.circle(display,WHITE,(x,y),5)

    for i in (0,2,4,6):
        connect_points(i,i+1,projected_points)
    for i in (0,1,4,5):
        connect_points(i,i+2,projected_points)
    for i in (0,1,2,3):
        connect_points(i,i+4,projected_points)

    pygame.display.update()