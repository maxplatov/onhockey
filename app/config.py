import yaml

CONFIG_PATH = "./config.yml"

with open(CONFIG_PATH, "r") as config_file:
    CONFIG = yaml.safe_load(config_file)

TOKEN_SECRET = CONFIG["secret"]

_DSN = "{username}:{pwd}@{host}:{port}/{database}".format(**CONFIG["db"])

DSN = "postgresql://" + _DSN  # for generate migration
DSN_ASYNC = "postgresql+asyncpg://" + _DSN  # for application to work
