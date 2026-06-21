import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.system_engine import LivingAISystem

ai = LivingAISystem()
res = ai.process('hello')
print('memory_count', len(ai.semantic_memory.get_memories()))
print('related_memories', ai.semantic_memory.search_memory('hello'))
print('distributed_stats', ai.distributed_memory.get_memory_stats())
print('response', res)
