WHITE = (255,255,255)


class Cells:
    def __init__(self):
        self.cells = [[WHITE] * 20 for _ in range(20)]
    def set_color(self, row, col, color):
        self.cells[row][col] = color
    def get_color(self, row, col):
        return self.cells[row][col]
    def clear(self):
        self.cells = [[WHITE] * 20 for _ in range(20)]