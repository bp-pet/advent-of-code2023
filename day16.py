import numpy as np

with open("day16.txt", 'r') as f:
    input = f.read()

x_size = len(input.split("\n"))
y_size = len(input.split("\n")[0])

class Beam:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction
    
    def move(self):
        if self.direction == "u":
            self.x -= 1
        elif self.direction == "r":
            self.y += 1
        elif self.direction == "l":
            self.y -= 1
        elif self.direction == "d":
            self.x += 1
        else:
            raise Exception("Invalid direction")
    
    def __str__(self):
        return f"Beam at {self.x, self.y}, direction {self.direction}"

class Board:
    def __init__(self, input: str):
        self.grid = np.array([list(i) for i in input.split("\n")])
        self.beams = []
        self.visited = np.zeros_like(self.grid)
    
    def run(self, iterations: int):
        for _ in range(iterations):
            self.one_step()
        return self.get_number_of_visited()

    def one_step(self):
        to_delete = []
        to_add = []
        for i, beam in enumerate(self.beams):
            beam.move()
            if self.is_out_of_bounds(beam):
                to_delete.append(i)
                continue
            char = self.grid[beam.x, beam.y]
            if char == ".":
                pass
            elif char == "\\":
                if beam.direction == "l":
                    beam.direction = "u"
                elif beam.direction == "r":
                    beam.direction = "d"
                elif beam.direction == "d":
                    beam.direction = "r"
                elif beam.direction == "u":
                    beam.direction = "l"
                else:
                    raise Exception("Invalid direction")
            elif char == "/":
                if beam.direction == "l":
                    beam.direction = "d"
                elif beam.direction == "r":
                    beam.direction = "u"
                elif beam.direction == "d":
                    beam.direction = "l"
                elif beam.direction == "u":
                    beam.direction = "r"
                else:
                    raise Exception("Invalid direction")
            elif char == "-":
                if beam.direction in ["l", "r"]:
                    pass
                else:
                    if self.visited[beam.x, beam.y]:
                        to_delete.append(i)
                    else:
                        beam.direction = "l"
                        to_add.append(Beam(beam.x, beam.y, "r"))
            elif char == "|":
                if beam.direction in ["u", "d"]:
                    pass
                else:
                    if self.visited[beam.x, beam.y]:
                        to_delete.append(i)
                    else:
                        beam.direction = "u"
                        to_add.append(Beam(beam.x, beam.y, "d"))
            else:
                raise Exception("Invalid element")
        for i in to_delete[::-1]:
            self.beams.pop(i)
        for beam in to_add:
            self.add_beam(beam)
        for beam in self.beams:
            self.visited[beam.x, beam.y] = 1

    def is_out_of_bounds(self, beam):
        if beam.x < 0 or beam.x >= self.grid.shape[0]:
            return True
        elif beam.y < 0 or beam.y >= self.grid.shape[1]:
            return True
        else:
            return False
        
    def __str__(self):
        beam_grid = np.zeros_like(self.grid)
        for beam in self.beams:
            beam_grid[beam.x, beam.y] = 1
        result = ""
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                if beam_grid[row, col]:
                    result += "#"
                else:
                    result += self.grid[row, col]
            result += "\n"
        return result

    def add_beam(self, beam):
        self.beams.append(beam)

    def get_visited_str(self):
        result = ""
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                if self.visited[row, col]:
                    result += "#"
                else:
                    result += "."
            result += "\n"
        return result

    def get_number_of_visited(self):
        result = 0
        for row in range(self.grid.shape[0]):
            for col in range(self.grid.shape[1]):
                if self.visited[row, col]:
                    result += 1
        return result


found_max = -1

n = 10000

for i in range(x_size):
    board = Board(input)
    board.add_beam(Beam(i, -1, 'r'))
    visited = board.run(n)
    if visited > found_max:
        found_max = visited
for i in range(x_size):
    board = Board(input)
    board.add_beam(Beam(i, y_size, 'l'))
    visited = board.run(n)
    if visited > found_max:
        found_max = visited
for j in range(y_size):
    board = Board(input)
    board.add_beam(Beam(-1, j, 'd'))
    visited = board.run(n)
    if visited > found_max:
        found_max = visited
for j in range(y_size):
    board = Board(input)
    board.add_beam(Beam(x_size, j, 'u'))
    visited = board.run(n)
    if visited > found_max:
        found_max = visited

print(found_max)