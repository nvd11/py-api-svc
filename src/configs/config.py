import yaml
import os
import sys
from loguru import logger

# append project path to sys.path
script_path = os.path.abspath(__file__)
project_path = os.path.dirname(os.path.dirname(os.path.dirname(script_path)))

print("project_path is {}".format(project_path))

# append project path to sys.path
sys.path.append(project_path)


# setup logs path
logger.remove()
# Configure sink for stdout to format messages as JSON for GCP Logging.
# The 'serialize=True' flag tells loguru to output logs as a JSON object.
# GCP Logging automatically parses JSON logs from stdout and uses the 'level.name' field
# as the 'severity'. We set the level to "DEBUG" to capture all logs.
logger.add(sys.stdout, serialize=True, level="DEBUG")
# Keep the file logger for local debugging.
logger.add(os.path.join(project_path, "logs", "app.log"), level="DEBUG")

logger.info("basic setup done")


yaml_configs = None
# load additon configs.yaml
with open(os.path.join(project_path, "src", "configs", "config_dev.yaml")) as f:
    yaml_configs = yaml.load(f, Loader=yaml.FullLoader)

logger.info("all configs loaded")
