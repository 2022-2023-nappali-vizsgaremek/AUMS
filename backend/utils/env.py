# Local imports
from utils.close import exit_app

# External imports
try: from dotenv import dotenv_values
except ImportError as import_error: exit_app(f"Module not found: {import_error}")

def get_env(key: str) -> str:
    """
    Get an environment variable

    Args:
        key (str): Key of the environment variable

    Returns:
        str: Value of the environment variable
    """

    config = dotenv_values(".env")
    env_value = config.get(key)

    if not env_value: exit_app(f"Environment variable not found: {key}")
    return config[key]