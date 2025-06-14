from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool


@CrewBase
class Voiceboard:
    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    def __init__(self) -> None:
        # Initialize tools that will be used by agents
        self.search_tool = SerperDevTool()
        self.scrape_tool = ScrapeWebsiteTool()
        self.website_search = WebsiteSearchTool()

    @agent
    def persona_identifier(self) -> Agent:
        return Agent(
            config=self.agents_config['persona_identifier'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.scrape_tool]
        )

    @agent
    def voice_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['voice_researcher'], # type: ignore[index]
            verbose=True,
            tools=[self.search_tool, self.scrape_tool, self.website_search]
        )

    @agent
    def persona_conversation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['persona_conversation_agent'], # type: ignore[index]
            verbose=True
        )

    @task
    def persona_identification_task(self) -> Task:
        return Task(
            config=self.tasks_config['persona_identification_task'], # type: ignore[index]
        )

    @task
    def voice_research_task(self) -> Task:
        return Task(
            config=self.tasks_config['voice_research_task'], # type: ignore[index]
        )

    @task
    def persona_conversation_task(self) -> Task:
        return Task(
            config=self.tasks_config['persona_conversation_task'], # type: ignore[index]
        )

    @task
    def persona_followup_task(self) -> Task:
        return Task(
            config=self.tasks_config['persona_followup_task'], # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Voiceboard crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )

    def run_initial_setup(self, startup_idea: str):
        """
        Run the initial persona identification and voice research phases.
        Returns the researched personas for user selection.
        """
        # Create a temporary crew with just the first two tasks
        setup_crew = Crew(
            agents=[self.persona_identifier(), self.voice_researcher()],
            tasks=[self.persona_identification_task(), self.voice_research_task()],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute the setup with the startup idea
        result = setup_crew.kickoff(inputs={'startup_idea': startup_idea})
        return result

    def run_conversation(self, selected_persona_name: str, user_message: str, startup_idea: str = ""):
        """
        Run a conversation with the selected persona.
        """
        # Create conversation crew with the conversation agent
        conversation_crew = Crew(
            agents=[self.persona_conversation_agent()],
            tasks=[self.persona_conversation_task()],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute conversation with persona and message
        result = conversation_crew.kickoff(inputs={
            'selected_persona_name': selected_persona_name,
            'user_message': user_message,
            'startup_idea': startup_idea
        })
        return result

    def run_followup(self, selected_persona_name: str, user_response: str, conversation_history: str):
        """
        Run a follow-up conversation with the selected persona.
        """
        # Create followup crew
        followup_crew = Crew(
            agents=[self.persona_conversation_agent()],
            tasks=[self.persona_followup_task()],
            process=Process.sequential,
            verbose=True
        )
        
        # Execute followup with persona response
        result = followup_crew.kickoff(inputs={
            'selected_persona_name': selected_persona_name,
            'user_response': user_response,
            'conversation_history': conversation_history
        })
        return result
    
    def get_persona_list_from_setup(self, setup_result):
        """
        Helper method to extract persona names from setup result for user selection.
        In a real implementation, you'd parse the JSON output from the first task.
        """
        # This is a simplified version - you'd parse the actual JSON output
        # from the persona_identification_task
        return [
            "Kevin O'Leary",
            "Barbara Corcoran", 
            "Mark Cuban",
            "Sara Blakely",
            "Reid Hoffman"
        ]