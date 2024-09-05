import json
import os
from .config.settings import (
    git_source_username, git_source_password, 
    git_target_parent_group_name, git_source_local_repo_path
)
from .utils.url_parsing import get_groups_from_url, get_repo_name_from_url
from .gitlab_manager import GitLabManager

def main():
    def load_repositories(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['repositories']
    
    repositories = load_repositories('repos.json')
    
    # Initialize the GitLabManager
    gitlab_manager = GitLabManager()
    
    for repo in repositories:
        git_source_repo_url = repo['url']

        # Extract subgroups and repository name from the source URL
        subgroups = get_groups_from_url(git_source_repo_url)
        repo_name = get_repo_name_from_url(git_source_repo_url)

        # Clone the source repository
        gitlab_manager.clone_repository(git_source_username, git_source_password, git_source_repo_url)

        # Find or create group if parent group is set
        if git_target_parent_group_name:
            parent_group = gitlab_manager.find_or_create_group(git_target_parent_group_name)
        
        last_group = gitlab_manager.find_or_create_sub_groups(subgroups, parent_group)
        git_target_current_http_url_to_repo = gitlab_manager.create_project_in_group(repo_name, last_group)

        # Push all branches to the new repository
        gitlab_manager.push_all_branches_to_new_repo(git_source_local_repo_path, git_target_current_http_url_to_repo)

if __name__ == "__main__":
    main()