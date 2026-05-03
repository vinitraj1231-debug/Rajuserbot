"""
AI Response Engine — OpenRouter API Integration
"""

import os
import httpx
import logging
from personality import build_system_prompt

log = logging.getLogger("ZynoBot.AI")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL     = "https://openrouter.ai/api/v1/chat/completions"
MODEL              = os.getenv("AI_MODEL", "openai/gpt-4o-mini")   # fast + cheap


async def get_ai_response(
    user_message: str,
    history: list,
    context: str = "cute",
    is_group: bool = False,
) -> str:
    """
    Call OpenRouter and get AI reply.

    Args:
        user_message: Current user message
        history:      List of {"role": ..., "content": ...} dicts
        context:      Detected mood/mode (cute, sad, flirty, angry, funny, romantic)
        is_group:     Whether the message is from a group chat

    Returns:
        AI response string
    """
    system_prompt = build_system_prompt(context, is_group)

    messages = [{"role": "system", "content": system_prompt}]
    messages += history
    messages.append({"role": "user", "content": user_message})

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://zynochat.in",
        "X-Title": "Zyno Userbot",
    }

    payload = {
        "model": MODEL,
        "messages": messages,
        "max_tokens": 120,
        "temperature": 0.85,
        "top_p": 0.95,
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(OPENROUTER_URL, json=payload, headers=headers)
            response.raise_for_status()
            data    = response.json()
            reply   = data["choices"][0]["message"]["content"].strip()

            # Safety: truncate overly long replies
            if len(reply) > 300:
                reply = reply[:280].rsplit(" ", 1)[0] + "..."

            return reply

    except httpx.TimeoutException:
        log.error("OpenRouter timeout")
        return "Hmm... thoda slow ho gayi hu 😅 ek second?"

    except httpx.HTTPStatusError as e:
        log.error(f"HTTP error: {e.response.status_code}")
        return "Oops kuch ho gaya 🙈 phir try karo na"

    except Exception as e:
        log.error(f"Unexpected error: {e}")
        return "Arey kuch gadbad ho gayi 😕"
