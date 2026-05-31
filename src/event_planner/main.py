#!/usr/bin/env python
import sys
import warnings

from datetime import datetime

from event_planner.crew import EventPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

def run():
    """
    Run the crew.
    """
    guest_list_str = """
    1. Alice: Attending, Vegetarian, Prefers not to sit next to Bob
    2. Bob: Attending, No restrictions, Prefers sitting next to Charlie
    3. Charlie: Attending, Gluten-free, Prefers sitting next to Bob
    4. David: Not attending
    5. Eve: Attending, Vegan, Prefers sitting near the window
    """

    inputs = {
        'guest_list': guest_list_str,
        'current_year': str(datetime.now().year)
    }

    try:
        EventPlanner().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")

def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        'guest_list': "1. Alice: Attending, Vegetarian",
        'current_year': str(datetime.now().year)
    }
    try:
        EventPlanner().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        EventPlanner().crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'guest_list': "1. Alice: Attending, Vegetarian",
        'current_year': str(datetime.now().year)
    }

    try:
        EventPlanner().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
