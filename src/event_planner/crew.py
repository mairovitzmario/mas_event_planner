from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew

@CrewBase
class EventPlanner():
    """EventPlanner crew with dynamically generated guest agents"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self, guests=None):
        self.guests = guests or []

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

    @crew
    def crew(self) -> Crew:
        """Creates the EventPlanner crew with an agent per guest"""
        guest_agents = []
        guest_tasks = []

        for guest_name in self.guests:
            g_agent = Agent(
                role=self.agents_config['guest_agent']['role'].format(guest_name=guest_name),
                goal=self.agents_config['guest_agent']['goal'].format(guest_name=guest_name),
                backstory=self.agents_config['guest_agent']['backstory'].format(guest_name=guest_name),
                verbose=True
            )
            guest_agents.append(g_agent)

            g_task = Task(
                description=self.tasks_config['guest_task']['description'].format(guest_name=guest_name, guest_list="{guest_list}"),
                expected_output=self.tasks_config['guest_task']['expected_output'].format(guest_name=guest_name),
                agent=g_agent
            )
            guest_tasks.append(g_task)

        menu_task = Task(
            config=self.tasks_config['menu_formulation_task'],
            agent=self.catering_agent(),
            context=guest_tasks
        )

        seating_task = Task(
            config=self.tasks_config['seating_and_final_plan_task'],
            agent=self.host_agent(),
            context=guest_tasks + [menu_task],
            output_file='event_plan.md'
        )

        all_agents = guest_agents + [self.catering_agent(), self.host_agent()]
        all_tasks = guest_tasks + [menu_task, seating_task]

        return Crew(
            agents=all_agents,
            tasks=all_tasks,
            process=Process.sequential,
            verbose=True,
        )
