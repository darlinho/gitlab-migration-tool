# GitLab Migration Tool

This project provides a set of tools to automate the migration of repositories from one git provider instance to another. The tool allows you to clone a repository from a source instance, create the corresponding groups and project in the target GitLab instance, and push all branches from the source repository to the newly created target repository.

## Features

- **Clone a Repository:** Clones a Git repository from a source instance to a local directory.
- **Create Nested Groups:** Automatically creates the necessary groups and sub-groups in the target GitLab instance based on the source repository's URL.
- **Create and Push Project:** Creates the project in the target GitLab instance and pushes all branches from the source repository to the new project.
- **Handles Authentication:** Uses environment variables to manage authentication to both the source and target GitLab instances.

## Project Structure

The project is structured to keep functionality modular and organized:

- **`main.py`:** The main entry point for the application.
- **`config/settings.py`:** Contains configuration settings, such as loading environment variables.
- **`gitlab_manager.py`:** A consolidated module containing all GitLab operations, including group management, project creation, and repository operations.
- **`utils/`:** Contains utility modules such as progress bars and URL parsing.
- **`tests/`:** Contains test cases for the project, ensuring the reliability of the migration process.

## Installation

### Prerequisites

- Python 3.8 or later
- Git installed on your machine
- A source and target GitLab instance

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://gitlab.com/darlinho/migrate-repository-from-one-source-to-another.git
   cd migrate-repository-from-one-source-to-another
2. **Install Poetry (if not already installed):**
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
3. **Install dependencies using Poetry:**
   ```bash
   poetry install
This command will create a virtual environment and install all the required dependencies specified in pyproject.toml.

4. **Activate the virtual environment:**
   ```bash
    poetry shell
5. **Configure environment variables:**
   ```bash
    cp .env.example .env
Replace the values in your **.env** file with your actual GitLab instance details.

### Usage

1. **Run the migration script:**
   ```bash
   poetry run start
  This will clone the source repository, create the necessary groups and project on the target GitLab instance, and push all branches to the new project.

2. **Check the target GitLab instance:**
  After running the script, verify that all groups, sub-groups, and branches have been successfully migrated to the target GitLab instance.

## Notes
- The tool assumes that the target GitLab instance uses the same authentication method for all API calls (private tokens in this case).
- The script will delete the local clone directory (/tmp/cloned_repo) if it already exists, ensuring a fresh clone each time.

## Troubleshooting
- **Authentication Issues:** Ensure that your **.env** file has the correct credentials and tokens.
- **Directory Deletion Issues:** If the script fails to delete the /tmp/cloned_repo directory, manually delete it and rerun the script.
- **Branch Pushing Issues:** Ensure that all branches are correctly fetched and tracked in the local repository before they are pushed to the target repository.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.