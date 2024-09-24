from crewai import Crew, Agent, Task
import os
import json
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from phoenix.otel import register
from openinference.instrumentation.openai import OpenAIInstrumentor
from openinference.instrumentation.crewai import CrewAIInstrumentor
from litellm import litellm
class Note(BaseModel):
    title: str
    content: str
    # status: NoteStatus


load_dotenv()
tracer_provider = register(
project_name="obsidian-boy",
endpoint="http://localhost:6006/v1/traces"
)
OpenAIInstrumentor().instrument(tracer_provider=tracer_provider)
CrewAIInstrumentor().instrument(tracer_provider=tracer_provider)
llm="openrouter/qwen/qwen-2.5-72b-instruct"
print(litellm.get_supported_openai_params(llm))

# os.environ["OPENAI_API_KEY"] = os.getenv("OPENROUTER_API_KEY")
# os.environ["OPENAI_API_BASE"] = '"https://openrouter.ai/api/v1'
# os.environ["OPENAI_API_KEY"] = os.getenv("DEEPSEEK_API_KEY")
# os.environ["OPENAI_API_BASE"] = 'https://api.deepseek.com/v1'
# llm=ChatOpenAI(model="gpt-4o", temperature=0.7)
# DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
# llm = ChatOpenAI(
#     model="deepseek-chat", 
#     api_key=DEEPSEEK_API_KEY, 
#     base_url="https://api.deepseek.com/beta",
#     temperature=0.0
# )

# research_agent = Agent(
#     role='Research agent',
#     goal='Research the the important resources for a given topic',
#     backstory="I am a researcher with a great skill to find the most relevant resources. I stick to the objectives. I don't make something up",
#     verbose=True,
#     llm=llm,
#     allow_delegation=False,
#     tools=[FileReadTool(), SerperDevTool()]
# )
writer_agent = Agent(
    role='Note writer',
    goal='Write personal notes using a specified template.',
    backstory='I am a note writer with a great skill to write personal notes.',
    verbose=True,
    llm="openrouter/qwen/qwen-2.5-72b-instruct",
    allow_delegation=False,
    tools=[]
)

note_json={'title':'a title for the note', 'content': 'the note content'}
note_task = Task(
    description=f"""
    Create a note about the resource Pydantic using the note template.
    The note shall contain a general section explaining the resource and its concepts and a multiple themed section with important links to websites.
    Adhere to this schema: {Note.model_json_schema()}
    """,
    agent=writer_agent,
    expected_output="a note that is the filled template",
    output_pydantic=Note,
    output_file="note.json"
)    
crew = Crew(
    agents=[writer_agent],
    tasks=[note_task],
    verbose=True
)

crew_output = crew.kickoff()
print(f"Crew: {crew_output}")
print(f"Pydantic: {note_task.output.pydantic}")

# Accessing the crew output
# print(f"Raw Output: {crew_output.raw}")
# if crew_output.json_dict:
#     print(f"JSON Output: {json.dumps(crew_output.json_dict, indent=2)}")
# if crew_output.pydantic:
#     print(f"Pydantic Output: {crew_output.pydantic}")
# print(f"Tasks Output: {crew_output.tasks_output}")
# print(f"Token Usage: {crew_output.token_usage}")