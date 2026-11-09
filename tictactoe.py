"""Two-player terminal Tic Tac Toe (Noughts and Crosses)."""

WINNING_LINES = (
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # columns
    (0, 4, 8), (2, 4, 6),             # diagonals
)


class GameQuit(Exception):
    """A player requested an early exit with Q."""


def players():
    """Ask Player 1 for a symbol; return (player_1, player_2)."""
    while True:
        answer = input("Player 1, choose X or O (Q to quit): ").strip().upper()
        if answer == "Q":
            raise GameQuit
        if answer in ("X", "O"):
            second = "O" if answer == "X" else "X"
            print(f"Player 1 is {answer}; Player 2 is {second}.")
            return answer, second
        print("Please choose X or O (or Q to quit).")


def display(grid):
    """Print numbered empty spaces and symbols in a 3x3 board."""
    for start in (0, 3, 6):
        print(" " + " | ".join(str(cell) for cell in grid[start:start + 3]))
        if start < 6:
            print("---+---+---")
    print()


def player_move(grid, symbol):
    """Read a legal move and update the board in place."""
    while True:
        answer = input(f"Player {symbol}, choose a position (1-9, Q to quit): ").strip()
        if answer.upper() == "Q":
            raise GameQuit
        try:
            position = int(answer)
        except ValueError:
            print("Please enter a whole number from 1 to 9.")
            continue
        if position not in range(1, 10):
            print("That position is outside the range 1-9.")
            continue
        if grid[position - 1] in ("X", "O"):
            print("That position is already taken.")
            continue
        grid[position - 1] = symbol
        return


def finished(grid, symbol):
    """Return True if symbol occupies an entire row, column or diagonal."""
    return any(all(grid[index] == symbol for index in line)
               for line in WINNING_LINES)


def draw(grid):
    """Return True only for a full board without a winner."""
    return (all(cell in ("X", "O") for cell in grid)
            and not finished(grid, "X")
            and not finished(grid, "O"))


def keep_playing():
    """Ask whether to start a fresh round."""
    while True:
        answer = input("Play again? (Y/N, Q to quit): ").strip().lower()
        if answer in ("y", "yes"):
            return True
        if answer in ("n", "no", "q"):
            return False
        print("Please enter Y or N (or Q to quit).")


def run_game():
    """Run consecutive two-player rounds until the players decide to leave."""
    print("Tic Tac Toe — two players. Enter Q at any prompt to quit.\n")
    try:
        while True:
            grid = list(range(1, 10))
            player1_symbol, player2_symbol = players()
            current_symbol = player1_symbol
            display(grid)

            while True:
                player_move(grid, current_symbol)
                display(grid)  # print the board immediately after every legal move

                if finished(grid, current_symbol):
                    number = 1 if current_symbol == player1_symbol else 2
                    print(f"Player {number} ({current_symbol}) wins!")
                    break
                if draw(grid):
                    print("The game is a draw!")
                    break
                current_symbol = (player2_symbol if current_symbol == player1_symbol
                                  else player1_symbol)

            if not keep_playing():
                break
            print("\nStarting a new game!\n")
    except GameQuit:
        pass
    except (EOFError, KeyboardInterrupt):
        print("\nInput interrupted; ending game.")
    print("Thanks for playing!")


if __name__ == "__main__":
    run_game()
