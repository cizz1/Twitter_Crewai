from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from tools.custom_tool import like_tool,reply_tool,retweet_tool,feedscan_tool
# Uncomment the following line to use an example of a custom tool
# from twittercrew.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool


# Load environment variables from a .env file


# Retrieve the API key from environment variables


# Your code to use GROQ_API_KEY and ChatGroq here
from dotenv import load_dotenv
load_dotenv()

@CrewBase
class TwittercrewCrew:
	"""Twittercrew crew"""

	llm= LLM(model="groq/mixtral-8x7b-32768")


	@agent
	def feed_scanner_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['feed_scanner_agent'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			tools=[feedscan_tool],
			llm=self.llm
		)

	@agent
	def news_scanner_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['news_scanner_agent'],
			verbose=True,
			tools=[SerperDevTool()],
			llm=self.llm
		)
	
	@agent
	def interaction_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['interaction_agent'],
			verbose=True,
			tools=[like_tool,reply_tool,retweet_tool],
			llm=self.llm
		)
	
	@agent
	def context_relevancy_check_agent(self) -> Agent:
		return Agent(
			config=self.agents_config['context_relevancy_check_agent'],
			verbose=True,
			llm=self.llm
		)
	
	@task
	def scan_tweets_task(self) -> Task:
		return Task(
			config=self.tasks_config['scan_tweets_task'],
			output_file='report.md'
		)
	
	@task
	def scan_news_task(self) -> Task:
		return Task(
			config=self.tasks_config['scan_news_task'],
		)

	@task
	def interact_with_tweets_task(self) -> Task:
		return Task(
			config=self.tasks_config['interact_with_tweets_task'],
			output_file='report.md'
		)
	
	@task
	def check_relevancy_task(self) -> Task:
		return Task(
			config=self.tasks_config['check_relevancy_task'],
		)
	

	@crew
	def crew(self) -> Crew:
		"""Creates the Twittercrew crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)