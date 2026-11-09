"""Run with: python3 -m unittest discover -s tests -v"""

import contextlib
import io
import unittest
from unittest.mock import patch

from tictactoe import GameQuit, WINNING_LINES, display, draw, finished, keep_playing, player_move, players, run_game


class TestGame(unittest.TestCase):
    def scripted(self, function, answers):
        output = io.StringIO()
        with patch("builtins.input", side_effect=answers), contextlib.redirect_stdout(output):
            result = function()
        return result, output.getvalue()

    def test_player_one_can_choose_x_or_o_and_case(self):
        for value, expected in (("X", ("X", "O")), ("o", ("O", "X")), (" x ", ("X", "O"))):
            with self.subTest(value=value):
                result, _ = self.scripted(players, [value])
                self.assertEqual(result, expected)

    def test_symbol_reprompt(self):
        result, text = self.scripted(players, ["bad", "1", "o"])
        self.assertEqual(result, ("O", "X"))
        self.assertEqual(text.count("Please choose X or O"), 2)

    def test_valid_moves_and_input_recovery(self):
        grid = list(range(1, 10))
        grid[0] = "O"
        _, text = self.scripted(lambda: player_move(grid, "X"), ["word", "0", "10", "1", "2"])
        self.assertEqual(grid[1], "X")
        self.assertIn("whole number", text)
        self.assertEqual(text.count("outside the range"), 2)
        self.assertIn("already taken", text)

    def test_all_eight_winning_lines_for_both_symbols(self):
        self.assertEqual(len(WINNING_LINES), 8)
        for line in WINNING_LINES:
            for symbol in ("X", "O"):
                with self.subTest(line=line, symbol=symbol):
                    grid = list(range(1, 10))
                    for index in line:
                        grid[index] = symbol
                    self.assertTrue(finished(grid, symbol))
                    self.assertFalse(finished(grid, "O" if symbol == "X" else "X"))

    def test_draw_not_a_win_and_win_not_a_draw(self):
        tie = ["X", "O", "X", "X", "O", "O", "O", "X", "X"]
        self.assertTrue(draw(tie))
        self.assertFalse(finished(tie, "X"))
        self.assertFalse(finished(tie, "O"))
        self.assertFalse(draw(["X"] * 9))
        self.assertFalse(draw(list(range(1, 10))))

    def test_display_is_readable(self):
        _, text = self.scripted(lambda: display(list(range(1, 10))), [])
        self.assertIn("1 | 2 | 3", text)
        self.assertIn("7 | 8 | 9", text)
        self.assertEqual(text.count("---+---+---"), 2)

    def test_play_again_answers(self):
        for answer, expected in (("YES", True), (" y ", True), ("N", False), ("no", False), ("q", False)):
            with self.subTest(answer=answer):
                result, _ = self.scripted(keep_playing, [answer])
                self.assertEqual(result, expected)

    def test_play_again_reprompt(self):
        result, text = self.scripted(keep_playing, ["??", "N"])
        self.assertFalse(result)
        self.assertIn("Please enter Y or N", text)

    def test_quit_from_select_or_move(self):
        with patch("builtins.input", return_value="q"):
            with self.assertRaises(GameQuit):
                players()
            with self.assertRaises(GameQuit):
                player_move(list(range(1, 10)), "X")

    def test_x_win_and_turn_switch(self):
        _, text = self.scripted(run_game, ["X", "1", "4", "2", "5", "3", "N"])
        self.assertIn("Player 1 (X) wins!", text)
        self.assertNotIn("Player 2 (O) wins!", text)
        self.assertEqual(text.count("---+---+---"), 12)  # initial + 5 moves

    def test_o_win_player_one(self):
        _, text = self.scripted(run_game, ["O", "1", "4", "2", "5", "3", "N"])
        self.assertIn("Player 1 (O) wins!", text)

    def test_second_player_can_win(self):
        _, text = self.scripted(run_game, ["X", "1", "2", "3", "5", "7", "8", "N"])
        self.assertIn("Player 2 (O) wins!", text)

    def test_q_during_game_exits_cleanly(self):
        _, text = self.scripted(run_game, ["X", "1", "q"])
        self.assertIn("Thanks for playing!", text)
        self.assertNotIn("wins!", text)

    def test_draw_game(self):
        _, text = self.scripted(run_game, ["X", "1", "2", "3", "5", "4", "6", "8", "7", "9", "N"])
        self.assertIn("The game is a draw!", text)
        self.assertNotIn("wins!", text)

    def test_replay_resets_board_and_can_exit(self):
        _, text = self.scripted(run_game, ["X", "1", "4", "2", "5", "3", "Y", "O", "1", "4", "2", "5", "3", "N"])
        self.assertEqual(text.count("wins!"), 2)
        self.assertIn("Starting a new game!", text)
        self.assertEqual(text.count("1 | 2 | 3"), 2)  # new board, numbered again
        self.assertTrue(text.endswith("Thanks for playing!\n"))

    def test_eof_graceful(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=EOFError), contextlib.redirect_stdout(output):
            run_game()
        self.assertIn("Input interrupted; ending game.", output.getvalue())
        self.assertIn("Thanks for playing!", output.getvalue())


if __name__ == "__main__":
    unittest.main()
