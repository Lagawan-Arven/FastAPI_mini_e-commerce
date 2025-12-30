import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent

ENV = os.getenv("ENV", "local")

env_file_map = {
    "local": ".env.local",
    "docker": ".env.docker",
}

env_file = env_file_map.get(ENV, ".env")

env_path = BASE_DIR / env_file

if env_path.exists():
    load_dotenv(env_path)
else:
    raise RuntimeError(f"Env file not found: {env_path}")
