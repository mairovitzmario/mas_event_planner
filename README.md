# MAS Event Planner

## Problem Domain

This project automates event planning by managing overlapping constraints like RSVPs, dietary restrictions, and seating arrangements. It uses a multiagent system to negotiate these details and dynamically generate an optimal, conflict-free event plan.

## Architecture

The system is built using the **CrewAI** framework, leveraging a robust network of autonomous agents to handle specific aspects of the event planning process. Configuration for agents and tasks is defined declaratively using YAML inside `src/event_planner/config/`.

### High-Level Workflow

The system operates via a collaborative and iterative negotiation process:

1. **Requirement Gathering**: Guests declare their attendance, dietary restrictions, and seating preferences.
2. **Drafting**: The Catering agent designs a menu accommodating all dietary needs, while the Host agent drafts an initial seating chart trying to satisfy everyone's preferences.
3. **Negotiation & Review**: Guests review the drafted arrangements, either approving them or raising strong objections if their constraints are violated.
4. **Finalization**: The Host agent adjusts the plan based on the feedback to resolve conflicts, generating the final Event Plan.
5. **Reporting**: The Summarizer agent documents the entire interaction, logs complaints and compromises, and outputs a comprehensive negotiation summary.

### Agents

- **Guest Agents**: Each Guest Agent represents an individual attendee. It strongly advocates for its assigned attendance status, dietary needs, and seating preferences. If not attending, it politely declines; if attending, it rigidly defends its constraints.
- **Caterer Agent** (Head Caterer): Reviews all attendees' dietary restrictions and crafts a single, inclusive menu that safely feeds everyone.
- **Host Agent** (Event Host & Coordinator): The meticulous coordinator. It creates draft seating charts, processes guest complaints or approvals, and finalizes the perfect seating chart and overall event plan.
- **Summarizer Agent** (Event Reporter & Summarizer): An objective observer that compiles meeting minutes. It logs the negotiation drama, compromises, and any remaining unresolved complaints into a structured format.

### Tasks

- **Guest Preference Task**: Guests state their requirements (attendance, diet, seating) to the Host and Caterer.
- **Menu Formulation Task** (Catering Agent): Reads all guest preferences and proposes a detailed menu catering explicitly to the attendees' restrictions.
- **Host Draft Seating Task** (Host Agent): Creates an initial draft seating chart striving to perfectly accommodate attendee preferences, while explicitly addressing any complaints from previous iterations.
- **Guest Review Task**: Guests review the draft seating chart. They either approve it enthusiastically or strongly object, stating exactly why it fails them.
- **Host Finalize Task** (Host Agent): Incorporates the menu and all guest feedback to adjust the seating chart, resolving lingering complaints and generating the absolute final event plan as markdown.
- **Summarize Negotiation Task** (Summarizer Agent): Reads all initial preferences, draft plans, reactions, and the final output to produce a brief, lively summary of the negotiation cycle and structurally populates the final data format.

## Setup Instructions

### 1. Configuration (Required for all methods)

Create an `.env` file in the project's root folder and populate it with your specific API key. Follow the `.env.example` model:

```env
MODEL=gemini/gemini-3.1-flash-lite
GEMINI_API_KEY=your-api-key
```

### 2. Running with Docker Compose (Recommended)

If you have Docker installed, this is the easiest way to run the entire system:

```bash
docker compose up --build
```

_(This will build the image and start the container, executing the multiagent workflow automatically.)_

Once completed, the planned outputs such as `event_plan.md` and `negotiation_summary.md` will be available in the `output/` directory.

### 3. Running Locally (Alternative)

This project uses `Python` with `uv` for dependency management. If you prefer running without Docker:

**1. Install Prerequisites**
Ensure you have `uv` installed. If you don't have it installed:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Create and Activate the Virtual Environment**

```bash
uv venv .venv
source .venv/bin/activate
```

**3. Install Dependencies**

```bash
uv sync
```

_(You can also use the CrewAI CLI: `crewai install`)_

**4. Run the Application**

```bash
# Make sure you are inside the venv
source .venv/bin/activate
crewai run

# If you wish to save logs inside a file you can pipe the output via the tee command like so
crewai run 2>&1 | tee output/conversation.log
```

Once completed, the planned outputs such as `event_plan.md` and `negotiation_summary.md` will be available in the `output/` directory.
