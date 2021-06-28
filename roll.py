import time
from leg_class import LEG
from leg_class import body_loc
from leg_class import inverse_kin
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')


leg1 = LEG('left', 'front')
leg2 = LEG('left', 'middle')
leg3 = LEG('left', 'back')
leg4 = LEG('right', 'front')
leg5 = LEG('right', 'middle')
leg6 = LEG('right', 'back')

legs = [leg1,leg2,leg3,leg4,leg5,leg6]

######################################
# VALUES DEFINITION. all sizes are in [mm]. #
angle = 45
resolution = 2
######################################
dist_mid = 174.25
dist_non_mid = 139.26
angles = range(0, abs(angle) + 1, resolution)
front_offset = 120
back_offset = front_offset * -1
y_const = 200
z_const = 250
wait_time = 0.01
######################################
x_a = [[], [], [], [], [], []]
y_a = [[], [], [], [], [], []]
z_a = [[], [], [], [], [], []]

for num in range(6):
    if num == 1 or num == 4:
        dist = dist_mid
    else:
        dist = dist_non_mid

    if num < 3:
        for ang in angles:
            y_a[num].append(y_const + (dist * np.sin(np.deg2rad(ang))))
            z_a[num].append(z_const - (dist - dist * np.cos(np.deg2rad(ang))))
    else:
        for ang in angles:
            y_a[num].append(y_const - (dist * np.sin(np.deg2rad(ang))))
            z_a[num].append(z_const + (dist - dist * np.cos(np.deg2rad(ang))))

for num in range(6):
    for i in range(len(y_a[num])):
        if legs[num].position == 'back':
            x_a[num].append(front_offset)
        elif legs[num].position == 'front':
            x_a[num].append(back_offset)
        else:
            x_a[num].append(0)

if angle < 0:
    for i in range(3):
        x_a[i], x_a[3 + i] = x_a[3 + i], x_a[i]
        y_a[i], y_a[3 + i] = y_a[3 + i], y_a[i]
        z_a[i], z_a[3 + i] = z_a[3 + i], z_a[i]

################################################################################

for it in range(len(x_a[0])):

    fig = plt.figure(1)
    ax = fig.add_subplot(projection='3d')

    for leg in range(6):

        angles = inverse_kin(x_a[leg][it],z_a[leg][it],y_a[leg][it])
        legs_loc = []
        p0,p1,p2,p3 = legs[leg].activate(angles[0],angles[1],angles[2])

        x = [p0[0], p1[0], p2[0], p3[0]]
        y = [p0[1], p1[1], p2[1], p3[1]]
        z = [p0[2], p1[2], p2[2], p3[2]]
        legs_loc.append(x)
        legs_loc.append(y)
        legs_loc.append(z)

        ax.plot(legs_loc[0],legs_loc[1],legs_loc[2], color='r',zdir='y')

        for i in range(len(legs_loc[0])):
            ax.scatter(legs_loc[0][i], legs_loc[1][i], legs_loc[2][i], color='k', zdir='y')

    ax.plot(body_loc()[0],body_loc()[1],body_loc()[2], linewidth='3', color='b',zdir='y') # creating body lines

    bound = 500
    ax.set_xlim(-bound/1.5,bound/1.5)
    ax.set_ylim(-bound,bound)
    ax.set_zlim(-bound,bound)
    ax.view_init(elev=190,azim=180)

    plt.draw()
    plt.pause(wait_time)
    plt.clf()
plt.show()