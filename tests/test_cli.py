"""Tests for agt.cli module - CLI command unit tests."""

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest

# Add parent directory to path to import agt
sys.path.insert(0, str(Path(__file__).parent.parent / "agt"))

from agt.cli import (
    cmd_clean,
    cmd_commit,
    cmd_push,
    cmd_run,
    cmd_start,
    err,
    main,
)


def test_err_function():
    """Test that err function prints message and exits."""
    with pytest.raises(SystemExit) as exc_info:
        err("Test error message")
    
    assert exc_info.value.code == 1


def test_cmd_start_creates_worktree(monkeypatch, tmp_path):
    """Test that cmd_start creates a worktree and sets AGENT_ID."""
    # Create a temporary git repo
    repo = tmp_path / "test_repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial"], cwd=repo, check=True, capture_output=True)
    
    # Mock get_repo_root to return our test repo
    with patch("agt.cli.get_repo_root", return_value=repo):
        # Clear AGENT_ID if set
        if "AGENT_ID" in os.environ:
            monkeypatch.delenv("AGENT_ID")
        
        cmd_start("main")
        
        # Check that AGENT_ID was set
        assert "AGENT_ID" in os.environ
        agent_id = os.environ["AGENT_ID"]
        assert agent_id.startswith("agent-")
        
        # Check that worktree was created
        worktree_path = repo / ".work" / agent_id
        assert worktree_path.exists()


def test_cmd_start_without_agent_id_fails(monkeypatch):
    """Test that cmd_run fails without AGENT_ID."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        cmd_run(["echo", "test"])
    
    assert exc_info.value.code == 1


def test_cmd_commit_without_agent_id_fails(monkeypatch):
    """Test that cmd_commit fails without AGENT_ID."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        cmd_commit("test message")
    
    assert exc_info.value.code == 1


def test_cmd_push_without_agent_id_fails(monkeypatch):
    """Test that cmd_push fails without AGENT_ID."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        cmd_push()
    
    assert exc_info.value.code == 1


def test_cmd_clean_without_agent_id_fails(monkeypatch):
    """Test that cmd_clean fails without AGENT_ID."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        cmd_clean()
    
    assert exc_info.value.code == 1


def test_main_without_args_exits():
    """Test that main exits with usage message when no args."""
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["agt"]):
            main()
    
    assert exc_info.value.code == 1


def test_main_unknown_command_exits():
    """Test that main exits on unknown command."""
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["agt", "unknown"]):
            main()
    
    assert exc_info.value.code == 1


def test_main_start_command(monkeypatch, tmp_path):
    """Test that main dispatches start command correctly."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=repo, check=True)
    subprocess.run(["git", "commit", "--allow-empty", "-m", "Initial"], cwd=repo, check=True, capture_output=True)
    
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with patch("agt.cli.get_repo_root", return_value=repo):
        with patch("sys.argv", ["agt", "start"]):
            main()
        
        assert "AGENT_ID" in os.environ


def test_main_commit_command_missing_message(monkeypatch):
    """Test that main commit command fails without message."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["agt", "commit"]):
            main()
    
    assert exc_info.value.code == 1


def test_main_run_command_missing_command(monkeypatch):
    """Test that main run command fails without command."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["agt", "run"]):
            main()
    
    assert exc_info.value.code == 1

