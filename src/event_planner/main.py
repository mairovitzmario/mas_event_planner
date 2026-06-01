#!/usr/bin/env python
import sys
import os
import json
import warnings

from event_planner.crew import EventPlanner

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

with open("input/data.json", "r") as f:
    DATA = json.load(f)

def run():
    max_iterations = 3
    iteration = 1
    previous_issues = "None. This is the first draft."
    
    os.makedirs("output", exist_ok=True)

    # Clear initial summary document block
    with open("output/negotiation_summary.md", "w") as f:
        f.write("# Total Event Planning Negotiation Summary\n\n")

    while iteration <= max_iterations:
        print(f"\n=============================================")
        print(f"--- Starting Negotiation Loop {iteration}/{max_iterations} ---")
        print(f"=============================================\n")
        
        inputs = {
            'previous_issues': previous_issues,
            'budget': DATA['budget']  
        }
        
        try:
            result = EventPlanner(guests_data=DATA['guests']).crew().kickoff(inputs=inputs)
            plan_result = result.pydantic
            
            if not plan_result:
                print("\nError: No pydantic output returned from Crew. Exiting.")
                break

            # Write individual loop negotiation summary
            if plan_result.negotiation_summary:
                with open("output/negotiation_summary.md", "a") as f:
                    f.write(f"## Loop {iteration} Negotiation Drama\n")
                    f.write(plan_result.negotiation_summary + "\n\n")
                
            if plan_result.all_resolved:
                print("\n*** Success! All guests are perfectly happy! ***\n")
                with open("output/event_plan.md", "w") as f:
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
            with open("output/event_plan.md", "w") as f:
                f.write(plan_result.final_plan_markdown)

def train():
    inputs = {'previous_issues': 'None', 'budget': DATA['budget']}
    try:
        EventPlanner(guests_data=DATA['guests']).crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    try:
        EventPlanner(guests_data=DATA['guests']).crew().replay(task_id=sys.argv[1])
    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    inputs = {'previous_issues': 'None', 'budget': DATA['budget']}
    try:
        EventPlanner(guests_data=DATA['guests']).crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
