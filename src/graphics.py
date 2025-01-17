from tkinter import Tk, BOTH, Canvas
import time
from typing import Optional
import warnings
import random


class Window:
    """
    Object that manages Tkinter windows on screen.
    """

    def __init__(
        self, width: int, height: int, background_color: str = "white"
    ) -> None:
        """Initializes a Window object without displaying it on screen."""
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title("Maze Solver")

        self._width = width
        self._height = height

        self._background_color = background_color

        self.__canvas = Canvas(
            master=self.__root,
            width=self._width,
            height=self._height,
            background=self._background_color,
        )
        self.__canvas.pack()

        self.__running = False

    def redraw(self) -> None:
        """Refreshes the Window object."""
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self) -> None:
        """Keeps the Window object alive and disposes of it gracefully when the user
        presses the close button."""
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        """Sends the closing signal to the Window object."""
        self.__running = False

    def draw_line(self, line: "Line", fill_color: str = "black") -> None:
        line.draw(canvas=self.__canvas, fill_color=fill_color)


class Point:
    """
    Object that stores 2D-point coordinates in pixels.
    """

    def __init__(self, x: int | float, y: int | float) -> None:
        """Initializes a Point object with `x` being the horizontal direction and `y` the vertical.

        Note that the origin coordinate (x=0, y=0) represents the top left of the window."""
        self.x = int(x)
        self.y = int(y)

    def __add__(self, other: "Point") -> "Point":
        return Point(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Point") -> "Point":
        return Point(self.x - other.x, self.y - other.y)

    def __mul__(self, factor: int | float) -> "Point":
        """Handles Point object * factor"""
        if isinstance(factor, (int, float)):
            return Point(int(self.x * factor), int(self.y * factor))
        return NotImplemented

    def __rmul__(self, factor: int | float) -> "Point":
        """Handles factor * Point object"""
        return self.__mul__(factor)

    def get_coordinates(self):
        return self.x, self.y


class Line:
    """
    Object that represents 2D lines.
    """

    def __init__(self, point_A: "Point", point_B: "Point"):
        self.point_A = point_A
        self.point_B = point_B

    def draw(self, canvas: Canvas, fill_color: str = "black"):
        """Draws a line between two Point objects.

        Valid string colors for `fill_color` can be found here:
        https://www.tcl.tk/man/tcl8.4/TkCmd/colors.htm"""
        x1, y1 = self.point_A.get_coordinates()
        x2, y2 = self.point_B.get_coordinates()
        canvas.create_line(x1, y1, x2, y2, fill=fill_color, width=2)


class Cell:
    """
    Object that represents the units or cells that comprise the maze.

    Each Cell object stores the position of said object in the canvas and which of
    its walls are active.
    """

    def __init__(
        self,
        top_left: "Point",
        bottom_right: "Point",
        window: Optional["Window"] = None,
    ) -> None:
        self._x1, self._y1 = top_left.get_coordinates()
        self._x2, self._y2 = bottom_right.get_coordinates()

        self._win = window

        self.has_N_wall = True
        self.has_S_wall = True
        self.has_E_wall = True
        self.has_W_wall = True

        self._north = Line(Point(self._x1, self._y1), Point(self._x2, self._y1))
        self._south = Line(Point(self._x1, self._y2), Point(self._x2, self._y2))
        self._east = Line(Point(self._x2, self._y1), Point(self._x2, self._y2))
        self._west = Line(Point(self._x1, self._y1), Point(self._x1, self._y2))

        # to track which cells have been visited
        # this will mean different things in different contexts
        # when solving the maze it will mean just that: which cells have been visited
        # during the process
        # but, when creating it, it keeps track of whether the cell has been visited
        # to break down one of its walls in a depth-first like algorithm
        self.visited = False

    def draw(self, fill_color: str = "black"):
        if self._win is None:
            return
        walls = zip(
            [self.has_N_wall, self.has_S_wall, self.has_E_wall, self.has_W_wall],
            [self._north, self._south, self._east, self._west],
        )
        for active, line in walls:
            if active:
                self._win.draw_line(line, fill_color)
            else:
                self._win.draw_line(line, self._win._background_color)

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
        if self._win is None:
            return
        line_color = "gray" if undo else "red"
        start = Point(0.5 * (self._x2 + self._x1), 0.5 * (self._y2 + self._y1))
        finish = Point(
            0.5 * (to_cell._x2 + to_cell._x1), 0.5 * (to_cell._y2 + to_cell._y1)
        )
        start_to_finish = Line(start, finish)
        self._win.draw_line(start_to_finish, line_color)


class Maze:
    """
    Deals with the Cell objects in the maze.
    """

    def __init__(
        self,
        x0: int | float,
        y0: int | float,
        num_rows: int | float,
        num_cols: int | float,
        cell_size_x: int | float,
        cell_size_y: int | float,
        window: Optional["Window"] = None,
        seed: Optional[int] = None,
    ) -> None:
        if num_rows < 1 or num_cols < 1:
            raise ValueError("Invalid number of rows or columns")
        if window is not None and not isinstance(window, Window):
            raise TypeError(
                "Invalid `window` parameter. It must be `window: Optional[Windows]`"
            )
        if seed is not None and not isinstance(seed, int):
            raise TypeError("`seed` parameter can only be int | None")

        if not isinstance(x0, int) or not isinstance(y0, int):
            warnings.warn("Casting origin coordinates to int", UserWarning)
        if not isinstance(num_rows, int) or not isinstance(num_cols, int):
            warnings.warn("Casting number of cells to int", UserWarning)
        if not isinstance(cell_size_x, int) or not isinstance(cell_size_y, int):
            warnings.warn("Casting cell dimensions to int", UserWarning)

        self._x0 = int(x0)
        self._y0 = int(y0)
        self._num_rows = int(num_rows)
        self._num_cols = int(num_cols)
        self._cell_size_x = int(cell_size_x)
        self._cell_size_y = int(cell_size_y)
        self._win = window

        self._seed = seed
        if self._seed is not None:
            random.seed(self._seed)

        self._create_cells()

    def _create_cells(self) -> None:
        self._cells = []

        x, y = self._x0, self._y0

        for column in range(self._num_cols):
            self._cells.append(
                [
                    Cell(
                        Point(x, y + k * self._cell_size_y),
                        Point(x + self._cell_size_x, y + (k + 1) * self._cell_size_y),
                        self._win,
                    )
                    for k in range(self._num_rows)
                ]
            )
            x += self._cell_size_x

        if self._win is None:
            return

        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._draw_cell(i, j)

        self._break_entrance_and_exit()

        self._break_walls_r()

        self._reset_cells_visited()

    def _draw_cell(self, i, j) -> None:
        if self._win is None:
            return
        self._cells[i][j].draw()
        self._animate()

    def _animate(self) -> None:
        if self._win is None:
            return
        self._win.redraw()
        time.sleep(0.05)

    def _break_entrance_and_exit(self) -> None:
        starting_cell = self._cells[0][0]
        starting_cell.has_N_wall = False
        self._draw_cell(0, 0)

        finishing_cell = self._cells[-1][-1]
        finishing_cell.has_S_wall = False
        self._draw_cell(-1, -1)

    def _break_walls_r(self, i: int = 0, j: int = 0) -> None:
        if not isinstance(i, int) or not isinstance(j, int):
            raise TypeError("index `i` and `j` should be int")
        # depth-first traversal-like algorithm
        self._cells[i][j].visited = True
        while True:
            # check whether neighbors are yet to be visited
            to_visit = []
            # northern neighbor
            ii, jj = i, j - 1
            if j > 1 and not self._cells[ii][jj].visited:
                to_visit.append((ii, jj))
            # southern neighbor
            ii, jj = i, j + 1
            if j < self._num_rows - 1 and not self._cells[ii][jj].visited:
                to_visit.append((ii, jj))
            # eastern neighbor
            ii, jj = i + 1, j
            if i < self._num_cols - 1 and not self._cells[ii][jj].visited:
                to_visit.append((ii, jj))
            # western neighbor
            ii, jj = i - 1, j
            if i > 1 and not self._cells[ii][jj].visited:
                to_visit.append((ii, jj))

            N_neighbors_to_visit = len(to_visit)
            if N_neighbors_to_visit == 0:
                # no neighbors to visit
                self._draw_cell(i, j)
                return

            # pick a yet to be visited neighbor at random
            next_i, next_j = to_visit[random.randrange(N_neighbors_to_visit)]
            # break down the walls between the current cell and the next
            if i < next_i:
                self._cells[i][j].has_E_wall = False
                self._cells[next_i][next_j].has_W_wall = False
            elif next_i < i:
                self._cells[i][j].has_W_wall = False
                self._cells[next_i][next_j].has_E_wall = False
            elif j < next_j:
                self._cells[i][j].has_S_wall = False
                self._cells[next_i][next_j].has_N_wall = False
            else:
                self._cells[i][j].has_N_wall = False
                self._cells[next_i][next_j].has_S_wall = False

            # go on to another adventure
            self._break_walls_r(next_i, next_j)

    def _reset_cells_visited(self) -> None:
        for i in range(self._num_cols):
            for j in range(self._num_rows):
                self._cells[i][j].visited = False
