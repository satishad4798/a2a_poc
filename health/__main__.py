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

from agent_executor import HealthAgentExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    skill = AgentSkill(
        id='health_advisor',
        name='Health Advisor',
        description='Provides general health information',
        tags=['health', 'wellness', 'medical', 'fitness'],
        examples=['What are the benefits of vitamin C?', 'How much water should I drink?'],
    )

    agent_card = AgentCard(
        name='Health Agent',
        description='An agent that provides health info using Gemini.',
        url='http://localhost:8003/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=HealthAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Health Agent on port 8003...")
    uvicorn.run(server.build(), host='0.0.0.0', port=8003)
