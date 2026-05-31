from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew
from pydantic import BaseModel, Field
from typing import List

class EventPlanResult(BaseModel):
    all_resolved: bool = Field(description="True if there were zero complaints from guests in their reviews, meaning everyone perfectly approved.")
    remaining_complaints: List[str] = Field(description="List of objections raised by guests that could not be satisfied, if any.")
    final_plan_markdown: str = Field(description="The complete event plan markdown, including the menu and the seating chart.")
    negotiation_summary: str = Field(description="A 2-3 paragraph summary of the event planning negotiation drama, guest complaints, and host compromises from this specific iteration.")

@CrewBase
class EventPlanner():
    """EventPlanner crew with dynamically generated guest agents and true negotiation"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, guests_data=None):
        self.guests_data = guests_data or []

    @agent
    def catering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['catering_agent'],
            verbose=True
        )

    @agent
    def host_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['host_agent'],
            verbose=True
        )

    @agent
    def summarizer_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['summarizer_agent'],
            verbose=True
        )

    @crew
    def crew(self) -> Crew:
        guest_agents = {}
        preference_tasks = []
        review_tasks = []

        # 1. Initialize Persona Agents & Provide preferences
        for g_data in self.guests_data:
            guest_name = g_data["guest_name"]
            g_agent = Agent(
                role=self.agents_config['guest_agent']['role'].format(**g_data),
                goal=self.agents_config['guest_agent']['goal'].format(**g_data),
                backstory=self.agents_config['guest_agent']['backstory'].format(**g_data),
                verbose=True
            )
            guest_agents[guest_name] = g_agent

            pref_task = Task(
                description=self.tasks_config['guest_preference_task']['description'].format(**g_data),
                expected_output=self.tasks_config['guest_preference_task']['expected_output'].format(**g_data),
                agent=g_agent
            )
            preference_tasks.append(pref_task)

        # 2. Caterer formulates menu based on preferences
        menu_task = Task(
            config=self.tasks_config['menu_formulation_task'],
            agent=self.catering_agent(),
            context=preference_tasks
        )

        # 3. Host drafts initial seating chart
        draft_seating_task = Task(
            config=self.tasks_config['host_draft_seating_task'],
            agent=self.host_agent(),
            context=preference_tasks
        )

        # 4. Guests review the drafted chart and approve/object
        for g_data in self.guests_data:
            guest_name = g_data["guest_name"]
            rev_task = Task(
                description=self.tasks_config['guest_review_task']['description'].format(**g_data),
                expected_output=self.tasks_config['guest_review_task']['expected_output'].format(**g_data),
                agent=guest_agents[guest_name],
                context=[draft_seating_task]
            )
            review_tasks.append(rev_task)

        # 5. Host finalizes everything resolving conflicts (outputs raw text markdown)
        finalize_task = Task(
            config=self.tasks_config['host_finalize_task'],
            agent=self.host_agent(),
            context=[menu_task, draft_seating_task] + review_tasks
        )

        # 6. Summarizer produces final JSON + The Negotiation Summary
        summary_task = Task(
            config=self.tasks_config['summarize_negotiation_task'],
            agent=self.summarizer_agent(),
            context=preference_tasks + [draft_seating_task] + review_tasks + [finalize_task],
            output_pydantic=EventPlanResult
        )

        all_agents = list(guest_agents.values()) + [self.catering_agent(), self.host_agent(), self.summarizer_agent()]
        all_tasks = preference_tasks + [menu_task, draft_seating_task] + review_tasks + [finalize_task, summary_task]

        return Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True,
            max_rpm=10,
        )
