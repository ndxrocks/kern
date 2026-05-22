"""
Learning Stores
===============
Storage backends for each learning type.

Each store implements the LearningStore protocol and handles:
- Recall: Retrieving relevant data
- Process: Extracting and saving learnings
- Context: Building agent context strings
- Tools: Providing agent tools

Available Stores:
- UserProfileStore: Long-term user profile fields
- UserMemoryStore: Long-term user memories (unstructured)
- SessionContextStore: Current session state
- LearnedKnowledgeStore: Reusable knowledge/insights
- EntityMemoryStore: Third-party entity facts
- DecisionLogStore: Agent decision logging (Phase 2)
"""

from kern.learn.stores.decision_log import DecisionLogStore
from kern.learn.stores.entity_memory import EntityMemoryStore
from kern.learn.stores.learned_knowledge import LearnedKnowledgeStore
from kern.learn.stores.protocol import LearningStore
from kern.learn.stores.session_context import SessionContextStore
from kern.learn.stores.user_memory import MemoriesStore, UserMemoryStore
from kern.learn.stores.user_profile import UserProfileStore

__all__ = [
    "LearningStore",
    "UserProfileStore",
    "UserMemoryStore",
    "MemoriesStore",  # Backwards compatibility alias
    "SessionContextStore",
    "LearnedKnowledgeStore",
    "EntityMemoryStore",
    "DecisionLogStore",
]
