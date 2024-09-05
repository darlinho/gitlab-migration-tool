import json
from rich.console import Console
from rich.panel import Panel

from .config.settings import (
    git_source_username, git_source_password, 
    git_target_parent_group_name, git_source_local_repo_path,
    git_source_url, git_source_token
)
from .utils.url_parsing import get_groups_from_url, get_repo_name_from_url
from .gitlab_manager import GitLabManager
from .gitea_manager import GiteaManager

console = Console()

def main():
    # Check if Gitea source settings are provided
    if git_source_url and git_source_token:
        # Initialize the GiteaManager
        gitea_manager = GiteaManager()
        repositories = gitea_manager.get_all_repositories()
    else:
        # Load repositories from repos.json if no Gitea source settings are provided
        def load_repositories(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
            return data['repositories']
        
        repositories = load_repositories('repos.json')
    
    # Initialize the GitLabManager
    gitlab_manager = GitLabManager()
    
    for repo_url in repositories:
        # Extract subgroups and repository name from the repository URL
        subgroups = get_groups_from_url(repo_url)
        repo_name = get_repo_name_from_url(repo_url)
        
        message = f"Début de la migration du repo: {repo_name}"
        console.print(Panel.fit(f"[bold magenta]{message}[/bold magenta]", border_style="green"))

        # Clone the source repository
        gitlab_manager.clone_repository(git_source_username, git_source_password, repo_url)

        # Find or create group if parent group is set
        if git_target_parent_group_name:
            parent_group = gitlab_manager.find_or_create_group(git_target_parent_group_name)
            last_group = gitlab_manager.find_or_create_sub_groups(parent_group, subgroups)
        else:
            last_group = gitlab_manager.find_or_create_sub_groups(None, subgroups)
        
        git_new_repo_url = gitlab_manager.create_project_in_group(repo_name, last_group)

        # Push all branches to the new repository
        gitlab_manager.push_all_branches_to_new_repo(git_source_local_repo_path, git_new_repo_url)

if __name__ == "__main__":
    main()