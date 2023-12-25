import numpy as np
import sympy as sp

class Particle:
    def __init__(self, pos: tuple[int], vel: tuple[int]):
        self.pos = pos
        self.vel = vel
    
    def __str__(self):
        return f"Particle - pos {self.pos}, vel {self.vel}"
    
    def find_intersection_with(self, other: "Particle") -> tuple[float]:
        """Return (x, y) intersection point, or None if intersection is in the past"""
        A = np.array([[self.vel[0], -other.vel[0]],
                      [self.vel[1], -other.vel[1]],
                      [self.vel[2], -other.vel[2]]])
        b = np.array([[other.pos[0] - self.pos[0]],
                      [other.pos[1] - self.pos[1]],
                      [other.pos[2] - self.pos[2]]])
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
        self.Ab = None
        self.set_up_system()
    
    def __str__(self):
        result = ""
        for particle in self.particles:
            result += "\n  " + str(particle)
        return result
    
    def set_up_system(self):
        n = len(self.particles)
        self.Ab = sp.Matrix(np.zeros([3 * n, 3 + n + 1]))
        for i, particle in enumerate(self.particles):
            for j in range(3):
                self.Ab[3 * i + j, j] = 1
                self.Ab[3 * i + j, -1] = particle.pos[j]
    
    def get_perfect_vel(self):
        boundary = 100
        total_iterations = (2 * boundary + 1) ** 3
        print(total_iterations)
        counter = 0
        for i in range(-boundary, boundary + 1):
            for j in range(-boundary, boundary + 1):
                for k in range(-boundary, boundary + 1):
                    counter += 1
                    if counter % 1000 == 0:
                        print(f"{counter} out of {total_iterations}")
                    pos = self.get_perfect_pos((i, j, k))
                    if pos is not None:
                        print(pos)
                        raise Exception
    
    def get_perfect_pos(self, v0):
        for i, particle in enumerate(self.particles):
            for j in range(3):
                self.Ab[3 * i + j, 3 + i] = v0[j] - particle.vel[j]
        
        reduced = self.Ab.rref()[0]

        # check for pivot in last column
        for i in range(reduced.shape[0] - 1, -1, -1):
            if reduced[i, -1]:
                row = np.array(reduced[i, :-1])
                if np.sum(np.abs(row)) == 0:
                    return None
                break
        return np.array(reduced[:, -1])[:3, 0]
    
    # def check_for_parallel_lines(self):
    #     for i, particle1 in enumerate(self.particles):
    #         for particle2 in self.particles[i+1:]:
    #             v1 = particle1.vel
    #             v2 = particle2.vel
    #             k1 = v2[0] / v1[0]
    #             k2 = v2[1] / v1[1]
    #             k3 = v2[2] / v1[2]
    #             if np.isclose(k1, k2) and np.isclose(k2, k3):
    #                 print(particle1)
    #                 print(particle2)

    # def get_all_intersections(self) -> int:
    #     """Return number of pairs that cross within area"""
    #     counter = 0
    #     for i, particle1 in enumerate(self.particles):
    #         for particle2 in self.particles[i+1:]:
    #             intersection = particle1.find_intersection_with(particle2)
    #             if intersection is not None:
    #                 counter += 1
    #     print(counter)
    #     return counter

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

field = Parser.parse_from_file(filename)
# field.get_perfect_vel()