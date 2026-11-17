"""
verify_questions.py - a "spell checker" for your question file.

It opens a JSON file full of questions and checks that each one is built
correctly. It does NOT check the maths (that is a different script).

How to run it:
    python scripts/verify_questions.py data/questions_ratio_proportion.json

If you give no file name, it uses the default path below.
"""

import json
import sys

# The file to check if you don't type one in the command line.
DEFAULT_FILE = "data/questions_ratio_proportion.json"

# Every question MUST have all of these "boxes" (fields).
REQUIRED_FIELDS = [
    "id", "topic", "question", "options", "answer",
    "solution_steps", "trick", "difficulty", "target_seconds",
]

VALID_LETTERS = ["A", "B", "C", "D"]


def check_question(q, position):
    """Look at ONE question. Return a list of problems (empty list = no problems)."""
    problems = []

    # --- Check 1: are all the required fields there? ---
    for field in REQUIRED_FIELDS:
        if field not in q:
            problems.append(f"missing field '{field}'")

    # --- Check 2: exactly 4 options, and no two the same ---
    options = q.get("options")
    if options is not None:
        if not isinstance(options, list) or len(options) != 4:
            count = len(options) if isinstance(options, list) else "not a list"
            problems.append(f"needs exactly 4 options, found: {count}")
        else:
            # Remove the "A. " label so we compare only the real answer text.
            # Example: "A. Rs. 750" becomes "Rs. 750"
            texts = [str(opt).split(".", 1)[-1].strip().lower() for opt in options]
            if len(set(texts)) != len(texts):
                problems.append("has duplicate options")

    # --- Check 3: the answer is A, B, C or D, and that option exists ---
    answer = q.get("answer")
    if answer is not None:
        if answer not in VALID_LETTERS:
            problems.append(f"answer '{answer}' is not one of A, B, C, D")
        elif isinstance(options, list):
            # Does any option start with that letter, like "C." ?
            letters_in_options = [str(opt).strip()[:1] for opt in options]
            if answer not in letters_in_options:
                problems.append(f"answer '{answer}' does not match any option")

    # --- Check 4: solution_steps is a list with something in it ---
    steps = q.get("solution_steps")
    if steps is not None:
        if not isinstance(steps, list) or len(steps) == 0:
            problems.append("solution_steps must be a non-empty list")
        elif any(not str(s).strip() for s in steps):
            problems.append("solution_steps contains an empty step")

    return problems


def main():
    # Pick the file: the one typed after the script name, or the default.
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE

    # Open the file. If it's missing or broken JSON, say so and stop.
    try:
        with open(path, encoding="utf-8") as f:
            questions = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: cannot find file '{path}'")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: '{path}' is not valid JSON: {e}")
        sys.exit(1)

    if not isinstance(questions, list):
        print("ERROR: the file must contain a list (array) of questions")
        sys.exit(1)

    all_problems = []  # we collect every problem here
    seen_ids = set()   # ids we have already met, to catch repeats

    for position, q in enumerate(questions, start=1):
        # Use the id as the name if we have one, otherwise the position.
        name = q.get("id", f"question #{position}") if isinstance(q, dict) else f"question #{position}"

        if not isinstance(q, dict):
            all_problems.append(f"{name}: is not a JSON object")
            continue

        # --- Check 5: ids must be unique ---
        qid = q.get("id")
        if qid is not None:
            if qid in seen_ids:
                all_problems.append(f"{name}: duplicate id")
            seen_ids.add(qid)

        # Run the checks above and remember anything found.
        for problem in check_question(q, position):
            all_problems.append(f"{name}: {problem}")

    # --- Report ---
    if all_problems:
        print(f"Found {len(all_problems)} problem(s):\n")
        for p in all_problems:
            print(f"  - {p}")
        sys.exit(1)  # exit code 1 = "something is wrong" (useful later for automation)
    else:
        print(f"Checked {len(questions)} questions.")
        print("All checks passed")


if __name__ == "__main__":
    main()
