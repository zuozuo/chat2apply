import yaml
import logging.config
from pathlib import Path

# Load the logger configuration from YAML file
config_path = Path(__file__).with_name('logger.yaml')
with open(config_path, "r") as config_file:
    config = yaml.safe_load(config_file)

# Configure the logger using the loaded YAML configuration
logging.config.dictConfig(config)

logger = logging.getLogger("bot_logger")

# Usage example
# logger = logging.getLogger("my_logger")
# logger.debug("Debug message")
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Critical message")
