from leg_class import LEG
from leg_class import body_loc
from leg_class import inverse_kin
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Qt5Agg')

leg4 = LEG('right', 'front')

######################################
psi_range = np.linspace(-45,46,20)
theta_range = np.linspace(-90,105,20)
phi_range = np.linspace(72,271,20)

fig = plt.figure(1)
ax = fig.add_subplot(projection='3d')

# for psi in psi_range:
for theta in theta_range:
    for phi in phi_range:
        p0,p1,p2,p3 = leg4.activate(0,theta,phi)

        x = p3[0]
        y = p3[1]
        z = p3[2]

        # print('psi = {}'.format(psi))
        # print('theta = {}'.format(theta))
        print('phi = {}'.format(phi))

        ax.scatter(x,y,z, color='k', zdir='y')

bound = 700
ax.set_xlim(-bound,bound)
ax.set_ylim(-bound,bound)
ax.set_zlim(-bound,bound)
ax.set_xlabel('x')
ax.set_ylabel('z')
ax.set_zlabel('y')

# ax.view_init(elev=270,azim=0)
plt.show()


