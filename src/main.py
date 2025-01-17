from graphics import Window, Maze


def main():
    win = Window(800, 600)
    _ = Maze(
        x0=50,
        y0=50,
        num_rows=5,
        num_cols=4,
        cell_size_x=100,
        cell_size_y=100,
        window=win,
    )
    win.wait_for_close()


if __name__ == "__main__":
    main()
