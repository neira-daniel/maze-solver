from graphics import Window, Maze


def main():
    win = Window(800, 600)
    # point_A = Point(100, 100)
    # point_B = Point(400, 400)
    # line_1 = Line(point_A, 0.5 * point_B)
    # line_2 = Line(point_A + point_B, point_B - point_A)
    # win.draw_line(line_1, "firebrick")
    # win.draw_line(line_2, "dark olive green")
    # cell_1 = Cell(0.5 * point_B, point_B - point_A, win)
    # cell_1.draw()
    # cell_2 = Cell(point_A + point_B, 1.1 * (point_A + point_B), win)
    # cell_2.has_W_wall = False
    # cell_2.draw()
    # cell_3 = Cell(Point(500, 100), Point(600, 200), win)
    # cell_3.has_S_wall = False
    # cell_3.has_E_wall = False
    # cell_4 = Cell(Point(500, 200), Point(600, 300), win)
    # cell_4.has_N_wall = False
    # cell_5 = Cell(Point(600, 100), Point(700, 200), win)
    # cell_5.has_W_wall = False
    # cell_3.draw("orange1")
    # cell_4.draw("green4")
    # cell_5.draw("black")
    # cell_3.draw_move(cell_4)
    # cell_3.draw_move(cell_5, True)
    _ = Maze(
        x0=50, y0=50, num_rows=5, num_cols=4, cell_size_x=100, cell_size_y=100, win=win
    )
    win.wait_for_close()


if __name__ == "__main__":
    main()
