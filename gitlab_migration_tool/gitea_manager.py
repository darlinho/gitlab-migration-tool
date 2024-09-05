import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning # type: ignore
from .config.settings import git_source_url, git_source_token
from rich.console import Console

console = Console()

# Suppress only the single InsecureRequestWarning from urllib3
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class GiteaManager:
    def __init__(self):
        """
        Initialize the GiteaManager with the Gitea instance URL and API token.
        """
        self.gitea_url = git_source_url.rstrip('/')
        self.api_token = git_source_token
        self.headers = {
            'Authorization': f'token {self.api_token}'
        }
                
    def get_all_organizations(self):
        """
        Retrieve all organizations from the Gitea instance and return their names.
        """
        url = f"{self.gitea_url}/api/v1/user/orgs"
      
        with console.status("[bold green]Fetching all organizations..."):
            response = requests.get(url, headers=self.headers, verify=False)

            if response.status_code != 200:
                print(f"Failed to retrieve organizations. Status code: {response.status_code}")
                return []

            organizations = response.json()
            console.log("Organisation fetched successfully !")
            
        return [org['username'] for org in organizations]
      
    def get_repos_for_organization(self, org_name):
        """
        Retrieve all repositories for a specific organization.
        """
        url = f"{self.gitea_url}/api/v1/orgs/{org_name}/repos"
        
        response = requests.get(url, headers=self.headers, verify=False)

        if response.status_code != 200:
            print(f"Failed to retrieve repositories for organization {org_name}. Status code: {response.status_code}")
            return []

        repos = response.json()

        # Return a list containing the url of the repositories
        return [repo['clone_url'] for repo in repos]
        

    def get_all_repositories(self):
        """
        Retrieve repositories from all organizations and return a flat list of repository names.
        """
        organizations = self.get_all_organizations()
        all_repos = []
        
        with console.status("[bold green]Fetching all repos of organizations..."):
          for org in organizations:
            repos = self.get_repos_for_organization(org)
            console.log(f"Repositories for {org} successfully fetched !!")
            all_repos.extend(repos)

        return all_repos
