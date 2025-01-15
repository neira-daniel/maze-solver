from tkinter import Tk, BOTH, Canvas


class Window:
    """
    Object that manages Tkinter windows on screen.
    """

    def __init__(self, width: int, height: int) -> None:
        """Initializes a Window object without displaying it on screen."""
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title("Maze Solver")

        self.__canvas = Canvas(master=self.__root, width=width, height=height)
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
