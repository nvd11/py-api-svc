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
log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
    "<level>{level: <8}</level> | "
    "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(os.path.join(project_path, "logs", "app.log"), format=log_format)

logger.info("basic setup done")


yaml_configs = None
# load additon configs.yaml
with open(os.path.join(project_path, "src", "configs", "config_dev.yaml")) as f:
    yaml_configs = yaml.load(f, Loader=yaml.FullLoader)

logger.info("all configs loaded")
