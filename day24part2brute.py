"""
DOES NOT WORK

Brute force solution: iterating through possible starting velocities and finding the starting
position for each.

Already made sure none of the particles' trajectories intersect or are parallel (code not
included.)
"""

import numpy as np
import sympy as sp

class Particle:
    def __init__(self, pos: tuple[int], vel: tuple[int]):
        self.pos = pos
        self.vel = vel
    
    def __str__(self):
        return f"Particle - pos {self.pos}, vel {self.vel}"

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
        """List all velocities up to some value and sort them. Only use first 3
        particles."""
        self.particles = self.particles[:3]
        boundary = 40
        start_vels = []
        for i in range(-boundary, boundary + 1):
            for j in range(-boundary, boundary + 1):
                for k in range(-boundary, boundary + 1):
                    start_vels.append((i, j, k))
        start_vels.sort(key=lambda x: sum(abs(i) for i in x))
        for v0 in start_vels:
            pos = self.get_perfect_pos(v0)
            if pos is not None:
                print("Found result", pos)
                raise Exception
    
    def get_perfect_pos(self, v0):
        """For a given starting velocity, find starting position by solving a system
        of linear equations. If no solutions, then starting velocity is not good."""
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
field.get_perfect_vel()