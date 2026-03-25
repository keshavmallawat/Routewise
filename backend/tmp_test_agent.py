from langchain_openai import ChatOpenAI
from crewai import Agent
import traceback

llm = ChatOpenAI(base_url='https://openrouter.ai/api/v1', api_key='dummy', model='openai/gpt-4o-mini')

try:
    agent = Agent(
        role='Test',
        goal='Test',
        backstory='Test',
        tools=[lambda x: x],
        verbose=True,
        llm=llm,
    )
    print('Agent created', agent)
except Exception:
    traceback.print_exc()
