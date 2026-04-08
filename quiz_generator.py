# -*- coding: utf-8 -*-
"""
Created on Wed Apr  8 19:22:13 2026

@author: shris
"""

import json
import re
import random

QUESTIONS_FILE = "questions.json"
MAX_ATTEMPTS = 3

QUESTIONS = [
    {
        "question": "What is the capital of France?",
        "options": ["A. Berlin", "B. Madrid", "C. Paris", "D. Rome"],
        "answer": "C",
        "hint": "It's known as the City of Light."
    },
    {
        "question": "Which planet is closest to the Sun?",
        "options": ["A. Venus", "B. Earth", "C. Mars", "D. Mercury"],
        "answer": "D",
        "hint": "It's the smallest planet in the solar system."
    },
    {
        "question": "What is 12 x 12?",
        "options": ["A. 132", "B. 144", "C. 124", "D. 148"],
        "answer": "B",
        "hint": "Think of a dozen dozens."
    },
    {
        "question": "Who wrote Hamlet?",
        "options": ["A. Charles Dickens", "B. Jane Austen", "C. William Shakespeare", "D. Leo Tolstoy"],
        "answer": "C",
        "hint": "To be or not to be..."
    },
    {
        "question": "What is the chemical symbol for water?",
        "options": ["A. WA", "B. HO", "C. H2O", "D. OX"],
        "answer": "C",
        "hint": "Two hydrogens and one oxygen."
    }
]


def main():

    questions = load_questions()
    score = run_quiz(questions)
    total = len(questions)
    percent = calculate_percent(score,total)
    print()
    print(f"Final score: {score}/{total} ({percent}%)")


def load_json(filepath, fallback):

    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        return fallback


def save_json(filepath, data):

    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_questions():

    questions = load_json(QUESTIONS_FILE, None)
    if questions is None:
        save_json(QUESTIONS_FILE, QUESTIONS)
        return QUESTIONS
    if not questions:
        raise ValueError(f"'{QUESTIONS_FILE}' is empty.")
    return questions


def is_valid_answer(ans):
    return bool(re.match(r"^[A-D]$", ans.strip().upper()))


def get_answer_input():

    while True:
        ans = input("  Your answer (A/B/C/D): ").strip().upper()
        if is_valid_answer(ans):
            return ans
        print("Please enter A, B, C, or D.")


def run_quiz(questions):

    score = 0
    random.shuffle(questions)

    for i, q in enumerate(questions, 1):
        print(f"\nQ{i}/{len(questions)}: {q['question']}")
        for opt in q["options"]:
            print(f"  {opt}")

        correct = q["answer"].strip().upper()
        hint = q.get("hint")

        for attempt in range(1, MAX_ATTEMPTS + 1):
            ans = get_answer_input()
            if ans == correct:
                print("Correct!")
                score += 1
                break
            else:
                remaining = MAX_ATTEMPTS - attempt
                if remaining == 0:
                    print(f"Wrong. The correct answer was {correct}.")
                elif remaining == 1 and hint:
                    print(f"Wrong. Hint: {hint}")
                else:
                    print(f"Wrong. {remaining} attempt(s) remaining.")

    return score


def calculate_percent(correct, total):
    if total == 0:
        raise ValueError("Total questions cannot be zero.")
    return round(correct / total * 100)


if __name__ == "__main__":
    main()