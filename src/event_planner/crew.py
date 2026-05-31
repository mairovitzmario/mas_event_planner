from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class EventPlanner():
    """EventPlanner crew"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def guest_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['guest_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def catering_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['catering_agent'], # type: ignore[index]
            verbose=True
        )

    @agent
    def host_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['host_agent'], # type: ignore[index]
            verbose=True
        )

    @task
    def rsvp_and_preferences_task(self) -> Task:
        return Task(
            config=self.tasks_config['rsvp_and_preferences_task'], # type: ignore[index]
        )

    @task
    def menu_formulation_task(self) -> Task:
        return Task(
            config=self.tasks_config['menu_formulation_task'], # type: ignore[index]
        )

    @task
    def seating_and_final_plan_task(self) -> Task:
        return Task(
            config=self.tasks_config['seating_and_final_plan_task'], # type: ignore[index]
            output_file='event_plan.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the EventPlanner crew"""
        return Crew(
            agents=self.agents,  
            tasks=self.tasks,    
            process=Process.sequential,
            verbose=True,
        )
