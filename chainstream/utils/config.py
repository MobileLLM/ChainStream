import yaml
import os
from pathlib import Path

CONFIG_FILE = os.path.join(Path(__file__).parent.parent, "config.yaml")
CONFIG = None


def load_config():
    global CONFIG

