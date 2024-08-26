import os
from dotenv import load_dotenv, find_dotenv

# Try to find the .env file
dotenv_path = find_dotenv()

if not dotenv_path:
    raise FileNotFoundError("Error: .env file not found. Please ensure that the .env file exists in the project root directory.")

# Load environment variables from the .env file
load_dotenv(dotenv_path)

# Access environment variables
git_source_username = os.getenv('GIT_SOURCE_USERNAME')
git_source_password = os.getenv('GIT_SOURCE_PASSWORD')
git_target_repo_url = os.getenv('GIT_TARGET_REPO_URL')
git_target_private_token = os.getenv('GIT_TARGET_PRIVATE_TOKEN')
git_target_parent_group_name = os.getenv('GIT_TARGET_PARENT_GROUP_NAME')
git_source_local_repo_path = "/tmp/cloned_repo"

# Check if critical environment variables are missing
required_vars = [
    "GIT_SOURCE_USERNAME", "GIT_SOURCE_PASSWORD",
    "GIT_TARGET_REPO_URL", "GIT_TARGET_PRIVATE_TOKEN", "GIT_TARGET_PARENT_GROUP_NAME"
]

for var in required_vars:
    if not os.getenv(var):
        raise EnvironmentError(f"Error: The environment variable '{var}' is not set in the .env file.")

