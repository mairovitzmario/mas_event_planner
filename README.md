# Multiagent System (MAS) Event Planner

## Problem Domain

This project automates event planning by managing overlapping constraints like RSVPs, dietary restrictions, and seating arrangements. It uses a multiagent system to negotiate these details and dynamically generate an optimal, conflict-free event plan.

## Architecture

The system is built using the **CrewAI** framework, leveraging a robust network of autonomous agents to handle specific aspects of the event planning process.

- **Agents**: Each agent is configured with a specific role, goal, and backstory (e.g., handling seating, resolving dietary restrictions, or tracking RSVPs).
- **Tasks**: The agents are assigned specific tasks to gather inputs, negotiate, and formulate plans.
- **Workflow**: The system uses a Crew to orchestrate task execution. Agents collaborate and negotiate internally to produce the final artifacts without requiring continuous manual intervention.
- Configuration for agents and tasks is defined declaratively using YAML inside `src/event_planner/config/`.

## Setup Instructions

This project uses `uv` for fast Python dependency management.

### 1. Prerequisites

Ensure you have `uv` installed. If you don't have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Create and Activate the Virtual Environment

Initialize the virtual environment at the project root and activate it:

```bash
uv venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the project dependencies using `uv`:

```bash
uv sync
```

_(You can also use the CrewAI CLI: `crewai install`)_

### 4. Configuration

Create an `.env` file in the project's root folder and populate it with your specific API key. Follow the `.env.example` model:

```env
MODEL=gemini/gemini-3.1-flash-lite
GEMINI_API_KEY=your-api-key
```

### 5. Running the Application

To execute the multiagent workflow and generate your event plan, use the CrewAI CLI:

```bash
# Make sure you are inside the venv
source .venv/bin/activate
crewai run

# If you wish to save logs inside a file you can pipe the output via the tee command like so
crewai run 2>&1 | tee output/conversation.log
```

Once completed, the planned outputs such as `event_plan.md` and `negotiation_summary.md` will be available in the `output/` directory.
