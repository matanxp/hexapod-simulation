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
y = 200
z = 200
step_size = 100
steps_num = 2
resolution = 10
step_height = 75
step_dist = 30
wait_time = 0.01
####################################

x_f = []  # array of x value sets for six legs. 'f' stands for 'forward motion'. leg0 = 0
y_f = []  # array of y value sets for six legs (etc.)
z_f = []  # array of z value sets for six legs (etc.)

x_b = []  # array of x value sets for six legs. 'b' stands for 'backwards motion'. leg0 = 0
y_b = []  # etc..
z_b = []

x_t = []
y_t = []
z_t = []


for num in (range(6)):  # creating value sets
    x_f.append(legs[num].x_forward(step_size, resolution))  # calculating x values for forward movement

    samples = len(x_f[num])

    y_f.append([y] * samples)
    z_f.append([z] * samples)

    x_b.append(np.flip(x_f[num]))  # creating values set for x backwards movement (opposite of x_f)

    y_b1 = np.linspace(y, y - step_height, int(samples / 2))
    y_b2 = np.flip(y_b1)
    y_b.append(np.ndarray.tolist(np.append(y_b1, y_b2)))
    if len(y_b[num]) < len(x_b[num]):
        y_b[num].append(y)

    z_b1 = np.linspace(z_f[num][-1], z_f[num][-1] - step_dist, int(samples / 2))
    z_b2 = np.flip(z_b1)
    z_b.append(np.ndarray.tolist(np.append(z_b1, z_b2)))
    if len(z_b[num]) < len(x_b[num]):
        z_b[num].append(z)

    if num % 2 != 0:  # switching double legs (0,2,4) values
        x_f[num], x_b[num] = x_b[num], x_f[num]
        y_f[num], y_b[num] = y_b[num], y_f[num]
        z_f[num], z_b[num] = z_b[num], z_f[num]

    x_t.append(list(x_f[num]) + list(x_b[num]))
    y_t.append(list(y_f[num]) + list(y_b[num]))
    z_t.append(list(z_f[num]) + list(z_b[num]))

#################################################################################
for step in range(steps_num):
    for it in range(len(x_t[0])):
        fig = plt.figure(1)
        ax = fig.add_subplot(projection='3d')
        for leg in range(6):
            angles = inverse_kin(x_t[leg][it],z_t[leg][it],y_t[leg][it])
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
        ax.set_xlabel('x')
        ax.set_ylabel('z')
        ax.set_zlabel('y')
        ax.view_init(elev=220,azim=50)
        plt.draw()
        plt.pause(wait_time)
        plt.clf()
plt.show()


