import numpy as np

class RandomWalker():
    def __init__(self):
        self.x = 0.0 # X-position
        self.y = 0.0 # Y-position
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Orientation
        self.v = 1.0 # Velocity

        # A simple walker that starts at the origin and moves in one
        # of four cardinal directions (0, π/2, π, 3π/2).

    def step(self):
        # Move forward in the direction of orientation
        self.x += self.v*np.cos(self.o)
        self.y += self.v*np.sin(self.o)
    
    def turn(self):
        # self.o = np.random.random()*2*np.pi # Part 1
        # Randomly choose between four grid-aligned orientations
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Grid-like movement


class TrulyRandomWalker():
    def __init__(self, duration):
        # Start at a random point within [-duration, duration]
        self.x = np.random.randint(-duration, duration + 1) # X-position
        self.y = np.random.randint(-duration, duration + 1) # Y-position
        
        # Orientation chosen from the four cardinal directions
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Orientation
        
        # Random speed scaled based on simulation duration
        self.v = np.random.randint(1, np.sqrt(np.sqrt(duration + 1) + 1) + 1) # Velocity

    def step(self):
        # Move forward using velocity and orientation
        self.x += self.v*np.cos(self.o)
        self.y += self.v*np.sin(self.o)

    def turn(self):
        # Grid-based turning, same as RandomWalker
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Grid-like movement


class RandomRandomWalker():
    def __init__(self, duration):
        # Generate two possible x-values: 0 and a random value
        self.xs = []
        self.xs.append(0.0)
        self.xs.append(np.random.randint(-duration, duration + 1))

        # Same for y-values
        self.ys = []
        self.ys.append(0.0)
        self.ys.append(np.random.randint(-duration, duration + 1))

        # Two orientations: 0 radians or a random cardinal direction
        self.os = []
        self.os.append(0.0)
        self.os.append(np.random.choice([0, 0.5, 1, 1.5])*np.pi)

        # Two velocities: base speed or a random one
        self.vs = []
        self.vs.append(1.0)
        self.vs.append(np.random.randint(1, np.sqrt(np.sqrt(duration + 1) + 1) + 1))

        # Randomly pick between the two possible values for each property
        self.x = self.xs[np.random.choice([0, 1])] # X-position
        self.y = self.ys[np.random.choice([0, 1])] # Y-position
        self.o = self.os[np.random.choice([0, 1])] # Orientation
        self.v = self.vs[np.random.choice([0, 1])] # Velocity

        # This walker randomly selects one of two possible initialization states.

    def step(self):
        # Move forward based on velocity and orientation
        self.x += self.v*np.cos(self.o)
        self.y += self.v*np.sin(self.o)

    def turn(self):
        # Grid-like turning similar to the other walkers
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Grid-like movement


class Braitenberg():
    def __init__(self):
        self.x = 0.0 # X-position
        self.y = 0.0 # Y-position
        self.o = np.random.choice([0, 0.5, 1, 1.5])*np.pi # Orientation
        self.v = 1.0 # Velocity
        
        self.r = 1.0 # Size (radius)
        
        # Sensor readings
        self.ls = 0.0 # Left Sensor
        self.rs = 0.0 # Right Sensor
        
        # Motor activations
        self.lm = 0.0 # Left Motor
        self.rm = 0.0 # Right Motor
        
        self.a = np.pi/2 # Angle offset of sensors

        # Initial global sensor positions
        self.rsX = self.r*np.cos(self.o+self.a) # X-position of right sensor
        self.rsY = self.r*np.sin(self.o+self.a) # Y-position of right sensor
        self.lsX = self.r*np.cos(self.o-self.a) # X-position of left sensor
        self.lsY = self.r*np.sin(self.o-self.a) # Y-position of left sensor

        # Gains controlling robot sensitivity
        self.tg = 1/10.0 # Turning gain
        self.vg = 1/10.0 # Velocity gain
        self.sg = 1/10.0 # Sensor gain

    def move(self):
        # Adjust orientation based on difference in motor outputs
        self.o += self.tg * (self.rm - self.lm)
        
        # Motor-to-velocity mapping
        # self.lm = 1.0
        # self.rm = 1.0
        # self.o += self.tg * (self.lm - self.rm) + np.random.normal(-0.1, 0.1)
        self.v = self.vg * (self.lm + self.rm)

        # Update body position
        self.x += self.v*np.cos(self.o)
        self.y += self.v*np.sin(self.o)

        # Update sensor positions after movement
        self.rsX = self.x + self.r*np.cos(self.o+self.a)
        self.rsY = self.y + self.r*np.sin(self.o+self.a)
        self.lsX = self.x + self.r*np.cos(self.o-self.a)
        self.lsY = self.y + self.r*np.sin(self.o-self.a)
    
    def sense(self, light, size):
        # Compute distances from sensors to light source
        self.ls = self.sg*np.sqrt((self.lsX - light.x)**2 + (self.lsY - light.y)**2)
        self.rs = self.sg*np.sqrt((self.rsX - light.x)**2 + (self.rsY - light.y)**2)

        # Clip readings to avoid excessively large sensor values
        self.ls = np.clip(self.ls, 0, size)
        self.rs = np.clip(self.rs, 0, size)
    
    def think(self, duration):
        # Convert sensor readings into motor commands
        # Closer light → smaller distance → bigger motor value
        self.lm = 1.0 / (self.ls)
        self.rm = 1.0 / (self.rs)

        # Clamp to prevent blowing up
        self.lm = np.clip(self.lm, 0.0, 10.0)
        self.rm = np.clip(self.rm, 0.0, 10.0)

        # Velocity gain based on total duration
        self.vg = np.log10(max(duration, 10))
        self.vg = np.clip(self.vg, 0.0, 100.0)/5

        # Turning gain depends on difference in motor outputs
        self.tg
        self.tg = np.clip(np.log10(max(duration, 10)), -250.0, 250.0)*(1 + np.abs(self.rm - self.lm))

        # Stop movement if too close to the light
        if self.ls < 0.5 or self.rs < 0.5:
            self.lm = 0.0
            self.rm = 0.0
            self.vg = 0.0
            self.tg = 0.0
    
    def thinkWorldTravel(self, duration):
        # Sensor → motor mapping, similar to think()
        self.lm = 1.0 / (self.ls)
        self.rm = 1.0 / (self.rs)
        self.lm = np.clip(self.lm, 0.0, 5.0)
        self.rm = np.clip(self.rm, 0.0, 5.0)

        # Velocity based on motor symmetry
        self.vg = (self.lm + self.rm) / int(np.sqrt(duration))
        if int(self.lm) == int(self.rm):
            # If both sensors see the same brightness, move directly forward
            self.vg = self.ls*self.rs
        
        # Turning gain scaled by duration
        self.tg = self.vg*int(np.sqrt(duration))
        
        # Stop motion if too close
        if self.ls < 0.5 or self.rs < 0.5:
            self.lm = 0.0
            self.rm = 0.0
            self.vg = 0.0
            self.tg = 0.0


class LightSource():
    def __init__(self, size):
        # Create a random light location within a square of side length 2*size
        self.x = np.random.randint(1-size, size)
        self.y = np.random.randint(1-size, size)

        # Ensure the light does not spawn too close to the origin
        while (np.sqrt(self.x**2 + self.y**2) <= 1):
            self.x = np.random.randint(1-size, size)
            self.y = np.random.randint(1-size, size)