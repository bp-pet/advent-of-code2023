class Block:
    def __init__(self, start: tuple[int], end: tuple[int]):
        self.start = start
        self.end = end
        self.get_base()
        
        if start[0] > end[0] or start[1] > end[1] or start[2] > end[2]:
            raise Exception("This should be fixed")
    
    def move_down_to(self, new_height):
        temp = self.end[2] - self.start[2]
        self.start[2] = new_height
        self.end[2] = new_height + temp
    
    def get_lowest_on_axis(self, axis: int):
        # axis is 0, 1, or 2
        return self.start[axis]
    
    def get_highest_on_axis(self, axis: int):
        # axis is 0, 1, or 2
        return self.end[axis]

    def get_base(self):
        self.base = set()
        for i in range(self.start[0], self.end[0] + 1):
            for j in range(self.start[1], self.end[1] + 1):
                self.base.add((i, j))
    
    def __str__(self):
        return f"Block from {self.start} to {self.end}"


class Field:
    def __init__(self, blocks: list[Block]):
        self.blocks = blocks
        self.floor = None
        self.sort_blocks_vertically()
    
    def sort_blocks_vertically(self):
        self.blocks.sort(key=lambda x: x.get_lowest_on_axis(2))
    
    def __str__(self):
        result = "Field with:"
        for block in self.blocks:
            result += "\n  " + str(block)
        return result
    
    def drop_all(self):
        free_blocks = [True] * len(self.blocks)
        for i, block in enumerate(self.blocks):
            new_height = 1
            support = []
            for j, other_block in enumerate(self.blocks[:i]):
                if len(block.base.intersection(other_block.base)) > 0:
                    temp = other_block.get_highest_on_axis(2) + 1
                    if temp > new_height:
                        new_height = temp
                        support = [j]
                    elif temp == new_height:
                        support.append(j)
            block.move_down_to(new_height)
            if len(support) == 1:
                free_blocks[support[0]] = False
        return sum(free_blocks)

class Parser:
    def __init__(self):
        pass

    def parse_file(self, filename) -> Field:
        with open(filename, "r") as f:
            raw = f.read()
        return self.parse_str(raw)
    
    def parse_str(self, raw) -> Field:
        blocks = []
        for line in raw.split("\n"):
            start_raw, end_raw = line.split("~")
            start_coords = [int(i) for i in start_raw.split(",")]
            end_coords = [int(i) for i in end_raw.split(",")]
            blocks.append(Block(start_coords, end_coords))
        return Field(blocks)
    
field = Parser().parse_file("day22.txt")
print(field.drop_all())