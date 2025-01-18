from graphics import Window, Maze


def main():
    win = Window(800, 600)
    maze = Maze(
        x0=50,
        y0=50,
        num_rows=10,
        num_cols=14,
        cell_size_x=50,
        cell_size_y=50,
        window=win,
        seed=None,
    )
    maze.solve()
    win.wait_for_close()


if __name__ == "__main__":
    main()
