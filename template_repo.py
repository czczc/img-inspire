import os
import subprocess
from pathlib import Path

REPO_URL = "https://github.com/freestylefly/awesome-gpt-image-2"
DEFAULT_PATH = Path(__file__).parent / "awesome-gpt-image-2"


def ensure_repo() -> Path:
    path = Path(os.environ.get("TEMPLATE_REPO_PATH", DEFAULT_PATH))
    if not (path / ".git").exists():
        print(f"Cloning template repo to {path}...")
        subprocess.run(["git", "clone", REPO_URL, str(path)], check=True)
    return path
