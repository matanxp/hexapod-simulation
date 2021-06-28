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
resolution = 5
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
Fmg = 16.35
Fe = 1.61
Fil = 0.883
Fol = 1.03
m1 = []
m2 = []
m3 = []

timestamp = 0.2
total_time = timestamp*len(x_t[4])
time = np.linspace(0,total_time,int(total_time/timestamp))

for it in range(len(x_f[0])):
    for leg in [4]:
        angles = inverse_kin(x_f[leg][it],z_f[leg][it],y_f[leg][it])
        legs_loc = []
        p0,p1,p2,p3 = legs[leg].activate(angles[0],angles[1],angles[2])

        x = [p0[0], p1[0], p2[0], p3[0]]
        y = [p0[1], p1[1], p2[1], p3[1]]
        z = [p0[2], p1[2], p2[2], p3[2]]
        legs_loc.append(x)
        legs_loc.append(y)
        legs_loc.append(z)

        Xi = 0.225 * np.sin(angles[1])
        Xo = 0.35 * np.sin(angles[2]-(90-angles[1]))

        Xcm_i = 0.099 * np.sin(angles[1])
        Xcm_o = 0.145 * np.sin(angles[2]-(90-angles[1]))

        M1 = 0.01 * 5/3
        M2 = Fmg*(Xi + Xo) - Fe*Xi - Fol*(Xi + Xcm_o) - Fil*Xcm_i
        M3 = Fmg*Xo - Fol*Xcm_o
        m1.append(M1)
        m2.append(-M2)
        m3.append(-M3)

for it in range(len(x_b[0])):
    for leg in [4]:
        angles = inverse_kin(x_b[leg][it],z_b[leg][it],y_b[leg][it])
        legs_loc = []
        p0,p1,p2,p3 = legs[leg].activate(angles[0],angles[1],angles[2])

        x = [p0[0], p1[0], p2[0], p3[0]]
        y = [p0[1], p1[1], p2[1], p3[1]]
        z = [p0[2], p1[2], p2[2], p3[2]]
        legs_loc.append(x)
        legs_loc.append(y)
        legs_loc.append(z)

        Xi = 0.225 * np.sin(angles[1])
        Xo = 0.35 * np.sin(angles[2]-(90-angles[1]))

        Xcm_i = 0.099 * np.sin(angles[1])
        Xcm_o = 0.145 * np.sin(angles[2]-(90-angles[1]))

        M1 = 0.01 * (0.165+0.165+0.105+0.09)
        M2 = - Fe*Xi - Fol*(Xi + Xcm_o) - Fil*Xcm_i
        M3 = - Fol*Xcm_o
        m1.append(M1)
        m2.append(-M2)
        m3.append(-M3)

fig,(ax1,ax2,ax3) = plt.subplots(3,)

ax1.plot(time,m1, linewidth='1.5',marker='o',markersize='3.5',mec='k')
# ax1.scatter(time,x_t[4])
ax1.grid()
ax1.set_title('Moment applied on engine 1')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Moment [N/m]')

ax2.plot(time,m2, linewidth='1.5', color='g',marker='o',markersize='3.5',mec='k')
ax2.grid()
ax2.set_title('Moment applied on engine 2')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Moment [N/m]')

ax3.plot(time,m3, linewidth='1.5', color='red',marker='o',markersize='3.5',mec='k')
ax3.grid()
ax3.set_title('Moment applied on engine 3')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Moment [N/m]')

plt.subplots_adjust(hspace=0.75)
# plt.subplot_tool()
plt.show()
