from environs import Env
import os

# Initialize the environs Env instance
env = Env()

# Define the path to the .env file
dotenv_path = os.path.join(os.getcwd(), ".env")

# Check if the .env file exists and is required
if not os.path.exists(dotenv_path):
    raise FileNotFoundError("Error: .env file is required but not found in the project root directory.")

# Load environment variables from the .env file
env.read_env(dotenv_path)

# Access environment variables with automatic type conversion and error handling
git_source_username = env("GIT_SOURCE_USERNAME", required=True)
git_source_password = env("GIT_SOURCE_PASSWORD", required=True)
git_target_repo_url = env("GIT_TARGET_REPO_URL", required=True)
git_target_private_token = env("GIT_TARGET_PRIVATE_TOKEN", required=True)
git_target_parent_group_name = env("GIT_TARGET_PARENT_GROUP_NAME", required=True)
git_source_local_repo_path = env("GIT_SOURCE_LOCAL_REPO_PATH", default="/tmp/cloned_repo")