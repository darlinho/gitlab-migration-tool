# tests/test_gitlab_manager.py
import gitlab
import pytest
from unittest.mock import patch, MagicMock
from gitlab_migration_tool.gitlab_manager import GitLabManager

@pytest.fixture
def gitlab_manager():
    return GitLabManager()

def test_find_or_create_group_existing(gitlab_manager, mocker):
    mock_group = MagicMock()
    mocker.patch.object(gitlab_manager.gl.groups, 'get', return_value=mock_group)

    result = gitlab_manager.find_or_create_group("existing-group")
    
    assert result == mock_group
    gitlab_manager.gl.groups.get.assert_called_once_with("existing-group")

def test_find_or_create_group_creates_new(gitlab_manager, mocker):
    mock_group = MagicMock()
    mocker.patch.object(gitlab_manager.gl.groups, 'get', side_effect=gitlab.exceptions.GitlabGetError(None, None))
    mocker.patch.object(gitlab_manager.gl.groups, 'create', return_value=mock_group)

    result = gitlab_manager.find_or_create_group("new-group")
    
    assert result == mock_group
    gitlab_manager.gl.groups.create.assert_called_once_with({
        'name': 'new-group',
        'path': 'new-group',
        'parent_id': None,
        'visibility': 'private'
    })

def test_clone_repository(gitlab_manager, mocker):
    mock_repo = mocker.patch('gitlab_migration_tool.gitlab_manager.Repo.clone_from')
    
    gitlab_manager.clone_repository("username", "password", "https://example.com/repo.git")

    mock_repo.assert_called_once()