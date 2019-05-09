class Simulate:
    def __init__(self, engine, stepsize, steptime, bodies, masslessbodies = None, envmod = None, bailout=False):
        self.engine = engine(steptime, bodies, masslessbodies)
        self.stepsize = stepsize
        self.steptime = steptime
        self.bodies = bodies
        self.masslessbodies = masslessbodies
        self.envmod = envmod
        self.bailout = bailout
        self.dirty = False
        self.steps = 0.0
        self.time = 0.0
    def main_loop(self):
        while not self.bailout or self.time < self.bailout:
            if self.envmod != None:
                if any([i.run(self) for i in self.envmod]):
                    break
            if self.dirty:
                self.engine.set_steptime(self.steptime)
                self.engine.set_bodies(self.bodies)
                self.engine.set_masslessbodies(self.masslessbodies)
                self.dirty=False
            self.engine.simulate(self.stepsize)
            self.steps += self.stepsize
            self.time += self.stepsize*self.steptime
    def set_dirty(self):
        self.dirty = True
