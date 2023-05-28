from typing import List, Tuple

from openai import ChatCompletion
from pydantic import BaseModel

from ..schemas import AiChatMessage
from ..utils import logger
from .prompts import PROMPTS
from .vecstores import Vecstores

map_int_topic = {"0": "banco_info", "1": "transaccion", "2": "other"}


class Agent:
    def __init__(self):
        self.vecstore = Vecstores()

    def __call__(self, user_msg: str, history: List[str]) -> Tuple[AiChatMessage]:
        """
        Generate AI response for the given user message and history.

        :param user_msg: User's message
        :param history: Chat history
        :return: Tuple of User's message, AI message and AI's message as a string.
        """
        logger.info(user_msg)
        topic = self.get_topic(user_msg)
        logger.info(topic)

        if topic == "transaccion":
            ai_msg = "Lo siento, el servicio de transacciones aun no está disponible"
        else:
            context, metadatas = self.get_context(user_msg, topic)
            history = self.format_history(history)

            prompt = PROMPTS["GET_INFO"].format(
                query=user_msg, context=context, history=history
            )
            logger.info(prompt)
            # print(f"\PROMPT: {prompt} \n")

            ai_msg = self.chat_completion(prompt)

        return (
            AiChatMessage(**{"role": "user", "content": user_msg}),
            AiChatMessage(**{"role": "assistant", "content": ai_msg}),
            ai_msg,
        )

    def get_topic(self, query: str) -> str:
        """
        Extract topic from the user query.

        :param query: User's query
        :return: Topic string
        """

        prompt = PROMPTS["GET_TOPIC"].format(query=query)

        topic = self.chat_completion(prompt, max_tokens=20)

        # Edge case: The model returns unnecessary text with the integer.
        if len(topic) > 1:
            for i in range(len(map_int_topic)):
                if str(i) in topic:
                    topic = i

        topic = map_int_topic[topic]
        return topic

    def get_context(self, q: str, topic: str) -> Tuple:
        """
        Get context for a given query and topic.

        :param q: User's query
        :param topic: Topic string
        :return: Context and metadata
        """
        logger.info(f"Context topic: {topic}")

        if topic in "other":
            return "No context provided.", []

        documents = self.vecstore.similarity_search(q, topic)

        metadatas = [doc.metadata["source"] for doc in documents]
        raw_context = "\n\n".join([doc.page_content for doc in documents])

        context = PROMPTS["CONTEXT"].format(raw_context=raw_context)

        return (context, metadatas)

    def format_history(self, history: List[str]) -> str:
        """
        Format history list as a string.

        :param history: Chat history
        :return: Formatted history string
        """
        return "\n".join([m for m in history])


    def chat_completion(self, prompt: str, max_tokens: int = None) -> str:
        """
        Get AI response for a given prompt.

        :param prompt: Prompt for the AI
        :param max_tokens: Maximum tokens for the response
        :return: AI's response
        """
        response = ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens)
        return response['choices'][0]['message']['content']
