import random
from words import WORDS, HINTS
from stats import SessionStats

# Difficulty changes the rules of a round: how many lives you get, how much a
# win is worth, and how much using the hint costs.
DIFFICULTIES = {
    "easy": {"lives": 8, "multiplier": 1, "hint_cost": 1},
    "normal": {"lives": 6, "multiplier": 2, "hint_cost": 2},
    "hard": {"lives": 4, "multiplier": 3, "hint_cost": 3},
}
DEFAULT_DIFFICULTY = "normal"
DEFAULT_CATEGORY = "technology"
BASE_WIN_POINTS = 5


def parse_letter(raw):
    """Return a single lowercase a-z letter, or None if the input is not one."""
    if len(raw) == 1 and "a" <= raw <= "z":
        return raw
    return None


def round_points(won, streak, difficulty, hint_used):
    """Points earned by a round. `streak` is the streak *including* this round.

    A loss earns nothing. A win earns (base + streak) * multiplier, and the
    hint always costs exactly `hint_cost` from that reward (never below 0).
    """
    if not won:
        return 0
    rules = DIFFICULTIES[difficulty]
    points = (BASE_WIN_POINTS + streak) * rules["multiplier"]
    if hint_used:
        points -= rules["hint_cost"]
    return max(points, 0)


class Round:
    """Everything that belongs to ONE round. A new round = a new Round object,
    so round state can never leak into the next round."""

    def __init__(self, secret, difficulty):
        self.secret = secret
        self.difficulty = difficulty
        self.lives = DIFFICULTIES[difficulty]["lives"]
        self.correct = set()
        self.wrong = set()
        self.hint_used = False

    def masked(self):
        return " ".join(ch if ch in self.correct else "_" for ch in self.secret)

    def won(self):
        return set(self.secret) <= self.correct

    def lost(self):
        return self.lives <= 0

    def over(self):
        return self.won() or self.lost()

    def guess(self, letter):
        """Apply a validated letter. Each distinct letter changes state once."""
        if letter in self.correct:
            return f"You already found '{letter}'. Nothing changed."
        if letter in self.wrong:
            return f"You already tried '{letter}' and it is not in the word. No life lost."
        if letter in self.secret:
            self.correct.add(letter)
            count = self.secret.count(letter)
            times = "time" if count == 1 else "times"
            return f"Correct: '{letter}' appears {count} {times}."
        self.wrong.add(letter)
        self.lives -= 1
        return f"Wrong: '{letter}' is not in the word. Lives left: {self.lives}."

    def use_hint(self):
        """Reveal the hint. Only the first use is charged."""
        text = HINTS.get(self.secret, "No hint available.")
        if self.hint_used:
            return f"Hint (already used, no extra cost): {text}"
        self.hint_used = True
        cost = DIFFICULTIES[self.difficulty]["hint_cost"]
        return f"Hint: {text}  (-{cost} from this round's win reward)"


