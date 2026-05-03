"""
Zyno AI Userbot - Advanced Telegram Userbot with AI Personality
Author: Built for Rr
"""

import os
import asyncio
import logging
from telethon import TelegramClient, events
from telethon.tl.types import User
from dotenv import load_dotenv
from ai import get_ai_response
from memory import MemoryManager

load_dotenv()

# ─── Config ──────────────────────────────────────────────────────────────────
API_ID   = int(os.getenv("TELEGRAM_API_ID"))
API_HASH = os.getenv("TELEGRAM_API_HASH")
SESSION  = os.getenv("SESSION_NAME", "zyno_session")

TRIGGER_WORDS = ["zyno", "zyna", "hey zyno", "zyno!"]
BOT_USERNAME  = os.getenv("BOT_USERNAME", "").lower()   # optional self-username

# ─── Logging ─────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
log = logging.getLogger("ZynoBot")

# ─── Client & Memory ─────────────────────────────────────────────────────────
client  = TelegramClient(SESSION, API_ID, API_HASH)
memory  = MemoryManager(max_history=10)


# ─── Helpers ─────────────────────────────────────────────────────────────────
def is_triggered_in_group(event) -> bool:
    """Returns True if bot should respond in a group chat."""
    text = event.raw_text.lower()

    # Mentioned via @username
    if BOT_USERNAME and f"@{BOT_USERNAME}" in text:
        return True

    # Trigger word used
    for word in TRIGGER_WORDS:
        if word in text:
            return True

    # Reply to a bot message
    if event.is_reply:
        return True

    return False


def clean_trigger(text: str) -> str:
    """Remove trigger words from start of message."""
    text_lower = text.lower()
    for word in TRIGGER_WORDS:
        if text_lower.startswith(word):
            text = text[len(word):].strip()
            break
    return text or text


# ─── Event Handlers ──────────────────────────────────────────────────────────

@client.on(events.NewMessage(incoming=True, func=lambda e: not e.is_group))
async def handle_private(event):
    """Handle all private/DM messages."""
    sender = await event.get_sender()
    if not isinstance(sender, User):
        return

    user_id  = sender.id
    user_msg = event.raw_text.strip()

    if not user_msg:
        return

    log.info(f"[DM] {sender.first_name} ({user_id}): {user_msg}")

    history  = memory.get(user_id)
    context  = detect_context(user_msg)

    # Show typing
    async with client.action(event.chat_id, "typing"):
        reply = await get_ai_response(user_msg, history, context, is_group=False)
        await asyncio.sleep(min(len(reply) * 0.03, 2.5))   # simulate typing delay

    memory.add(user_id, "user", user_msg)
    memory.add(user_id, "assistant", reply)

    await event.reply(reply)


@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_group))
async def handle_group(event):
    """Handle group messages — only when triggered."""
    if not is_triggered_in_group(event):
        return

    sender = await event.get_sender()
    if not isinstance(sender, User):
        return

    user_id  = sender.id
    user_msg = clean_trigger(event.raw_text.strip())

    if not user_msg:
        user_msg = "hello"

    log.info(f"[GROUP] {sender.first_name} ({user_id}): {user_msg}")

    history  = memory.get(user_id)
    context  = detect_context(user_msg)

    async with client.action(event.chat_id, "typing"):
        reply = await get_ai_response(user_msg, history, context, is_group=True)
        await asyncio.sleep(min(len(reply) * 0.025, 2.0))

    memory.add(user_id, "user", user_msg)
    memory.add(user_id, "assistant", reply)

    await event.reply(reply)


# ─── Context Detection ────────────────────────────────────────────────────────
EMOTION_MAP = {
    "sad": ["sad", "dukhi", "rona", "cry", "bura lag", "dil dukha", "depressed", "alone", "akela"],
    "flirty": ["love you", "pyaar", "cute", "beautiful", "handsome", "crush", "date", "dil de", "propose"],
    "angry": ["angry", "gussa", "bakwas", "chup", "annoying", "hate", "stupid", "idiot"],
    "funny": ["haha", "lol", "joke", "meme", "funny", "lmao", "hehe", "rofl"],
    "romantic": ["miss you", "yaad aa", "sochta hu", "dream", "raat ko", "neend nahi"],
}

def detect_context(text: str) -> str:
    text_lower = text.lower()
    for mood, keywords in EMOTION_MAP.items():
        for kw in keywords:
            if kw in text_lower:
                return mood
    return "cute"   # default mode


# ─── Startup ─────────────────────────────────────────────────────────────────
async def main():
    log.info("🚀 Zyno Userbot starting...")
    await client.start()
    me = await client.get_me()
    log.info(f"✅ Logged in as: {me.first_name} (@{me.username})")
    log.info("💬 Zyno is now active and listening...")
    await client.run_until_disconnected()


if __name__ == "__main__":
    asyncio.run(main())
