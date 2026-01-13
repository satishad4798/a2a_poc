import asyncio
import logging
import sys
from uuid import uuid4

import httpx
from a2a.client import A2ACardResolver, A2AClient
from a2a.types import (
    MessageSendParams,
    SendMessageRequest,
)

async def main(query: str) -> None:
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    base_url = 'http://localhost:8001'

    async with httpx.AsyncClient() as httpx_client:
        resolver = A2ACardResolver(
            httpx_client=httpx_client,
            base_url=base_url,
        )

        try:
            logger.info(f'Fetching agent card from: {base_url}')
            agent_card = await resolver.get_agent_card()
            logger.info(f'Agent found: {agent_card.name}')
        except Exception as e:
            logger.error(f'Failed to fetch agent card: {e}')
            return

        client = A2AClient(
            httpx_client=httpx_client, agent_card=agent_card
        )

        send_message_payload = {
            'message': {
                'role': 'user',
                'parts': [
                    {'kind': 'text', 'text': query}
                ],
                'messageId': uuid4().hex,
            },
        }
        
        request = SendMessageRequest(
            id=str(uuid4()), params=MessageSendParams(**send_message_payload)
        )

        logger.info(f"Sending query: {query}")
        try:
            response = await client.send_message(request)
            
            # Print the text response
            # Response handling might vary based on server implementation
            # usually response.result.message.parts[0].text if using standard A2A types
            print("\n=== AGENT RESPONSE ===")
            print(response.model_dump(mode='json', exclude_none=True))
            print("======================\n")

        except Exception as e:
            logger.error(f"Error sending message: {e}")

if __name__ == '__main__':
    query = sys.argv[1] if len(sys.argv) > 1 else "Why is the sky blue?"
    asyncio.run(main(query))
