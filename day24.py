import numpy as np

class Particle:
    def __init__(self, pos: tuple[int], vel: tuple[int]):
        self.pos = pos
        self.vel = vel
    
    def __str__(self):
        return f"Particle - pos {self.pos}, vel {self.vel}"
    
    def find_intersection_with(self, other: "Particle") -> tuple[float]:
        """Return (x, y) intersection point, or None if intersection is in the past"""
        A = np.array([[self.vel[0], -other.vel[0]],
                      [self.vel[1], -other.vel[1]]])
        b = np.array([[other.pos[0] - self.pos[0]],
                      [other.pos[1] - self.pos[1]]])
        try:
            solution = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            # no intersection
            return None
        t1, t2 = solution[0, 0], solution[1, 0]
        if t1 < 0 or t2 < 0:
            return None
        intersection_x = self.pos[0] + t1 * self.vel[0]
        intersection_y = self.pos[1] + t1 * self.vel[1]
        return (intersection_x, intersection_y)

class Field:
    def __init__(self, particles: list[Particle]):
        self.particles = particles
    
    def __str__(self):
        result = ""
        for particle in self.particles:
            result += "\n  " + str(particle)
        return result

    def get_all_intersections(self, x_bounds: tuple[float], y_bounds: tuple[float]) -> int:
        """Return number of pairs that cross within area"""
        counter = 0
        for i, particle1 in enumerate(self.particles):
            for particle2 in self.particles[i+1:]:
                intersection = particle1.find_intersection_with(particle2)
                if intersection is not None:
                    if x_bounds[0] < intersection[0] < x_bounds[1] and y_bounds[0] < intersection[1] < y_bounds[1]:
                        counter += 1
        return counter

class Parser:
    def parse_from_file(filename) -> Field:
        with open(filename, "r") as f:
            raw = f.read()
        particles = []
        for line in raw.split("\n"):
            pos_raw_list = line.split(" ")[:3]
            vel_raw_list = line.split(" ")[4:]
            vel_raw_list = [v for v in vel_raw_list if len(v) > 0]
            for i in range(2):
                # remove commas
                pos_raw_list[i] = pos_raw_list[i][:-1]
                vel_raw_list[i] = vel_raw_list[i][:-1]
            pos = [int(p) for p in pos_raw_list]
            vel = [int(v) for v in vel_raw_list]
            particles.append(Particle(pos, vel))
        return Field(particles)

filename = "day24.txt"

boundaries = {"day24demo.txt": ((7, 27), (7, 27)),
              "day24.txt": ((200000000000000, 400000000000000), (200000000000000, 400000000000000))}

field = Parser.parse_from_file(filename)
result = field.get_all_intersections(boundaries[filename][0], boundaries[filename][1])

print(result)