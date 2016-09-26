import random
import sys
import time

import pygame
from pygame.locals import *

DEAD_COLOR = (0, 0, 0)
ALIVE_COLOR = (0, 230, 0)


class Cell:
    """
    Represents a cell value.
    """

    def __init__(self, value):
        self.value = value
        self._last_draw_value = None

    def toggle(self):
        """
        Toggle cell value.
        """

        self.value = int(not bool(self.value))
        self._last_draw_value = None

    def draw(self, screen, loc, size=16, grid=False,
             dead=DEAD_COLOR, alive=ALIVE_COLOR):
        """
        Draw at location i, j assuming cells of the given size.
        """

        i, j = loc
        if self.value != self._last_draw_value:
            x, y = size * i, size * j
            if grid:
                rect = x, y, size - 1, size - 1
            else:
                rect = x, y, size, size
            cell_color = alive if self.value else dead
            pygame.draw.rect(screen, cell_color, rect)
            self._last_draw_value = self.value


class Board:
    """
    Store cells in a square board.
    """

    _instance = None

    @property
    def size(self):
        return len(self._data)

    @property
    def shape(self):
        return len(self._data), len(self._data[0])

    def __init__(self, M, N):
        self._data = [[Cell(0) for _ in range(N)] for _ in range(M)]
        self.future = {}
        Board._instance = self

    def __len__(self):
        return len(self._data)

    def __getitem__(self, idx):
        i, j = idx
        if i < 0 or j < 0:
            return 0
        try:
            return self._data[i][j].value
        except IndexError:
            return 0

    def __setitem__(self, idx, value):
        i, j = idx
        self._data[i][j].value = value

    def __iter__(self):
        for row in self._data:
            return [x.value for x in row]

    def fill_random(self, superimpose=False):
        """
        Fill board with random cells.
        """

        choices = [0, 0, 0, 1] if superimpose else [0, 1]
        M, N = self.shape
        if not superimpose:
            self.fill_dead()
        for i in range(M):
            for j in range(N):
                value = random.choice(choices)
                if value and not self._data[i][j].value:
                    self._data[i][j].value = 1

    def fill_dead(self):
        """
        Fill board with dead cells.
        """

        M, N = self.shape
        self._data = [[Cell(0) for _ in range(N)] for _ in range(M)]

    def fill_alive(self):
        """
        Fill board with dead cells.
        """

        M, N = self.shape
        self._data = [[Cell(1) for _ in range(N)] for _ in range(M)]

    def fill_grid(self, superimpose=False):
        """
        Fill board with dead cells.
        """

        M, N = self.shape
        if not superimpose:
            self.fill_dead()
        for i in range(M):
            for j in range(N):
                if not self._data[i][j].value and (i + j) % 2:
                    self._data[i][j].value = 1

    def fill_margin(self, superimpose=False):
        """
        Fills a margin with alive objects.
        """

        M, N = self.shape
        if not superimpose:
            self.fill_dead()
        for i in range(N):
            self._data[0][i].value = 1
            self._data[M - 1][i].value = 1
        for i in range(M):
            self._data[i][0].value = 1
            self._data[i][N - 1].value = 1

    def fill_row(self, i):
        """
        Fill the i-th row with live cells.
        """

        M, N = self.shape
        for j in range(N):
            self._data[i][j].value = self._data[i][j].value or 1

    def fill_col(self, j):
        """
        Fill the j-th col with live cells.
        """

        M, N = self.shape
        for i in range(M):
            self._data[i][j].value = self._data[i][j].value or 1

    def fill_inverted(self):
        """
        Invert all cell values.
        """

        for row in self._data:
            for cell in row:
                cell.toggle()

    def fill_hstripes(self, superimpose=False):
        """
        Fill board with horizontal stripes.
        """

        if not superimpose:
            self.fill_dead()

        M, N = self.shape
        for i in range(M):
            if i % 2:
                for j in range(N):
                    self._data[i][j].value = 1

    def fill_vstripes(self, superimpose=False):
        """
        Fill board with vertical stripes
        """

        if not superimpose:
            self.fill_dead()

        M, N = self.shape
        for j in range(N):
            if j % 2:
                for i in range(M):
                    self._data[i][j].value = 1

    def cell(self, i, j):
        """
        Return cell at location i, j.
        """

        return self._data[i][j]

    def cell_at_coords(self, x, y, size=16):
        """
        Return cell at screen position x, y.
        """

        i = int(x / size)
        j = int(y / size)
        return self.cell(i, j)

    def toggle(self, i, j):
        """
        Toggle value of cell at location (i, j)
        """

        self.cell(i, j).toggle()

    def draw(self, screen, **kwargs):
        """
        Draw board on screen.
        """

        for i, row in enumerate(self._data):
            for j, cell in enumerate(row):
                cell.draw(screen, (i, j), **kwargs)

    def copy(self):
        """
        Return a copy of board.
        """

        new = object.__new__(Board)
        new._data = [row.copy() for row in self._data]
        new.future = self.future.copy()