class HangmanGame:
    """Session-level state: score, streak, statistics, and the player's
    current category/difficulty choices. Lives across all rounds."""

    def __init__(self, input_fn=input, output_fn=print):
        self.input = input_fn
        self.output = output_fn
        self.score = 0
        self.streak = 0
        self.stats = SessionStats()
        self.category = DEFAULT_CATEGORY
        self.difficulty = DEFAULT_DIFFICULTY
        self.round = None

    # ---- round lifecycle -------------------------------------------------

    def start_round(self, secret=None):
        secret = secret or random.choice(WORDS[self.category])
        self.round = Round(secret, self.difficulty)
        return self.round

    def finish_round(self):
        """Apply the result of the finished round to session state."""
        won = self.round.won()
        self.streak = self.streak + 1 if won else 0
        points = round_points(won, self.streak, self.round.difficulty, self.round.hint_used)
        self.score += points
        self.stats.record(won, self.streak)
        return won, points

    # ---- prompts ---------------------------------------------------------

    def ask_choice(self, label, options, current):
        """Ask for one of `options` by name or number. Enter keeps `current`.
        Returns the choice, or None if the player typed q."""
        menu = ", ".join(f"{i}) {name}" for i, name in enumerate(options, 1))
        while True:
            self.output(f"\n{label}: {menu}")
            raw = self.input(f"Choose {label.lower()} [Enter = {current}, q = quit]: ").strip().lower()
            if raw == "q":
                return None
            if raw == "":
                return current
            if raw in options:
                return raw
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            self.output(f"'{raw}' is not a valid {label.lower()}. Try again.")

    def ask_yes_no(self, prompt):
        while True:
            raw = self.input(prompt).strip().lower()
            if raw in ("y", "yes"):
                return True
            if raw in ("n", "no", "q"):
                return False
            self.output("Please answer y or n.")

    # ---- gameplay --------------------------------------------------------

    def show_status(self):
        r = self.round
        cost = DIFFICULTIES[r.difficulty]["hint_cost"]
        hint = "used" if r.hint_used else f"available (/hint, costs {cost})"
        self.output(f"\nWord:  {r.masked()}")
        self.output(f"Wrong: {' '.join(sorted(r.wrong)) or '-'}")
        self.output(
            f"Lives: {r.lives}  Score: {self.score}  Streak: {self.streak}  "
            f"[{self.category} / {r.difficulty}]  Hint: {hint}"
        )

    def handle_input(self, raw):
        """Process one line of round input. Returns (message, quit_requested).
        Invalid input never changes state."""
        if raw == "/quit":
            return None, True
        if raw == "/hint":
            return self.round.use_hint(), False
        if raw.startswith("/"):
            return f"Unknown command '{raw}'. Use a letter, /hint, or /quit.", False
        letter = parse_letter(raw)
        if letter is None:
            shown = raw if raw else "(nothing)"
            return f"'{shown}' is not a single letter a-z. Nothing changed.", False
        return self.round.guess(letter), False

    def play_round(self):
        """Play one round. Returns 'won', 'lost', or 'quit'."""
        self.start_round()
        self.output(f"\nNew round: {self.category}, {self.difficulty} "
                    f"({self.round.lives} lives, {len(self.round.secret)} letters)")
        while not self.round.over():
            self.show_status()
            raw = self.input("Letter, /hint, or /quit: ").strip().lower()
            message, quit_requested = self.handle_input(raw)
            if quit_requested:
                self.output(f"Round abandoned. The word was: {self.round.secret}")
                return "quit"
            self.output(message)

        won, points = self.finish_round()
        if won:
            rules = DIFFICULTIES[self.round.difficulty]
            base = BASE_WIN_POINTS + self.streak
            breakdown = f"({BASE_WIN_POINTS} + streak {self.streak}) x {rules['multiplier']} = {base * rules['multiplier']}"
            if self.round.hint_used:
                breakdown += f", hint -{rules['hint_cost']}"
            self.output(f"\nSolved: {self.round.secret}  +{points} points  [{breakdown}]")
            return "won"
        self.output(f"\nOut of lives. The word was: {self.round.secret}  (streak reset)")
        return "lost"

    def summary(self):
        s = self.stats
        rate = f"{100 * s.wins // s.rounds}%" if s.rounds else "-"
        return (
            "\n=== Session summary ===\n"
            f"Rounds played: {s.rounds}\n"
            f"Rounds won:    {s.wins} ({rate})\n"
            f"Best streak:   {s.best_streak}\n"
            f"Final score:   {self.score}"
        )

    def run(self):
        self.output("Hangman Challenge")
        self.output("A session consists of multiple rounds.")
        try:
            while True:
                category = self.ask_choice("Category", list(WORDS), self.category)
                if category is None:
                    break
                self.category = category
                difficulty = self.ask_choice("Difficulty", list(DIFFICULTIES), self.difficulty)
                if difficulty is None:
                    break
                self.difficulty = difficulty
                if self.play_round() == "quit":
                    break
                if not self.ask_yes_no("Another round? [y/n]: "):
                    break
        except (EOFError, KeyboardInterrupt):
            self.output("\nInput closed.")
        self.output(self.summary())
