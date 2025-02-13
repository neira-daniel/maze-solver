import unittest

from graphics import Maze


class TestMaze(unittest.TestCase):
    def test_maze_create_cells(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        self.assertEqual(
            len(maze._cells),
            num_cols,
        )
        self.assertEqual(
            len(maze._cells[0]),
            num_rows,
        )

    def test_invalid_maze_dimensions(self):
        num_cols = 0
        num_rows = 10
        with self.assertRaises(ValueError):
            _ = Maze(0, 0, num_rows, num_cols, 10, 10)

    def test_invalid_window_parameter(self):
        num_cols = 5
        num_rows = 10
        window = "window"
        with self.assertRaises(TypeError):
            _ = Maze(0, 0, num_rows, num_cols, 10, 10, window=window)

    def test_break_entrance_and_exit(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        maze._break_entrance_and_exit()

        self.assertEqual(maze._cells[0][0].has_N_wall, False)

        self.assertEqual(maze._cells[-1][-1].has_S_wall, False)

    def test_visited_property(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        maze._break_entrance_and_exit()

        maze._break_walls_r(0, 0)

        visited = [
            maze._cells[i][j].visited
            for i in range(maze._num_cols)
            for j in range(maze._num_rows)
        ]

        self.assertTrue(any(visited))

    def test_reset_visited_property(self):
        num_cols = 12
        num_rows = 10
        maze = Maze(0, 0, num_rows, num_cols, 10, 10)
        maze._break_entrance_and_exit()

        maze._break_walls_r(0, 0)

        maze._reset_cells_visited()

        visited = [
            maze._cells[i][j].visited
            for i in range(maze._num_cols)
            for j in range(maze._num_rows)
        ]

        self.assertFalse(any(visited))


if __name__ == "__main__":
    unittest.main()
