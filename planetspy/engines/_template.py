ass SimulationEngine:
    def SimulationEngine(self, steptime, bodies, masslessbodies):
        self.set_steptime(steptime)
        self.set_bodies(bodies)
        self.set_masslessbodies(masslessbodies)
        
    def set_steptime(self, steptime):
        self.steptime = steptime
    def set_bodies(self, bodies):
        self.bodies = bodies
    def set_masslessbodies(self, masslessbodies):
        self.masslessbodies = masslessbodies

    def get_steptime(self):
        return self.steptime
    def get_bodies(self):
        return self.bodies
    def get_masslessbodies(self):
        return self.masslessbodies
    
    def simulate(self, steps):
        pass