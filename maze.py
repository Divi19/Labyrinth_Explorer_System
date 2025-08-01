from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

from config import Directions, Tiles
from hollows import Hollow, MysticalHollow, SpookyHollow
from treasure import Treasure
from data_structures.linked_stack import LinkedStack


class Position:
    def __init__(self, row: int, col: int) -> None:
        """
        Args:
            row(int): Row number in this maze cell position
            col(int): Column number in this maze cell position
        """
        self.row: int = row
        self.col: int = col

    def __eq__(self, value: object) -> bool:
        return isinstance(value, Position) and value.row == self.row and value.col == self.col

    def __repr__(self):
        return str(self)

    def __str__(self) -> str:
        return f"({self.row}, {self.col})"


@dataclass
class MazeCell:
    tile: str | Hollow
    position: Position
    visited: bool = False

    def __str__(self) -> str:
        return str(self.tile)

    def __repr__(self) -> str:
        return f"'{self.tile}'"


class Maze:
    directions: dict[Directions, Tuple[int, int]] = {
        Directions.UP: (-1, 0),
        Directions.DOWN: (1, 0),
        Directions.LEFT: (0, -1),
        Directions.RIGHT: (0, 1),
    }

    def __init__(self, start_position: Position, end_positions: List[Position], walls: List[Position], hollows: List[tuple[Hollow, Position]], rows: int, cols: int) -> None:
        """
        Constructs the maze you should never be interacting with this method.
        Please take a look at `load_maze_from_file` & `sample1`

        Args:
            start_position(Position): Starting position in the maze.
            end_positions(List[Position]): End positions in the maze.
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            rows(int): Number of rows in the maze.
            cols(int): Number of columns in the maze.

        Complexity:
            Best Case Complexity: O(_create_grid)
            Worst Case Complexity: O(_create_grid)
        """
        self.start_position: Position = start_position
        self.end_positions: List[Position] = end_positions
        self.rows: int = rows
        self.cols: int = cols
        self.grid: List[List[MazeCell]] = self._create_grid(walls, hollows, end_positions)

    def _create_grid(self, walls: List[Position], hollows: List[(Hollow, Position)], end_positions: List[Position]) -> List[List[MazeCell]]:
        """
        Args:
            walls(List[Position]): Walls in the maze.
            hollows(List[Position]): Hollows in the maze.
            end_positions(List[Position]): End positions in the maze.

        Return:
            List[MazeCell]: The generated maze grid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.
        """
        grid: List[List[MazeCell]] = [[MazeCell(' ', Position(i, j))
                                       for j in range(self.cols)] for i in range(self.rows)]
        grid[self.start_position.row][self.start_position.col] = MazeCell(
            Tiles.START_POSITION.value, self.start_position)
        for wall in walls:
            grid[wall.row][wall.col].tile = Tiles.WALL.value
        for hollow, pos in hollows:
            grid[pos.row][pos.col].tile = hollow
        for end_position in end_positions:
            grid[end_position.row][end_position.col].tile = Tiles.EXIT.value
        return grid

    @staticmethod
    def validate_maze_file(maze_name: str) -> None:
        """
        Mazes must have the following:
        - A start position (P)
        - At least one exit (E)
        - All rows must have the same number of columns
        - Tiles are representations can be found in config.py
        - At least one treasure

        Args:
            maze_name(str): The name of the maze.

        Raises:
            ValueError: If maze_name is invalid.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            Assuming dictionary operations can be done on O(1) time.
        """
        tile_count: dict[str, int] = {}
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            cols: int = len(lines[0].strip())
            for line in lines:
                if len(line.strip()) != cols:
                    raise ValueError(f"Uneven columns in {maze_name} ensure all rows have the same number of columns")
                # Check tiles
                for tile in line.strip():
                    if tile not in tile_count:
                        tile_count[tile] = 1
                    else:
                        tile_count[tile] += 1
        if 'P' not in tile_count or 'E' not in tile_count:
            raise ValueError(f"Missing start or end position in {maze_name}")

        if tile_count['P'] > 1:
            raise ValueError(f"Multiple start positions found in {maze_name}")

        # Check we have at least one treasure
        if not (Tiles.SPOOKY_HOLLOW.value in tile_count or Tiles.MYSTICAL_HOLLOW.value in tile_count):
            raise ValueError(f"No treasures found in {maze_name}")

        valid_types: List[str] = [tile.value for tile in Tiles]
        invalid_tiles: List[str] = [tile for tile in tile_count if tile not in valid_types]
        if invalid_tiles:
            raise ValueError(f"Invalid tile(s) found in {maze_name} ({invalid_tiles})")

    @classmethod
    def load_maze_from_file(cls, maze_name: str) -> Maze:
        """
        Args:
            maze_name(str): The maze name to load the maze from.

        Return:
            Maze: The newly created maze instance.

        Complexity:
            Best Case Complexity: O(N) where N is the number of cells in the maze.
            Worst Case Complexity: O(N) where N is the number of cells in the maze.

            For small mazes we assume the lists we not need to resize.
        """
        cls.validate_maze_file(maze_name)
        end_positions, walls, hollows = [], [], []
        mystical_hollow: MysticalHollow = MysticalHollow()
        start_position: Position | None = None
        with open(f"./mazes/{maze_name}", 'r') as f:
            lines: List[str] = f.readlines()
            rows: int = len(lines)
            cols: int = len(lines[0].strip())
            for i, line in enumerate(lines):
                for j, tile in enumerate(line.strip()):
                    if tile == Tiles.START_POSITION.value:
                        start_position: Position = Position(i, j)
                    elif tile == Tiles.EXIT.value:
                        end_positions.append(Position(i, j))
                    elif tile == Tiles.WALL.value:
                        walls.append(Position(i, j))
                    elif tile == Tiles.SPOOKY_HOLLOW.value:
                        hollows.append((SpookyHollow(), Position(i, j)))
                    elif tile == Tiles.MYSTICAL_HOLLOW.value:
                        hollows.append((mystical_hollow, Position(i, j)))
        assert start_position is not None
        return Maze(start_position, end_positions, walls, hollows, rows, cols)

    def is_valid_position(self, position: Position) -> bool:
        """
        Checks if the position is within the maze and not blocked by a wall.

        Args:
            position (Position): The position to check.

        Returns:
            bool - True if the position is within the maze and not blocked by a wall.

        Complexity:
        Both the best and worst case is O(1) since we are using simple comparison operators and return statements which are
        all O(1) complexity.

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        #Check if position is in the maze and that the position is not a wall
        rows, columns = position.row, position.col

        #Not in maze
        if rows < 0 or rows >= self.rows or columns < 0 or columns >= self.cols:
            return False

        maze_position = self.grid[rows][columns]

        #Obstacles or visited tiles
        if maze_position.tile == Tiles.WALL.value or maze_position.visited:
            return False
        
        return True

    def get_available_positions(self, current_position: Position) -> List[Position]:
        """
        Returns a list of all the new possible you can move to from your current position.

        Args:
            current_position (Position): Your current position.

        Returns:
            List[Position] - A list of all the new possible you can move to from your current position.

        Complexity:
        Both the best and worst case complexity is O(1) because the for loop itself only runs for a fixed number of iterations and in
        this case it loops over the 4 possible exit locations which is complexity of O(4) which is just simplified to O(1) constant time complexity.
        The is_valid position has best and worst case of O(1) and the append method also has O(1) complexity. Thus, the final complexity for best and worst
        case is just O(1).

            Best Case Complexity: O(1)
            Worst Case Complexity: O(1)
        """
        rows, column = current_position.row, current_position.col
        exit_postions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        positions_available_to_move = []

        for alter_row, alter_column in exit_postions:
            found_position = (rows + alter_row, column + alter_column)
            positional_object = Position(found_position[0], found_position[1])
            if self.is_valid_position(positional_object):
                positions_available_to_move.append(positional_object)

        return positions_available_to_move

    def find_way_out(self) -> List[Position] | None:
        """
        Finds a way out of the maze in some cases there may be multiple exits
        or no exits at all.

        Returns:
            List[Position]: If there is a way out of the maze, 
            the path will be made up of the coordinates starting at 
            your original starting point and ending at the exit.

            None: Unable to find a path to the exit, simply return None.

        Complexity:
        In both the best and worst case the depth first search has to travel a certain number of mazecells in order to reach the
        end. Despite, the best case being that the path is found sooner and vists fewer locations, the complexity still remains the same at O(n) 
        as it still needs to track the visited number of mazecells since it still needs to mark the cells as visited and track the path. In the worst-case
        it travels all of the n mazecells, hence, O(n).

            Best Case Complexity: O(n) where n is the number of mazecells on the grid
            Worst Case Complexity: O(n) where n is the number of mazecells on the grid
        """
        start: Position = self.start_position
        # current_pos = start
        path_found = []
        # there_is_a_path = False

        def depth_first_search(current_pos):
            #Marks position and adds it to the stack for a potential path
            rows, columns = current_pos.row, current_pos.col
            maze_position = self.grid[rows][columns]
            maze_position.visited = True
            path_found.append(current_pos)
            # print(path_found.peek())
            if maze_position.tile == Tiles.EXIT.value:
                return True

            for possible_positions in self.get_available_positions(current_pos):
                if depth_first_search(possible_positions):
                    return True
                
            path_found.pop()
            return False
        
        if depth_first_search(start):
            return path_found
        else:
            return None

    def take_treasures(self, path: List[MazeCell], backpack_capacity: int) -> List[Treasure] | None:
        """
        You must take the treasures in the order they appear in the path selecting treasures
        that have the highest value / weight ratio.
        Remember the total of treasures cannot exceed backpack_capacity, which means
        Individual treasures cannot exceed this value either.

        Should there be no treasures that are viable please return an empty list.

        You do not have to validate the path, it is guaranteed to be a valid path.

        Args:
            path (List[MazeCell]): The path you took to reach the exit.
            backpack_capacity (int): The maximum weight you can carry.

        Returns:
            List[Treasure] - List of the most optimal treasures.
            None - If there are no treasures to take.

        Complexity:
        The best-case complexity occurs when there are no hollow instances on the path for both spooky and mystical hollow. This would mean that only
        the for loop is iterated over to go through the mazecells in the path list which has a complexity of O(m) where m is the number of maze cells
        in the path list.

        The worst-case complexity occurs when each maze cell has a mystical hollow instance in its location. Since we have to go though m number of maze cells, the
        complexity of the for loop itself is O(m). The worst-case complexity for get_optimal_treasure() occurs when almost all the treasures that were called by the get_max method, had a weight greater than the backpack capacity
        meaning that the while loop had to go though n-1 iterations and each time it had to call the get_max method which has complexity of O(logn) for best and worst
        case. Hence, the while loop has a complexity of O(n * logn) which simplfies to O(nlogn). The for loop will have had to go through n-1 iterations to add back all the invalid
        treasures back into the max heap leading to a complexity of O(nlogn) where we go through n iterations and the worst-case of add is O(logn) where the element added has to rise all the
        way up to the root. Therefore, we have a complexity of O(nlogn + nlogn) which can be simplified to a worst-case complexity of O(nlogn).  Therfore, combining both these complexities give O(m * nlogn).

            Best Case Complexity: O(m) where m is the number of maze cells in the path list
            Worst Case Complexity: O(m * nlogn) where m is the number of mazecells in the path list and n is the number of treasures in
            the hollow

        """
        treasures_collected = []
        for cell in path:
            if isinstance(cell.tile, SpookyHollow):
                hollow = cell.tile
                treasure = hollow.get_optimal_treasure(backpack_capacity)
                if treasure is not None:
                    backpack_capacity -= treasure.weight
                    treasures_collected.append(treasure)

            if isinstance(cell.tile, MysticalHollow):
                hollow = cell.tile
                treasure = hollow.get_optimal_treasure(backpack_capacity)
                if treasure is not None:
                    backpack_capacity -= treasure.weight
                    treasures_collected.append(treasure)

        if len(treasures_collected) == 0:
            return None
        
        return treasures_collected


    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        """
        Returns the grid in a human-readable format.

        Complexity:
        Best Case Complexity: O(n) where n is the number of cells in the maze.
        Worst Case Complexity: O(n) where n is the number of cells in the maze.
        """
        my_grid: str = ""
        for row in self.grid:
            my_grid += "" if my_grid == "" else "\n"
            my_grid += str(row)

        return my_grid


def sample1() -> None:
    maze = Maze.load_maze_from_file("sample.txt")
    print(maze)


def sample2() -> None:
    maze = Maze.load_maze_from_file("sample2.txt")
    print(maze)
    # Samples as to how the grid / maze cells work
    r, c = 4, 0  # row 4, col 0
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))
    r, c = 2, 3  # row 2, col 3
    print(maze.grid[r][c].position, type(maze.grid[r][c]), f"Visited: {maze.grid[r][c].visited}")
    print(maze.grid[r][c].tile, type(maze.grid[r][c].tile))


if __name__ == "__main__":
    sample1()
