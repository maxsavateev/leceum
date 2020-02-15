from random import choice

figures = {
    'I': [
        [
            [1, 1, 1, 1],
        ],
        [
            [1],
            [1],
            [1],
            [1],
        ],
    ],
    'O': [
        [
            [1, 1],
            [1, 1],
        ],
    ],
    'T': [
        [
            [0, 1, 0],
            [1, 1, 1],
        ],
        [
            [1, 0],
            [1, 1],
            [1, 0],
        ],
        [
            [1, 1, 1],
            [0, 1, 0],
        ],
        [
            [0, 1],
            [1, 1],
            [0, 1],
        ],
    ],
    'J': [
        [
            [1, 1, 1],
            [0, 0, 1],
        ],
        [
            [0, 1],
            [0, 1],
            [1, 1],
        ],
        [
            [1, 0, 0],
            [1, 1, 1],
        ],
        [
            [1, 1],
            [1, 0],
            [1, 0],
        ]
    ],
    'L': [
        [
            [1, 1, 1],
            [1, 0, 0]
        ],
        [
            [1, 1],
            [0, 1],
            [0, 1]
        ],
        [
            [0, 0, 1],
            [1, 1, 1]
        ],
        [
            [1, 0],
            [1, 0],
            [1, 1]
        ]
    ],
    'S': [
        [
            [0, 1, 1],
            [1, 1, 0]
        ],
        [
            [1, 0],
            [1, 1],
            [0, 1]
        ]
    ],
    'Z': [
        [
            [1, 1, 0],
            [0, 1, 1]
        ],
        [
            [0, 1],
            [1, 1],
            [1, 0]
        ]
    ]
}


class Figure:
    def __init__(self, states, brick):
        self.grid = []
        self.states = states
        self.brick = brick
        self.current_state = 0

        self.placed = False
        self.x = 0
        self.y = 0
        self.width = len(self.states[self.current_state][0])
        self.height = len(self.states[self.current_state])

    def place(self, grid, new_x, new_y, new_state) -> bool:
        width = len(self.states[new_state][0])
        height = len(self.states[new_state])
        if new_y >= 0 and new_y + height <= len(grid) and \
           new_x >= 0 and new_x + width <= len(grid[0]):
            tmp = [row.copy() for row in grid]
            if self.placed:
                self.clear()
            for x in range(width):
                for y in range(height):
                    if self.states[new_state][y][x]:
                        if grid[new_y + y][new_x + x] is not None:
                            grid.clear()
                            grid.extend(tmp)
                            return False
                        else:
                            grid[new_y + y][new_x + x] = self.brick
            self.placed = True
            self.x = new_x
            self.y = new_y
            self.width = width
            self.height = height
            self.current_state = new_state
            self.grid = grid
            return True
        else:
            return False

    def move(self, direction: str) -> bool:
        if direction == 'left':
            return self.place(self.grid, self.x - 1, self.y, self.current_state)
        elif direction == 'right':
            return self.place(self.grid, self.x + 1, self.y, self.current_state)
        elif direction == 'down':
            return self.place(self.grid, self.x, self.y + 1, self.current_state)
        else:
            return False

    def rotate(self) -> bool:
        new_state = self.current_state + 1
        if new_state >= len(self.states):
            new_state = 0
        print('state', new_state)
        return self.place(self.grid, self.x, self.y, new_state)

    def clear(self):
        for x in range(self.width):
            for y in range(self.height):
                if self.states[self.current_state][y][x]:
                    self.grid[self.y + y][self.x + x] = None


def random(bricks) -> Figure:
    name = choice(list(figures.keys()))
    return Figure(figures[name], choice(bricks))
