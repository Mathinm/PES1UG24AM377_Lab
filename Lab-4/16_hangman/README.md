# Scenario 16 — Hangman Challenge

A multi-round terminal word-guessing game with categories, hints, scoring, and streaks.

## Provided files

- `main.py` — entry point.
- `game.py` — round state, guesses, hints, scoring, and session flow.
- `words.py` — in-memory word and hint data.
- `stats.py` — session statistics support.
- `requirements.txt` — dependency declaration.

## Setup

```bash
python main.py
```

## Before changing the code

Run several rounds and inspect how round state, score, guessed letters, and category
selection are represented. Reproduce the Task 1 issue before modifying it.

## Task 1 — Guess-state correctness

Correct repeated-guess handling so a previously attempted wrong letter cannot consume
another life, and a previously accepted correct letter cannot be counted as a new guess.

**Done when:** each distinct letter affects the round exactly once.

## Task 2 — Complete the session model

Integrate the supplied session-statistics component so rounds played, rounds won, and
best streak are tracked correctly across multiple rounds.

**Done when:** starting a new round resets only round-specific state; session statistics
continue across the whole run.

## Task 3 — Difficulty and scoring

Add difficulty choices that alter the available lives and scoring. Preserve category
selection and make hint usage affect scoring consistently.

**Done when:** difficulty changes round rules without leaking state between rounds.

## Task 4 — Robust input and feedback

Improve command handling for invalid letters, repeated commands, category selection,
and hint usage. Feedback should describe actual player actions once.

**Done when:** malformed input never changes game state and feedback is not duplicated.

## Required testing

Test repeated correct and incorrect guesses, hints, category changes, multiple rounds,
streak resets, difficulty changes, invalid input, and quitting.


## LLM usage

You may use an LLM during the lab. The goal is to use it as a coding assistant while
retaining responsibility for understanding and testing the result.

- Inspect the existing code before asking for changes.
- Ask for explanations when you do not understand a proposed change.
- Test generated code against the stated behaviour and edge cases.
- Keep your complete LLM chat history for submission.
- Do not replace the whole project with an unrelated implementation.
- Keep all state in memory; do not add CSV, JSON, SQLite, or other persistence.

## Submission checklist

- [ ] Task 1 completed and the original defect was reproduced and fixed.
- [ ] Tasks 2–4 completed and tested.
- [ ] Boundary and invalid-input cases tested.
- [ ] No unnecessary external dependencies added.
- [ ] No persistent storage added.
- [ ] Code remains understandable and modular.
- [ ] Complete LLM chat-history link included.

## Folder structure

```text
scenario-04-hangman/
├── README.md
├── requirements.txt
├── main.py
├── game.py
├── words.py
└── stats.py
```

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
