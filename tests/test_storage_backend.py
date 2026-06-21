import os
import sys
import tempfile

sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')

from core.storage import JsonStorageBackend


def test_json_storage_backend():
    temp_dir = tempfile.mkdtemp(prefix="livingai_storage_")
    backend = JsonStorageBackend(directory=temp_dir)
    key = "test_storage"
    data = {"hello": "world", "count": 1}

    assert backend.set(key, data)
    assert backend.exists(key)
    assert backend.get(key) == data
    assert backend.delete(key)
    assert not backend.exists(key)
