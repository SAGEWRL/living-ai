import os
import sys
import tempfile

sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')

from core.storage import JsonStorageBackend
from core.storage_config import create_storage_backend
from core.semantic_memory import SemanticMemory
from core.distributed_memory_manager import DistributedMemoryManager


def test_shared_storage_backend_behavior():
    temp_dir = tempfile.mkdtemp(prefix="livingai_shared_")
    os.environ["LIVING_AI_STORAGE_BACKEND"] = "json"
    os.environ["LIVING_AI_JSON_STORAGE_DIR"] = temp_dir

    backend = create_storage_backend()
    assert isinstance(backend, JsonStorageBackend)

    mem = SemanticMemory(storage_backend=backend)
    mem.add_memory("test memory")
    assert "test memory" in mem.get_memories()

    dist = DistributedMemoryManager(storage_backend=backend)
    dist.store_memory("distributed memory")
    assert len(dist.get_short_term()) == 1
    assert dist.get_short_term()[0] == "distributed memory"
