#!/usr/bin/env python
import sys
import warnings
from datetime import datetime

from event_planner.crew import EventPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

GUESTS_DATA = [
    {"guest_name": "Alice", "attending": "Yes", "dietary": "Vegetarian", "seating": "Must not sit next to Bob or Charlie. Wants to sit near Fiona."},
    {"guest_name": "Bob", "attending": "Yes", "dietary": "Carnivore", "seating": "Must sit next to David. Refuses to sit near Eve (vegan)."},
    {"guest_name": "Charlie", "attending": "Yes", "dietary": "Gluten-free", "seating": "Needs to sit next to Alice."}, # Intentional conflict with Alice
    {"guest_name": "David", "attending": "Yes", "dietary": "None", "seating": "Must sit next to Bob."},
    {"guest_name": "Eve", "attending": "Yes", "dietary": "Vegan", "seating": "Needs a window seat, refuses to sit next to any Carnivores like Bob."},
    {"guest_name": "Fiona", "attending": "Yes", "dietary": "Pescatarian", "seating": "Will only sit next to Alice."}
]

def run():
    max_iterations = 3
    iteration = 1
    previous_issues = "None. This is the first draft."
    
    while iteration <= max_iterations:
        print(f"\n=============================================")
        print(f"--- Starting Negotiation Loop {iteration}/{max_iterations} ---")
        print(f"=============================================\n")
        
        inputs = {
            'current_year': str(datetime.now().year),
            'previous_issues': previous_issues
        }
        
        try:
            result = EventPlanner(guests_data=GUESTS_DATA).crew().kickoff(inputs=inputs)
            plan_result = result.pydantic
            
            if not plan_result:
                print("\nError: No pydantic output returned from Crew. Exiting.")
                break
                
            if plan_result.all_resolved:
                print("\n*** Success! All guests are perfectly happy! ***\n")
                with open("event_plan.md", "w") as f:
                    f.write(plan_result.final_plan_markdown)
                return
            else:
                print(f"\n--- Loop {iteration} Failed to satisfy everyone. ---")
                print("Remaining complaints:")
                for complaint in plan_result.remaining_complaints:
                    print("-", complaint)
                
                previous_issues = " ".join(plan_result.remaining_complaints)
                iteration += 1
                
        except Exception as e:
            raise Exception(f"An error occurred while running the crew in loop {iteration}: {e}")
            
    if iteration > max_iterations:
        print(f"\n*** Reached maximum {max_iterations} iterations. Forcing plan finalization despite complaints. ***")
        if 'plan_result' in locals() and plan_result:
            with open("event_plan.md", "w") as f:
                f.write(plan_result.final_plan_markdown)

def train():
    inputs = {'current_year': str(datetime.now().year), 'previous_issues': 'None'}
    try:
        EventPlanner(guests_data=GUESTS_DATA).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        EventPlanner(guests_data=GUESTS_DATA).crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {'current_year': str(datetime.now().year), 'previous_issues': 'None'}
    try:
        EventPlanner(guests_data=GUESTS_DATA).crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
