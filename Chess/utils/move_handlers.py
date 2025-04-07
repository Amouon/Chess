def process_algebraic_notation(algebraic_notation):
    """ Process algebraic notation and return a tuple of the form ((row, col), (row, col))

     :param algebraic_notation: The algebraic notation of the move
     :return: A tuple of the form ((row, col), (row, col))"""

    start = algebraic_notation[:2]
    end = algebraic_notation[2:]
    # Convert the start and end squares to row and column
    start = (int(start[1]) - 1, ord(start[0]) - 97)
    end = (int(end[1]) - 1, ord(end[0]) - 97)

    return end, start


def process_location(algebraic_notation):
    """ Process algebraic notation and return a tuple of the form (row, col)

     :param algebraic_notation: The algebraic notation of the square
     :return: A tuple of the form (row, col)"""
    start = algebraic_notation[:2]
    start = (int(start[1]) - 1, ord(start[0]) - 97)
    return start


def convert_to_algebraic_notation(position):
    """ Convert a tuple of the form (row, col) to algebraic notation

     :param position: A tuple of the form (row, col)
     :return: The algebraic notation of the square"""
    # Convert a position to algebraic notation
    row, col = position
    return chr(col + 97) + str(row + 1)


def print_board(repository):
    """ Print the board

     :param board: The board to print"""
    for i in range(len(repository.board)):
        string = []
        for j in range(len(repository.board[i])):
            if repository.board[i][j] is not None:
                string.append(repository.board[i][j])
            else:
                string.append("")
        print(string)
    print("\n")