class World:
    """
    Controls simulation.
    """

    @classmethod
    def from_board(cls, board, rule=None, **kwargs):
        world = World(board.shape, rule=rule, **kwargs)
        world.board = board
        return world

    def __init__(self, board_size=32, cell_size=None,
                 dead_color=DEAD_COLOR,
                 alive_color=ALIVE_COLOR,
                 draw_grid=True, skip=15,
                 rule=None):
        if isinstance(board_size, int):
            board_size = board_size, board_size
        M, N = board_size
        if cell_size is None:
            cell_size = int(800 / max(M, N))
            cell_size = max(min(64, cell_size), 4)
        self.cell_size = cell_size
        self.board_size = board_size
        self.width = M * self.cell_size
        self.height = N * self.cell_size
        self.board = Board(M, N)
        self.steps = 0
        self.time = 0
        self.screen = None
        self.dead_color = dead_color
        self.alive_color = alive_color
        self.rule = rule or conway
        self.draw_grid = draw_grid
        self.skip = skip
        self._mainloop_running = False
        self._simulation_running = False
        self._initialized = False
        self._clock = None
        self._current_action = None

    def init(self):
        """
        Initializes Pygame.
        """

        if not self._initialized:
            pygame.init()
            self._clock = pygame.time.Clock()
            self.screen = pygame.display.set_mode((self.width, self.height))
        self._initialized = True

    def update(self):
        """
        Advance one simulation frame.
        """

        # Respond to events
        for event in pygame.event.get():
            if event.type == QUIT:
                self._mainloop_running = False

            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self._simulation_running = not self._simulation_running
                elif event.key == K_RIGHT and self.rule:
                    self.rule(self.board)
                elif event.key == K_s:
                    if event.mod & 64:
                        self.board.fill_hstripes(True)
                    else:
                        self.board.fill_vstripes(True)
                elif event.key == K_r:
                    self.board.fill_random(not event.mod & 64)
                elif event.key == K_d:
                    self.board.fill_dead()
                elif event.key == K_a:
                    self.board.fill_alive()
                elif event.key == K_g:
                    self.board.fill_grid(not event.mod & 64)
                elif event.key == K_m:
                    self.board.fill_margin(not event.mod & 64)
                elif event.key == K_i:
                    self.board.fill_inverted()
                elif event.key == K_l:
                    M, N = self.board_size
                    if random.choice([0, 1]):
                        idx = random.randrange(N)
                        self.board.fill_col(idx)
                    else:
                        idx = random.randrange(M)
                        self.board.fill_row(idx)
                elif event.key == K_UP:
                    self.skip = max(self.skip - 1, 1)
                elif event.key == K_DOWN:
                    self.skip = min(self.skip + 1, 60)

            if event.type == MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                cell = self.board.cell_at_coords(x, y, self.cell_size)
                self._current_action = not bool(cell.value)

            if event.type == MOUSEBUTTONUP:
                self._current_action = None

        # Respond to mouse events
        pressed = pygame.mouse.get_pressed()
        if any(pressed):
            x, y = pygame.mouse.get_pos()
            cell = self.board.cell_at_coords(x, y, self.cell_size)
            if bool(cell.value) != self._current_action:
                cell.toggle()

        # Update simulation
        if self._simulation_running and self.rule:
            if self.steps % self.skip == 0:
                self.time = time.time()
                self.rule(self.board)

        # Update simulation drawing
        self.board.draw(self.screen, size=self.cell_size, grid=self.draw_grid,
                        dead=self.dead_color,
                        alive=self.alive_color)

        # Apply future changes, if any
        if self.board.future:
            for (i, j), value in self.board.future.items():
                self.board[i, j] = value
            self.board.future.clear()

        # Update pygame and simulation parameters
        pygame.display.flip()
        if self._simulation_running:
            dt = time.time() - self.time
            if dt < 1 / 60:
                time.sleep(1 / 60 - dt)
                self.time = time.time()
            else:
                self.time += 1 / 60
        else:
            time.sleep(1 / 60)

        self.steps += 1

    def run(self):
        """
        Simulation main loop.
        """

        self.init()
        self.time = time.time()
        self._mainloop_running = True
        while self._mainloop_running:
            self.update()
        pygame.quit()


def conway(board, prob=1):
    """
    Conway's rules for the Game of life with a probabilistic twist.
    """

    # Iterate over all cells picking up the ones that should change
    M, N = board.shape
    for i in range(M):
        for j in range(N):
            value = board[i, j]

            # Count alive neighbors
            alive_neighbors = 0
            for a in [-1, 0, 1]:
                for b in [-1, 0, 1]:
                    if board[i + a, j + b]:
                        alive_neighbors += 1

            # Correct offset (the previous loop includes the cell itself)
            if value:
                alive_neighbors -= 1

            # Apply Conway's rules
            if value and (alive_neighbors >= 4 or alive_neighbors <= 1):
                if random.random() < prob ** (alive_neighbors - 3):
                    board.future[i, j] = 0
            elif not value and alive_neighbors == 3:
                if random.random() < prob:
                    board.future[i, j] = 1
            elif not value and alive_neighbors == 2 and prob != 1:
                if random.random() < min(1 - prob, prob):
                    board.future[i, j] = 1


def run(rule=None, board=None):
    """
    Runs simulation.
    """

    if rule is None or board is None:
        frame = sys._getframe(-2)
        glob = frame.f_globals
        if rule is None:
            rule = glob.get('rule', None)
        if board is None:
            board = Board._instance or Board(32, 32)

    if isinstance(rule, str):
        if rule == 'conway':
            rule = conway
        elif rule.startswith('conway'):
            _, prob = rule.split('-')
            prob = float(prob) / 100

            def rule(board):
                conway(board, prob)
        else:
            raise ValueError('unknown rule: %r' % rule)
    elif rule is None:
        rule = lambda b: None

    world = World.from_board(board, rule=rule)
    world.run()
