import numpy as np

class collisions:
    loc = []
    def __init__(self, named = True):
        self.named = named
    def run(self, simclass):
        self.loc.append(np.copy(simclass.bodies[0][::,0:3]))
        x_dist = np.hstack(simclass.bodies[0][::,0]) - np.vstack(simclass.bodies[0][::,0])
        y_dist = np.hstack(simclass.bodies[0][::,1]) - np.vstack(simclass.bodies[0][::,1])
        z_dist = np.hstack(simclass.bodies[0][::,2]) - np.vstack(simclass.bodies[0][::,2])
        radii_add = np.hstack(simclass.bodies[0][::,6]) + np.vstack(simclass.bodies[0][::,6])
        x_distsq = x_dist**2
        y_distsq = y_dist**2
        z_distsq = z_dist**2
        distsq = (x_distsq + y_distsq + z_distsq)
        dist = np.sqrt(distsq)
        dist = np.where(dist != 0, dist, np.inf)
        distsq = 1/np.where(distsq != 0, distsq, np.inf) 
        dist = np.where(dist >= radii_add , dist, 0)
        collided_bodies = np.where(dist == 0)
        coll_bodies = []
        for i in range(0, len(collided_bodies[0])//2):
            coll_bodies.append([collided_bodies[0][i], collided_bodies[1][i]])
        if len(coll_bodies) ==0:
            return False
        def combine(F,L):
            x = (simclass.bodies[0][F, 0]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 0]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            y = (simclass.bodies[0][F, 1]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 1]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            z = (simclass.bodies[0][F, 2]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 2]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            vx = (simclass.bodies[0][F, 3]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 3]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            vy = (simclass.bodies[0][F, 4]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 4]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            vz = (simclass.bodies[0][F, 5]*simclass.bodies[0][F, 7] + simclass.bodies[0][L, 5]*simclass.bodies[0][L, 7])/(simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7])
            r = (simclass.bodies[0][F, 6]**3 + simclass.bodies[0][L, 6]**3)**(1/3)
            m = simclass.bodies[0][F, 7] + simclass.bodies[0][L, 7]
            return np.array([x, y, z ,vx, vy, vz, r, m])
        for i in range(len(coll_bodies)):
            simclass.bodies[0][coll_bodies[i][0]] = combine(coll_bodies[i][0], coll_bodies[i][1])
        simclass.bodies[0] = np.delete(simclass.bodies[0], np.array(coll_bodies)[::,1], 0)
        if self.named == True:
            for i in range(len(coll_bodies)):
                simclass.bodies[1][coll_bodies[i][0]][0] = simclass.bodies[1][coll_bodies[i][0]][0] + simclass.bodies[1][coll_bodies[i][1]][0]
            def delete(list_, n):
                list_ = list_[:n] + list_[n+1:]
                return list_
            for i in range(len(coll_bodies)):
                simclass.bodies[1] = delete(simclass.bodies[1], np.array(coll_bodies)[i,1])
        simclass.set_dirty()
        return False

class record:
    loc = []
    def __init__(self):
        self.loc = []
    def run(self, simclass):
        self.loc.append(np.copy(simclass.bodies[0][::,0:3]))
        if simclass.masslessbodies:
            loc[len(loc) - 1].append(simclass.masslessbodies[0][::,0:3])
        return False

###  normally distributed dust cloud  ####

#total mass = ~1 pluto
#rad 10**14 m
#particle rad ~idk
#cloud velocity 10**4 m/s

#cloud = [np.array([[x, y, z ,vx, vy, vz, r, m],[],[],[],[],[]...]),[]]

def cloud_gen(total_mass, radius, avg_velocity, num_part):
    xloc = np.random.normal(scale = radius, size = num_part)
    yloc = np.random.normal(scale = radius, size = num_part)
    zloc = np.random.normal(scale = radius, size = num_part)
    vx = np.random.normal(loc = avg_velocity, scale = 15, size = num_part) #normal dist about avg velocity [m/s] in x direction
    vy = np.random.normal(scale = 2, size = num_part)
    vz = np.random.normal(scale = 2, size = num_part)
    m = abs(np.random.normal( loc= total_mass/num_part ,scale = total_mass/(4*num_part) ,size = num_part))
    r = np.zeros(num_part)
    cloud = [[],[]]
    cloud[0] = np.zeros(num_part)
    r = [m[i]**(1/3)*1/30 for i in range(num_part)]
    cloud[0] = np.array([[xloc[i],yloc[i], zloc[i], vx[i], vy[i], vz[i], r[i], m[i] ] for i in range(num_part)])
    return cloud