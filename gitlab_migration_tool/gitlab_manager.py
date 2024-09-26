import os
import shutil
import gitlab
from git import Repo
from urllib.parse import quote
from .config.settings import git_target_repo_url, git_target_private_token, git_source_local_repo_path
from .utils.progress import CloneProgress, PushProgress


class GitLabManager:
    def __init__(self):
        self.gl = gitlab.Gitlab(git_target_repo_url, private_token=git_target_private_token)

    def find_or_create_group(self, group_name, parent_id=None):
        """Find a group by name and create it if it doesn't exist."""
        try:
            if parent_id:
                full_path = f"{self.gl.groups.get(parent_id).full_path}/{group_name}"
                group = self.gl.groups.get(full_path)
            else:
                group = self.gl.groups.get(group_name)
        except gitlab.exceptions.GitlabGetError:
            group_data = {
                'name': group_name,
                'path': group_name,
                'parent_id': parent_id,
                'visibility': 'private',
            }
            group = self.gl.groups.create(group_data)

        return group

    def find_or_create_sub_groups(self, current_parent_group=None, subgroups=None):
        """Check or create nested subgroups."""

        for subgroup_name in subgroups:
            parent_id = current_parent_group.id if current_parent_group else None
            current_parent_group = self.find_or_create_group(subgroup_name, parent_id)

        return current_parent_group

    def create_project_in_group(self, repo_name, parent_group):
        """Create a project in a given group."""
        try:
            project = self.gl.projects.create({'name': repo_name, 'namespace_id': parent_group.id})
            print(f"Project '{repo_name}' created in the group '{parent_group.full_path}'.")
            return project.http_url_to_repo
        except gitlab.exceptions.GitlabCreateError as e:
            print(f"Error creating project: {e}")
            return None

    def clone_repository(self, username, password, repo_url):
        """Clone the repository from the source."""
        # Remove the directory if it exists
        if os.path.exists(git_source_local_repo_path):
            print(f"Removing existing directory: {git_source_local_repo_path}")
            shutil.rmtree(git_source_local_repo_path)

        encoded_username = quote(username)
        encoded_password = quote(password)

        auth_repo_url = repo_url.replace("https://", f"https://{encoded_username}:{encoded_password}@")

        clone_dir = os.path.join(os.getcwd(), git_source_local_repo_path)

        try:
            Repo.clone_from(auth_repo_url, clone_dir, progress=CloneProgress())
            print(f"Repository successfully cloned to: {clone_dir}")
        except Exception as e:
            print(f"Error while cloning the repository: {e}")

    def push_all_branches_to_new_repo(self, local_repo_path, new_repo_url):
        """Push all branches from a local Git repository to a new remote repository."""
        try:
            repo = Repo(local_repo_path)
            if repo.bare:
                print(f"The repository at {local_repo_path} is bare or invalid.")
                return

            if 'new-origin' in repo.remotes:
                new_origin = repo.remote('new-origin')
                new_origin.set_url(new_repo_url)
            else:
                new_origin = repo.create_remote('new-origin', new_repo_url)

            repo.git.fetch('--all')

            for remote_ref in repo.refs:
                if 'origin/' in remote_ref.name and remote_ref.name != 'origin/HEAD':
                    branch_name = remote_ref.name.replace('origin/', '')
                    if branch_name not in repo.heads:
                        repo.create_head(branch_name, remote_ref)
                    repo.heads[branch_name].set_tracking_branch(remote_ref)
                    print(f"Branch {branch_name} is now tracked locally.")

            for ref in repo.heads:
                print(f"Pushing branch {ref.name} to {new_repo_url}")
                new_origin.push(ref.name, progress=PushProgress())

            print("All branches have been pushed successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
