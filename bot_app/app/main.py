import os

import aioredis
import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from pydantic import ValidationError
load_dotenv()

from . import schemas
from .ai.agent import Agent
from .audio import get_voice_text
from .text import send_message
from .utils import logger

REDIS_URL = os.getenv("REDIS_URL")
MAP_CHAT_PROFILE = {2067529574: "young", -961331167: "senior"}

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    app.state.redis = await aioredis.from_url(REDIS_URL)
    await app.state.redis.flushdb()
    app.state.agent = Agent()


@app.post("/")
async def telegram_webhook(request: Request):
    try:
        data = await request.json()

        msg = await validate_data(data)
        ai_msg = await handle_chat(msg)
        return {"ai": ai_msg}

    except ValidationError as e:
        logger.error(e.errors())
        return {"status": "error"}

@app.get("/tokens")
def get_spent_tokens():
    return app.state.agent.total_tokens


async def validate_data(data) -> schemas.Message:
    try:
        msg = schemas.Message(**data["message"])
        return msg
    except ValidationError as e:
        logger.error(e.errors())
        raise HTTPException(status_code=400, detail="Invalid data.")


async def handle_chat(msg: schemas.Message) -> schemas.AiChatMessage:
    """Retrieve chat history, generate reply, update history and reply to user."""

    chat_id = msg.chat.id
    user_msg_raw = await get_user_message(msg)

    chat_history = await app.state.redis.lrange(chat_id, 0, -1)
    chat_history = [x.decode("utf-8") for x in chat_history]

    profile = MAP_CHAT_PROFILE.get(chat_id, "young")
    user_msg, ai_msg, ai_msg_telegram = app.state.agent(profile, user_msg_raw, chat_history)

    await app.state.redis.rpush(chat_id, str(user_msg))
    await app.state.redis.rpush(chat_id, str(ai_msg))
    await app.state.redis.expire(chat_id, 900)

    await send_message(chat_id, ai_msg_telegram)

    return ai_msg


async def get_user_message(msg: schemas.Message) -> str:
    """Extract the raw text message from a Message object"""

    if msg.voice != None:
        logger.info("Message type is voice, handling it")
        user_msg = await get_voice_text(msg)

    else:
        logger.info("Message type is text, handling it")
        user_msg = msg.text

    return user_msg
