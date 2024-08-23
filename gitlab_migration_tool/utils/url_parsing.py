import logging
from urllib.parse import urlparse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_groups_from_url(git_url: str):
    """
    Extract groups from a Git URL.

    Args:
        git_url (str): The Git URL from which to extract groups.

    Returns:
        list: A list of group names extracted from the URL, or an empty list if no groups are found.
    """
    try:
        parsed_url = urlparse(git_url)
        path_parts = parsed_url.path.strip('/').split('/')
        groups = path_parts[:-1]  # Exclude the repository name

        if not groups:
            logger.info("No groups found in the URL.")
            return []

        return groups
    except Exception as e:
        logger.error(f"Error extracting groups from URL: {e}")
        return []

def get_repo_name_from_url(git_url: str):
    """
    Extract the repository name from a Git URL.

    Args:
        git_url (str): The Git URL from which to extract the repository name.

    Returns:
        str: The repository name, without the '.git' suffix if present.
    """
    try:
        parsed_url = urlparse(git_url)
        repo_name = parsed_url.path.strip('/').split('/')[-1]

        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]

        return repo_name
    except Exception as e:
        logger.error(f"Error extracting repository name from URL: {e}")
        return None
