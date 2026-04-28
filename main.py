import os
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import AgentCapabilities, AgentCard, AgentSkill

from lead_manager.agent_executor import LeadManagerAgentExecutor

# Define the Agent Card
agent_card = AgentCard(
    name="Lead Manager Agent",
    description="Simple Lead Manager Agent",
    url="http://localhost", # Render will handle the domain routing
    version="1.0.0",
    capabilities=AgentCapabilities(
        streaming=False,
        pushNotifications=False,
    ),
    skills=[
        AgentSkill(
            id="process_search",
            name="Process Search Query",
            description="Processes search queries",
            examples=["Search for leads"],
            tags=["search"],
        )
    ],
    defaultInputModes=["data"],
    defaultOutputModes=["data"],
)

# Instantiate handler and executor
agent_executor = LeadManagerAgentExecutor()
task_store = InMemoryTaskStore()
request_handler = DefaultRequestHandler(
    agent_executor=agent_executor, task_store=task_store
)

# Build the ASGI app so platforms like Render can hook into it
app_builder = A2AStarletteApplication(
    agent_card=agent_card,
    http_handler=request_handler,
)

app = app_builder.build()
