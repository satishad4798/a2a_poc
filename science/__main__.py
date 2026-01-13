import logging
import sys

import uvicorn
from a2a.server.apps import A2AStarletteApplication
from a2a.server.request_handlers import DefaultRequestHandler
from a2a.server.tasks import InMemoryTaskStore
from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)

from agent_executor import ScienceAgentExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    skill = AgentSkill(
        id='science_qa',
        name='Science Q&A',
        description='Answers science related questions',
        tags=['science', 'chemistry', 'physics', 'biology'],
        examples=['Why is the sky blue?', 'Explain quantum entanglement'],
    )

    agent_card = AgentCard(
        name='Science Agent',
        description='An agent that answers science questions using Gemini.',
        url='http://localhost:8001/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=False), # Simpler for now
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=ScienceAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Science Agent on port 8001...")
    uvicorn.run(server.build(), host='0.0.0.0', port=8001)
