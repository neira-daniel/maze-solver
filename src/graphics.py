from tkinter import Tk, BOTH, Canvas
import time


class Window:
    """
    Object that manages Tkinter windows on screen.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes a Window object without displaying it on screen."""
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title("Maze Solver")

        self._width = width
        self._height = height

        self.__canvas = Canvas(
            master=self.__root, width=self._width, height=self._height
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
        self, top_left: "Point", bottom_right: "Point", window: "Window"
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

    def draw(self, fill_color: str = "black"):
        walls = zip(
            [self.has_N_wall, self.has_S_wall, self.has_E_wall, self.has_W_wall],
            [self._north, self._south, self._east, self._west],
        )
        for active, line in walls:
            if active:
                self._win.draw_line(line, fill_color)

    def draw_move(self, to_cell: "Cell", undo: bool = False) -> None:
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
        num_rows: int,
        num_cols: int,
        cell_size_x: int,
        cell_size_y: int,
        win: "Window",
    ) -> None:
        self._x0 = x0
        self._y0 = y0
        self._num_rows = num_rows
        self._num_cols = num_cols
        self._cell_size_x = cell_size_x
        self._cell_size_y = cell_size_y
        self._win = win

        self._create_cells()

    def _create_cells(self) -> None:
        self._cells = []

        x, y = self._x0, self._y0

        for row in range(self._num_rows):
            self._cells.append(
                [
                    Cell(
                        Point(x + k * self._cell_size_x, y),
                        Point(x + (k + 1) * self._cell_size_x, y + self._cell_size_y),
                        self._win,
                    )
                    for k in range(self._num_cols)
                ]
            )
            y += self._cell_size_y

        for i in range(self._num_rows):
            for j in range(self._num_cols):
                self._draw_cell(i, j)

    def _draw_cell(self, i, j):
        self._cells[i][j].draw()
        self._animate()

    def _animate(self):
        self._win.redraw()
        time.sleep(0.05)
