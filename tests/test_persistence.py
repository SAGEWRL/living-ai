import os
import json
import sys
import tempfile

sys.path.insert(0, r'c:\Users\Administrator\Desktop\living-ai-core')

from core.persistence_utils import load_json_safe, write_json_atomic


def run_persistence_checks():
    tmp_dir = tempfile.mkdtemp(prefix="livingai_test_")
    target = os.path.join(tmp_dir, "test_state.json")

    data = {"foo": "bar", "count": 1}
    assert write_json_atomic(target, data)
    loaded = load_json_safe(target, default={})
    assert loaded == data

    # Simulate a corrupted file and ensure recovery path returns default
    with open(target, "w", encoding="utf-8") as f:
        f.write("{not valid json")

    recovered = load_json_safe(target, default={"restarted": True})
    assert recovered == {"restarted": True}
    assert os.path.exists(target + ".corrupt")

    print("PERSISTENCE_TESTS_PASSED")


def test_persistence_checks():
    run_persistence_checks()


if __name__ == '__main__':
    run_persistence_checks()
