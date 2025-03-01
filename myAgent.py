from agno.agent import Agent
from agno.tools import Toolkit
from agno.models.groq import Groq as gg
import gradio as gr
#from dotenv import load_dotenv
import toolkitHandler as tk

stored_api_key = ""

agent = Agent(
    model = gg(id="llama-3.3-70b-versatile"),
    tools=[tk.DataRetriver()],
    description="""
                you are an AI agent which can do Curd operations.
                call only one function at a time.
                show function call with the parameters.
                display the records of table if returned.
                don't hallosinate data.
                """,
    instructions=['if you get errors show them in redable form.'
                  'don not hallosinate data.'],
    show_tool_calls=True, markdown=True,
    #response_model=Respose,
    
)
#text = "add sunny age 43 and email 444435@gmail.com to the table test"
#agent.print_response(text)