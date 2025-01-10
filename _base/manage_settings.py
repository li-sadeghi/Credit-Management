import os
from decouple import Config, RepositoryEnv

# We check that what is the environment: development, production, test, ...
ENVIRONMENT = os.environ.get("ENV", "development").lower()
if ENVIRONMENT == "development":
    env_file = "config/development.env"

config = Config(RepositoryEnv(env_file))
