from graphics import Window, Line, Point


def main():
    win = Window(800, 600)
    point_A = Point(100, 100)
    point_B = Point(400, 400)
    line_1 = Line(point_A, 0.5 * point_B)
    line_2 = Line(point_A + point_B, point_B - point_A)
    win.draw_line(line_1, "firebrick")
    win.draw_line(line_2, "dark olive green")
    win.wait_for_close()


if __name__ == "__main__":
    main()
