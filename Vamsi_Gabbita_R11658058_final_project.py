import argparse
from multiprocessing import Process, Manager


class Cell:
    """Cell Class - each node in the matrix"""

    def __init__(self, x: int, y: int, value=None):
        """Init."""
        self.x = x
        self.y = y
        self.value = value


def parse_args() -> argparse.Namespace:
    """Arg parser helper"""
    parser = argparse.ArgumentParser(
        prog="StepAnalyzer",
        description="Computes the next 100 steps",
    )

    parser.add_argument(
        "-i",
        metavar="input_file",
        type=str,
        help="Input file - full path",
        required=True,
    )

    parser.add_argument(
        "-o",
        metavar="output_file",
        type=str,
        help="Input file - full path",
        required=True,
    )

    parser.add_argument(
        "-t",
        metavar="thread_count",
        type=int,
        help="Total number of threads",
        required=False,
        default=1,
    )

    args = parser.parse_args()

    return args


def read_matrix(input_file: str) -> list:
    """Read input file."""
    with open(input_file) as f:
        contents = f.readlines()

    matrix = []
    for line in contents:
        clean_line = line.strip()
        row = []
        for char in clean_line:
            row.append(char)
        if len(row) > 0:
            matrix.append(row)

    return matrix


def pretty_print(matrix: list) -> None:
    """Just print."""
    for row in matrix:
        print(" ".join(row))


def get_next_status(process_id: int, old_matrix: list, indices: list, output) -> None:
    """Get the status of next timeslot for the given list of indices."""
    for cell in indices:
        x = cell.x
        y = cell.y

        is_alive = True if old_matrix[x][y] == "+" else False
        alive_neighbor_count = get_living_neighbors(old_matrix, x, y)

        # Alive when currently alive and even neighbors being alive OR
        # Alive when currently dead but have prime number of alive neighbors
        if (is_alive and alive_neighbor_count in [2, 4, 6]) or (
            not is_alive and alive_neighbor_count in [2, 3, 5, 7]
        ):
            cell.value = "+"
        else:
            cell.value = "-"

    # Return value
    output[process_id] = indices


def run(old_matrix: list, row_count: int, col_count: int, process_count: int) -> list:
    """Find next time period matrix."""
    # init new matrix
    new_matrix = [["-" for _ in range(col_count)] for _ in range(row_count)]
    processes = []
    indices = []
    output = Manager().dict()

    # Compute Indices
    for i in range(row_count):
        for j in range(col_count):
            indices.append(Cell(x=i, y=j))

    # split indices into list with process_count number of sub-lists
    slices = {}
    for process_id in range(process_count):
        slices[process_id] = []

    process_id = 0
    for cell in indices:
        slices[process_id].append(cell)
        process_id = (process_id + 1) % process_count

    for index in range(process_count):
        p = Process(
            target=get_next_status, args=(index, old_matrix, slices[index], output)
        )
        p.start()
        processes.append(p)

    # Wait for all of them to complete
    for p in processes:
        p.join()

    # Stitch it back
    for process_id in range(process_count):
        for cell in output[process_id]:
            new_matrix[cell.x][cell.y] = cell.value

    return new_matrix


def dump_matrix(matrix: list, output_file: str) -> None:
    """Print Matrix to file"""
    with open(output_file, "w") as f:
        for row in matrix:
            f.write("".join(row) + "\n")


def main():
    """Main logic"""
    # Get command line arguments
    args = parse_args()

    # Read input file
    matrix = read_matrix(args.i)
    # pretty_print(matrix)

    col_count = len(matrix[0])
    row_count = len(matrix)

    for _ in range(100):
        matrix = run(matrix, row_count, col_count, args.t)

    pretty_print(matrix)
    dump_matrix(matrix, args.o)


def get_living_neighbors(matrix: list, x: int, y: int) -> int:
    """Get all neighbors in an order"""
    row_count = len(matrix)
    col_count = len(matrix[x])

    # print(f"Matrix firest line: {matrix[0]}")
    # print(f"Matrix last line: {matrix[-1]}")
    # print(f"({x}, {y})")
    # print(f"({row_count}, {col_count})")

    neighbors = [
        matrix[(x - 1) % row_count][(y - 1) % col_count],
        matrix[(x - 1) % row_count][y % col_count],
        matrix[(x - 1) % row_count][(y + 1) % col_count],
        matrix[x % row_count][(y - 1) % col_count],
        matrix[x % row_count][(y + 1) % col_count],
        matrix[(x + 1) % row_count][(y - 1) % col_count],
        matrix[(x + 1) % row_count][y % col_count],
        matrix[(x + 1) % row_count][(y + 1) % col_count],
    ]

    alive_count = 0
    for val in neighbors:
        if val == "+":
            alive_count += 1

    return alive_count


if __name__ == "__main__":
    print("Project :: R11658058")
    main()
