import numpy as np

def matrices_generator(angles):
    psi = np.deg2rad(angles[0])
    theta = np.deg2rad(angles[1])
    phi = np.deg2rad(angles[2])

    A01 = [[np.cos(psi), 0, -np.sin(psi),0],
           [0, 1, 0, 0],
           [np.sin(psi), 0, np.cos(psi), 0],
           [0, 0, 0, 1]]

    A12 = [[1, 0, 0, 0],
           [0, np.cos(theta), -np.sin(theta), -31],
           [0, np.sin(theta), np.cos(theta), 0],
           [0, 0, 0, 1]]

    A23 = [[1, 0, 0, 0],
           [0, np.cos(phi), -np.sin(phi), 0],
           [0, np.sin(phi), np.cos(phi), 0],
           [0, 0, 0, 1]]

    A_right = [[-1,0,1,0],
               [0,1,0,0],
               [0,0,-1,0],
               [0,0,0,1]]

    return A01,A12,A23,A_right

def inverse_kin(x, y, z):
    # converts x,y,z in world axis system to engines' degrees.
    # NOTE: while calculating this program assumes:
    # #1 outer leg edge is lower then the body
    # #2 inner leg edge is higher then outer leg edge
    # #3 x is forward, y is upwards and z is outwards
    # #4 y is given in opposite direction (greater y = higher body (=lower leg edge) ).
    # function fixes coordinates according to leg side (left/right)

    l1 = 51.5
    l2 = 210.54
    l3 = 372.4

    # a = np.sqrt(x**2 + z**2 + l1)

    psi = np.arctan2(x,z)

    b = np.sqrt(y ** 2 + z ** 2 + x**2)

    C = (l2 ** 2 + b ** 2 - l3 ** 2) / (2 * l2 * b)
    D = (l2 ** 2 + l3 ** 2 - b ** 2) / (2 * l2 * l3)

    alpha = np.arcsin(y / b)

    theta = np.arctan2(np.sqrt(1 - C ** 2), C) - alpha
    phi = np.arctan2(np.sqrt(1 - D ** 2), D)

    # rad to deg
    psi_d = np.degrees(psi)
    theta_d = np.degrees(theta)
    phi_d = np.degrees(phi)

    pos = [psi_d, theta_d, phi_d]
    return pos

def body_loc():
    dx = dz = 90.87
    dz_mid = 122.75
    dots = [[dx, 0, -dx, -dx, 0, dx, dx],
            [0,0,0,0,0,0,0],
            [dz, dz_mid, dz, -dz, -dz_mid, -dz, dz]]
    return dots


class LEG:
    def __init__(self, side, position):
        self.side = side
        self.position = position
        dx = dz = 90.87
        dz_mid = 122.75

        # offset fix for legs depending on position & side
        if self.position == 'middle':
            self.z_offset = dz_mid
            self.x_offset = 0
        elif self.position == 'front':
            self.z_offset = dz
            self.x_offset = dx
        else:
            self.z_offset = dz
            self.x_offset = -dx

    def activate(self, psi, theta, phi):
        l0 = [0,0,51.5,1]
        d0 = [0,-31,0,1]
        l1 = [0,0,210.5,1]
        l2 = [0,0,372.4,1]

        phi = phi-180   # phi correction for angle reference

        A01,A12,A23,A_right = matrices_generator([psi, theta, phi])
        A02 = np.dot(A01,A12)
        A03 = np.dot(A02, A23)

        point_values = [[0,0,0,1],
                        np.ndarray.tolist(np.dot(A01,l0)+d0),
             np.ndarray.tolist(np.dot(A01,l0)+np.dot(A02,l1)),
             np.ndarray.tolist(np.dot(A01,l0)+np.dot(A02,l1)+np.dot(A03,l2))]

        for v in range(4):
            point_values[v][0] = point_values[v][0] + self.x_offset
            point_values[v][2] = point_values[v][2] + self.z_offset

        if self.side == 'right':
            for point in point_values:
                point[2] = -point[2]

        return (point_values[0],point_values[1],point_values[2],point_values[3])

    # def x_forward(self, step_size, resolution):
    # # Creates x values for forward movement (one leg at a time).
    #     front_offset = -100
    #     back_offset = -1 * front_offset
    #
    #     if self.position == 'front':
    #         return range(step_size + front_offset, front_offset, -resolution)
    #     elif self.position == 'back':
    #         return range(back_offset, -step_size + back_offset, -resolution)
    #     else:
    #         return range(round(step_size/2), -round(step_size/2), -resolution)

    def x_forward(self, step_size, resolution):
        # Creates x values for forward movement (one leg at a time).
        front_offset = -100
        back_offset = -1 * front_offset

        x = []

        if self.position == 'front':
            start = step_size + front_offset
            finish = front_offset
        elif self.position == 'back':
            start = back_offset
            finish = -step_size + back_offset
        else:
            start = round(step_size / 2)
            finish = -round(step_size / 2)


        x_edge = []
        x_other_edge = []
        counter = 0
        counter_sum = 0
        acceleration = 2

        while counter < resolution:
            x_edge.append(start - (counter + counter_sum))
            x_other_edge.append(finish + (counter + counter_sum))
            counter_sum = counter_sum + counter
            counter = counter + acceleration

        x_other_edge = np.flip(x_other_edge)
        x = range(x_edge[-1]-resolution, x_other_edge[0], -resolution)

        x = np.append(x_edge, x)
        x = np.append(x, x_other_edge)
        return x