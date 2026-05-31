#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from event_planner.crew import EventPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

GUEST_LIST_STR = """
1. Alice: Attending, Vegetarian, Prefers not to sit next to Bob
2. Bob: Attending, No restrictions, Prefers sitting next to Charlie
3. Charlie: Attending, Gluten-free, Prefers sitting next to Bob
4. David: Not attending
5. Eve: Attending, Vegan, Prefers sitting near the window
"""
GUESTS = ["Alice", "Bob", "Charlie", "David", "Eve"]

def run():
    """
    Run the crew.
    """
    inputs = {
        'guest_list': GUEST_LIST_STR,
        'current_year': str(datetime.now().year)
    }

    try:
        EventPlanner(guests=GUESTS).crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'guest_list': GUEST_LIST_STR,
        'current_year': str(datetime.now().year)
    }
    try:
        EventPlanner(guests=GUESTS).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EventPlanner(guests=GUESTS).crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'guest_list': GUEST_LIST_STR,
        'current_year': str(datetime.now().year)
    }

    try:
        EventPlanner(guests=GUESTS).crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
