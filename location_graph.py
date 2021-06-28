from leg_class import LEG
import numpy as np
import matplotlib.pyplot as plt

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
z = 250
step_size = 100
resolution = 10
step_height = 75
step_dist = 30
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

timestamp = 0.2
total_time = timestamp*len(x_t[4])
time = np.linspace(0,total_time,int(total_time/timestamp))

#################################################################################
fig,(ax1,ax2,ax3) = plt.subplots(3,)

ax1.plot(time,x_t[4], linewidth='1.5',marker='o',markersize='3.5',mec='k')
# ax1.scatter(time,x_t[4])
ax1.grid()
ax1.set_title('X location')
ax1.set_xlabel('Time [s]')
ax1.set_ylabel('Location [mm]')

ax2.plot(time,y_t[4], linewidth='1.5', color='g',marker='o',markersize='3.5',mec='k')
ax2.grid()
ax2.set_title('Y location')
ax2.set_xlabel('Time [s]')
ax2.set_ylabel('Location [mm]')

ax3.plot(time,z_t[4], linewidth='1.5', color='red',marker='o',markersize='3.5',mec='k')
ax3.grid()
ax3.set_title('Z location')
ax3.set_xlabel('Time [s]')
ax3.set_ylabel('Location [mm]')

plt.subplots_adjust(hspace=0.75)
# plt.subplot_tool()
plt.show()
