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

from agent_executor import MathAgentExecutor

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    skill = AgentSkill(
        id='math_solver',
        name='Math Solver',
        description='Solves math problems',
        tags=['math', 'calculator', 'algebra', 'calculus'],
        examples=['Solve 2x + 5 = 10', 'What is the derivative of x^2?'],
    )

    agent_card = AgentCard(
        name='Math Agent',
        description='An agent that solves math problems using Gemini.',
        url='http://localhost:8002/',
        version='1.0.0',
        default_input_modes=['text'],
        default_output_modes=['text'],
        capabilities=AgentCapabilities(streaming=False),
        skills=[skill],
    )

    request_handler = DefaultRequestHandler(
        agent_executor=MathAgentExecutor(),
        task_store=InMemoryTaskStore(),
    )

    server = A2AStarletteApplication(
        agent_card=agent_card,
        http_handler=request_handler,
    )

    print("Starting Math Agent on port 8002...")
    uvicorn.run(server.build(), host='0.0.0.0', port=8002)
