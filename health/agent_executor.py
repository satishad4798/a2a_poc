import logging
import os

import google.generativeai as genai
from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    InternalError,
    TaskState,
    Part,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HealthAgentExecutor(AgentExecutor):
    """Health Agent Executor using Gemini."""

    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            logger.warning("GOOGLE_API_KEY not found in environment variables.")
        else:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel(
                model_name="gemini-1.5-flash",
                system_instruction="You are a general health assistant. Provide helpful information on health topics. Always include a disclaimer that you are an AI and not a doctor. Do not provide medical diagnoses."
            )

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        if not self.api_key:
             raise ServerError(error=InternalError(message="Server misconfigured: Missing GOOGLE_API_KEY"))

        query = context.get_user_input()
        logger.info(f"Received query: {query}")

        task = context.current_task
        if not task:
            task = new_task(context.message) # type: ignore
            await event_queue.enqueue_event(task)
        
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        try:
             # Indicate working state
            await updater.update_status(
                TaskState.working,
                new_agent_text_message("Consulting health database... (Disclaimer: I am an AI)", task.context_id, task.id)
            )

            response = await self.model.generate_content_async(query)
            response_text = response.text

            # Send result
            await updater.add_artifact(
                [Part(root=TextPart(text=response_text))],
                name="health_info",
            )
            await updater.complete()

        except Exception as e:
            logger.error(f"Error generating content: {e}")
            raise ServerError(error=InternalError()) from e

    async def cancel(
        self, context: RequestContext, event_queue: EventQueue
    ) -> None:
        raise ServerError(error=UnsupportedOperationError())
