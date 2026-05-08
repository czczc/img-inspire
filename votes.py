import json
from pathlib import Path

_FILE = Path("votes.json")

# votes.json structure:
# {"counts": {"template_id": {"up": N, "down": N}, ...}}


def _load_raw() -> dict:
    if not _FILE.exists():
        return {"counts": {}}
    data = json.loads(_FILE.read_text())
    # migrate old formats
    if "counts" not in data:
        data = {"counts": {}}
    data["counts"].pop("current", None)
    return data


def load() -> dict:
    return _load_raw()


def _save(data: dict) -> None:
    _FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def record(template_id: str, direction: str) -> dict:
    """Always increments the given direction. Returns updated {up, down}."""
    data = _load_raw()
    counts = data["counts"].setdefault(template_id, {"up": 0, "down": 0})
    if direction in ("up", "down"):
        counts[direction] += 1
    _save(data)
    return {"up": counts["up"], "down": counts["down"]}


def get_info(template_id: str, data: dict) -> dict:
    counts = data["counts"].get(template_id, {"up": 0, "down": 0})
    return {"up": counts["up"], "down": counts["down"]}


def weight(template_id: str, data: dict) -> float:
    counts = data["counts"].get(template_id, {"up": 0, "down": 0})
    net = counts["up"] - counts["down"]
    return max(0.1, 1.0 + net * 0.5)
