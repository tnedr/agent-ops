"""Negative test cases - error handling and edge cases."""

import os
import subprocess
import sys
from pathlib import Path

import pytest

# Add parent directory to path to import agt
sys.path.insert(0, str(Path(__file__).parent.parent / "agt"))


@pytest.fixture
def git_repo(tmp_path):
    """Create a temporary Git repository for testing."""
    repo = tmp_path / "test_repo"
    repo.mkdir()
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    (repo / "README.md").write_text("# Test\n")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial"], cwd=repo, check=True, capture_output=True)
    return repo


def test_run_without_start_fails(git_repo, monkeypatch):
    """Test that run fails without AGENT_ID (no start)."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "agt", "run", "echo", "test"],
            cwd=git_repo,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )
        
        assert result.returncode != 0
        assert "Run 'agt start' first" in result.stderr
        
    finally:
        os.chdir(original_cwd)


def test_commit_without_start_fails(git_repo, monkeypatch):
    """Test that commit fails without AGENT_ID (no start)."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "agt", "commit", "test message"],
            cwd=git_repo,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )
        
        assert result.returncode != 0
        assert "Run 'agt start' first" in result.stderr
        
    finally:
        os.chdir(original_cwd)


def test_push_without_start_fails(git_repo, monkeypatch):
    """Test that push fails without AGENT_ID (no start)."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "agt", "push"],
            cwd=git_repo,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )
        
        assert result.returncode != 0
        assert "Run 'agt start' first" in result.stderr
        
    finally:
        os.chdir(original_cwd)


def test_clean_without_start_fails(git_repo, monkeypatch):
    """Test that clean fails without AGENT_ID (no start)."""
    if "AGENT_ID" in os.environ:
        monkeypatch.delenv("AGENT_ID")
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "agt", "clean"],
            cwd=git_repo,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )
        
        assert result.returncode != 0
        assert "Run 'agt start' first" in result.stderr
        
    finally:
        os.chdir(original_cwd)


def test_clean_with_invalid_agent_id_fails(git_repo, monkeypatch):
    """Test that clean fails with non-existent worktree."""
    monkeypatch.setenv("AGENT_ID", "agent-nonexistent")
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        result = subprocess.run(
            [sys.executable, "-m", "agt", "clean"],
            cwd=git_repo,
            env=os.environ.copy(),
            capture_output=True,
            text=True,
        )
        
        assert result.returncode != 0
        assert "Worktree not found" in result.stderr
        
    finally:
        os.chdir(original_cwd)


def test_commit_without_changes_fails(git_repo, monkeypatch):
    """Test that commit fails when there are no changes to commit."""
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # Start worktree
        result = subprocess.run(
            [sys.executable, "-m", "agt", "start"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        
        # Extract AGENT_ID
        lines = result.stdout.split("\n")
        agent_id_line = [line for line in lines if line.startswith("AGENT_ID=")]
        agent_id = agent_id_line[0].split("=", 1)[1]
        env["AGENT_ID"] = agent_id
        
        # Try to commit with no changes
        result = subprocess.run(
            [sys.executable, "-m", "agt", "commit", "empty commit"],
            cwd=git_repo,
            env=env,
            capture_output=True,
            text=True,
        )
        
        # Git will fail with "nothing to commit"
        assert result.returncode != 0
        
    finally:
        os.chdir(original_cwd)


def test_start_twice_creates_two_worktrees(git_repo, monkeypatch):
    """Test that starting twice creates two separate worktrees."""
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # First start
        result1 = subprocess.run(
            [sys.executable, "-m", "agt", "start"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        
        lines1 = result1.stdout.split("\n")
        agent_id1_line = [line for line in lines1 if line.startswith("AGENT_ID=")]
        agent_id1 = agent_id1_line[0].split("=", 1)[1]
        
        # Clear AGENT_ID for second start
        if "AGENT_ID" in env:
            del env["AGENT_ID"]
        
        # Second start
        result2 = subprocess.run(
            [sys.executable, "-m", "agt", "start"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        
        lines2 = result2.stdout.split("\n")
        agent_id2_line = [line for line in lines2 if line.startswith("AGENT_ID=")]
        agent_id2 = agent_id2_line[0].split("=", 1)[1]
        
        # Verify two different IDs
        assert agent_id1 != agent_id2
        
        # Verify both worktrees exist
        worktree1 = git_repo / ".work" / agent_id1
        worktree2 = git_repo / ".work" / agent_id2
        assert worktree1.exists()
        assert worktree2.exists()
        
    finally:
        os.chdir(original_cwd)

