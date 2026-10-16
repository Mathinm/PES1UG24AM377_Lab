# Lab 5: Static Code Analysis — Animal Shelter Adoption Register

**Your file:** `pet_shelter.py`

Follow the lab handout for the full instructions.

## About the program

A register for an animal shelter. It records pets in an SQLite database, processes adoptions, finds the oldest pet still available, issues adoption codes and clears out unadopted records.

The code works, but only just. It has quality, style and security problems of the kind Pylint, Flake8 and Bandit are built to find.

## What to do

1. **Run it first** and read the output carefully:
   ```bash
   python pet_shelter.py
   ```
   It runs a short demonstration and may create a small output file in the current folder, so run it from a folder you don't mind adding files to.

2. **Install the tools:**
   ```bash
   pip install pylint bandit flake8
   ```

3. **Run the analysis** and save the reports:
   ```bash
   pylint pet_shelter.py > pylint_report.txt
   bandit -r pet_shelter.py > bandit_report.txt
   flake8 pet_shelter.py > flake8_report.txt
   ```

4. **Document the issues** in `issues.md` using this table (at least 4 rows, high and medium severity first):

   | Issue | Type | Line(s) | Description | Fix Approach |
   |-------|------|---------|-------------|--------------|
   | ... | ... | ... | ... | ... |

5. **Fix the code.** Fix at least 4 of the issues you documented, then rerun all three tools to confirm they are gone. Repeat until you are satisfied. The program should still do its job when you are done.

6. **Reflect.** Answer the four reflection questions from the handout in `reflection.md`.

## Deliverables

1. `pet_shelter.py`: your cleaned version, with at least 4 issues fixed.
2. `issues.md`: the completed issue table.
3. `reflection.md`: your answers to the reflection questions.

**Target:** aim for a Pylint score above 9.5 on your final file. A perfect 10.00/10 is very good.

Be ready to explain the bugs you found and how you fixed them. You may be called on to present.
