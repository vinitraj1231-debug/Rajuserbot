"""
Memory Manager — Per-user conversation history (in-memory)
"""

from collections import defaultdict, deque
from typing import List, Dict


class MemoryManager:
    """
    Stores last N messages per user_id.
    Format per entry: {"role": "user"/"assistant", "content": "..."}
    """

    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        # user_id -> deque of message dicts
        self._store: Dict[int, deque] = defaultdict(lambda: deque(maxlen=max_history))

    def add(self, user_id: int, role: str, content: str):
        """Add a message to user history."""
        self._store[user_id].append({"role": role, "content": content})

    def get(self, user_id: int) -> List[dict]:
        """Return full history list for a user."""
        return list(self._store[user_id])

    def clear(self, user_id: int):
        """Clear history for a specific user."""
        self._store[user_id].clear()

    def clear_all(self):
        """Nuke all histories."""
        self._store.clear()

    def stats(self) -> dict:
        """Return basic stats."""
        return {
            "total_users": len(self._store),
            "total_messages": sum(len(v) for v in self._store.values()),
        }
