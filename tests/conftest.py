import os
import tempfile
import pytest

from core.storage import JsonStorageBackend


@pytest.fixture(autouse=True)
def ensure_test_storage(tmp_path, monkeypatch):
    # Create an isolated storage directory per test session
    d = str(tmp_path / "livingai_tests")
    os.environ["LIVING_AI_STORAGE_BACKEND"] = "json"
    os.environ["LIVING_AI_JSON_STORAGE_DIR"] = d
    backend = JsonStorageBackend(directory=d)

    # Monkeypatch the create_storage_backend to return this backend when used
    from core import storage_config
    monkeypatch.setattr(storage_config, 'create_storage_backend', lambda: backend)

    yield

    # cleanup not strictly necessary; tmp_path is ephemeral
