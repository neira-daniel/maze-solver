from tkinter import Tk, BOTH, Canvas


class Window:
    def __init__(self, width: int, height: int) -> None:
        self.__root = Tk()
        self.__root.protocol("WM_DELETE_WINDOW", self.close)
        self.__root.title("Maze Solver")

        self.__canvas = Canvas(master=self.__root, width=width, height=height)
        self.__canvas.pack()

        self.__running = False

    def redraw(self) -> None:
        self.__root.update()
        self.__root.update_idletasks()

    def wait_for_close(self) -> None:
        self.__running = True
        while self.__running:
            self.redraw()

    def close(self) -> None:
        self.__running = False
