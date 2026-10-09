"""Run with:  python -m unittest -v test_game"""
import unittest
from unittest import mock

import game
from game import HangmanGame, Round, DIFFICULTIES, round_points


def scripted(inputs, secrets=()):
    """A game driven by a list of inputs; returns (game, captured output)."""
    feed = iter(inputs)
    out = []

    def fake_input(_prompt=""):
        try:
            return next(feed)
        except StopIteration:
            raise EOFError  # behave like a closed terminal

    g = HangmanGame(input_fn=fake_input, output_fn=out.append)
    if secrets:
        it = iter(secrets)
        g.start_round_orig = g.start_round
        g.start_round = lambda secret=None: g.start_round_orig(next(it))
    return g, out


class Task1RepeatedGuesses(unittest.TestCase):
    def test_repeated_wrong_letter_costs_one_life_only(self):
        r = Round("python", "normal")
        r.guess("z")
        r.guess("z")
        r.guess("z")
        self.assertEqual(r.lives, 5)
        self.assertEqual(r.wrong, {"z"})

    def test_repeated_correct_letter_counts_once(self):
        r = Round("python", "normal")
        first = r.guess("p")
        second = r.guess("p")
        self.assertTrue(first.startswith("Correct"))
        self.assertIn("already", second)
        self.assertEqual(r.correct, {"p"})
        self.assertEqual(r.lives, 6)

    def test_repeated_letter_in_word_is_one_guess(self):
        r = Round("galaxy", "normal")
        msg = r.guess("a")
        self.assertIn("2 times", msg)
        self.assertEqual(r.masked(), "_ a _ a _ _")


class Task2Session(unittest.TestCase):
    def test_new_round_resets_only_round_state(self):
        g = HangmanGame()
        g.start_round("python")
        g.round.guess("z")
        g.round.use_hint()
        for ch in "python":
            g.round.guess(ch)
        g.finish_round()
        score, streak = g.score, g.streak
        g.start_round("galaxy")
        self.assertEqual(g.round.wrong, set())
        self.assertEqual(g.round.correct, set())
        self.assertFalse(g.round.hint_used)
        self.assertEqual(g.round.lives, 6)
        self.assertEqual((g.score, g.streak), (score, streak))
        self.assertEqual(g.stats.rounds, 1)

    def test_stats_and_streak_reset(self):
        g = HangmanGame()
        for word, win in [("python", True), ("network", True), ("galaxy", False), ("enzyme", True)]:
            g.start_round(word)
            if win:
                for ch in word:
                    g.round.guess(ch)
            else:
                for ch in "qwbdfj":
                    g.round.guess(ch)
                self.assertTrue(g.round.lost())
            g.finish_round()
        self.assertEqual(g.stats.rounds, 4)
        self.assertEqual(g.stats.wins, 3)
        self.assertEqual(g.stats.best_streak, 2)
        self.assertEqual(g.streak, 1)


class Task3DifficultyScoring(unittest.TestCase):
    def test_lives_follow_difficulty(self):
        for name, rules in DIFFICULTIES.items():
            self.assertEqual(Round("python", name).lives, rules["lives"])

    def test_difficulty_does_not_leak_between_rounds(self):
        g = HangmanGame()
        g.difficulty = "hard"
        g.start_round("python")
        self.assertEqual(g.round.lives, 4)
        g.difficulty = "easy"
        g.start_round("python")
        self.assertEqual(g.round.lives, 8)

    def test_scoring(self):
        self.assertEqual(round_points(True, 1, "easy", False), 6)
        self.assertEqual(round_points(True, 1, "normal", False), 12)
        self.assertEqual(round_points(True, 1, "hard", False), 18)
        self.assertEqual(round_points(True, 1, "hard", True), 15)
        self.assertEqual(round_points(False, 0, "hard", True), 0)

    def test_hint_cost_consistent_even_at_zero_score(self):
        # Original bug: hint was free when score was 0.
        g = HangmanGame()
        g.start_round("python")
        g.round.use_hint()
        for ch in "python":
            g.round.guess(ch)
        _, points = g.finish_round()
        self.assertEqual(points, round_points(True, 1, "normal", False) - 2)

    def test_second_hint_not_charged_again(self):
        r = Round("python", "normal")
        r.use_hint()
        msg = r.use_hint()
        self.assertIn("already used", msg)
        self.assertTrue(r.hint_used)


class Task4Input(unittest.TestCase):
    def setUp(self):
        self.g = HangmanGame()
        self.g.start_round("python")

    def state(self):
        r = self.g.round
        return (r.lives, set(r.correct), set(r.wrong), r.hint_used, self.g.score)

    def test_malformed_input_never_changes_state(self):
        before = self.state()
        for raw in ["", "ab", "1", "?", " ", "é", "/foo", "/hints", "python"]:
            msg, quit_ = self.g.handle_input(raw)
            self.assertFalse(quit_)
            self.assertIn("Nothing changed" if not raw.startswith("/") else "Unknown", msg)
        self.assertEqual(self.state(), before)

    def test_quit(self):
        _, quit_ = self.g.handle_input("/quit")
        self.assertTrue(quit_)


class FullSession(unittest.TestCase):
    def test_scripted_session(self):
        inputs = [
            "maths", "1", "",        # bad category, then technology, default difficulty
            "z", "z", "pp", "/hint", "/hint",
            "p", "y", "t", "h", "o", "n",
            "maybe", "y",            # bad y/n answer, then yes
            "", "3",                 # keep category, hard
            "/quit",
        ]
        g, out = scripted(inputs, secrets=["python", "network"])
        g.run()
        text = "\n".join(out)
        self.assertEqual(text.count("Wrong: 'z'"), 1)
        self.assertIn("already tried 'z'", text)
        self.assertIn("Solved: python", text)
        self.assertIn("Please answer y or n.", text)
        self.assertIn("New round: technology, hard (4 lives", text)
        self.assertIn("Rounds played: 1", text)
        self.assertIn("Best streak:   1", text)
        self.assertIn("Final score:   10", text)  # (5+1)*2 - 2 hint

    def test_eof_prints_summary(self):
        g, out = scripted([])
        g.run()
        self.assertIn("Session summary", "\n".join(out))


if __name__ == "__main__":
    unittest.main()
