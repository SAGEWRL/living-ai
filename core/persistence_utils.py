import json
import os
import tempfile


def write_json_atomic(path, data, indent=2):
    directory = os.path.dirname(os.path.abspath(path))
    os.makedirs(directory, exist_ok=True)
    fd, temp_path = tempfile.mkstemp(dir=directory, prefix=".tmp_", suffix=".json")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        os.replace(temp_path, path)
        return True
    except Exception:
        try:
            if os.path.exists(temp_path):
                os.remove(temp_path)
        except Exception:
            pass
        return False


def load_json_safe(path, default=None):
    if default is None:
        default = {}
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        # Move corrupted file aside and continue with default data
        corrupt_path = f"{path}.corrupt"
        try:
            if os.path.exists(corrupt_path):
                os.remove(corrupt_path)
            os.replace(path, corrupt_path)
        except Exception:
            pass
        return default
