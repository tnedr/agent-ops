"""Integration tests for agt CLI - full workflow with temporary Git repos."""

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
    
    # Initialize git repo
    subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)
    subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
    
    # Create initial commit
    (repo / "README.md").write_text("# Test Repo\n")
    subprocess.run(["git", "add", "README.md"], cwd=repo, check=True, capture_output=True)
    subprocess.run(["git", "commit", "-m", "Initial commit"], cwd=repo, check=True, capture_output=True)
    
    return repo


@pytest.fixture
def bare_remote(tmp_path):
    """Create a bare Git repository as remote."""
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
    return remote


@pytest.fixture
def git_repo_with_remote(git_repo, bare_remote):
    """Create a Git repo with a remote configured."""
    subprocess.run(
        ["git", "remote", "add", "origin", str(bare_remote)],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["git", "push", "-u", "origin", "main"],
        cwd=git_repo,
        check=True,
        capture_output=True,
    )
    return git_repo, bare_remote


def test_full_workflow_start_to_commit(git_repo, monkeypatch):
    """Test full workflow: start → run → commit."""
    # Set up environment
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    # Change to repo directory
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # Clear AGENT_ID
        if "AGENT_ID" in env:
            del env["AGENT_ID"]
            monkeypatch.delenv("AGENT_ID")
        
        # Start worktree
        result = subprocess.run(
            [sys.executable, "-m", "agt", "start"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
            text=True,
        )
        
        # Extract AGENT_ID from output
        lines = result.stdout.split("\n")
        agent_id_line = [line for line in lines if line.startswith("AGENT_ID=")]
        assert len(agent_id_line) > 0
        agent_id = agent_id_line[0].split("=", 1)[1]
        
        # Set AGENT_ID in environment for subsequent commands
        env["AGENT_ID"] = agent_id
        monkeypatch.setenv("AGENT_ID", agent_id)
        
        # Verify worktree was created
        worktree_path = git_repo / ".work" / agent_id
        assert worktree_path.exists()
        
        # Create a file in worktree
        test_file = worktree_path / "demo.txt"
        test_file.write_text("hello from agent")
        
        # Run command in worktree
        subprocess.run(
            [sys.executable, "-m", "agt", "run", "ls", "-la"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Commit changes
        subprocess.run(
            [sys.executable, "-m", "agt", "commit", "feat: add demo file"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Verify commit was created
        result = subprocess.run(
            ["git", "log", "--oneline", "-1"],
            cwd=worktree_path,
            check=True,
            capture_output=True,
            text=True,
        )
        assert "feat: add demo file" in result.stdout
        
    finally:
        os.chdir(original_cwd)


def test_full_workflow_with_push(git_repo_with_remote, monkeypatch):
    """Test full workflow: start → run → commit → push."""
    git_repo, bare_remote = git_repo_with_remote
    
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # Clear AGENT_ID
        if "AGENT_ID" in env:
            del env["AGENT_ID"]
            monkeypatch.delenv("AGENT_ID")
        
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
        assert len(agent_id_line) > 0
        agent_id = agent_id_line[0].split("=", 1)[1]
        env["AGENT_ID"] = agent_id
        monkeypatch.setenv("AGENT_ID", agent_id)
        
        worktree_path = git_repo / ".work" / agent_id
        
        # Create and commit file
        test_file = worktree_path / "demo.txt"
        test_file.write_text("hello from agent")
        
        subprocess.run(
            [sys.executable, "-m", "agt", "commit", "feat: add demo file"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Push to remote
        subprocess.run(
            [sys.executable, "-m", "agt", "push", "origin"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Verify branch exists in remote
        result = subprocess.run(
            ["git", "ls-remote", "--heads", str(bare_remote)],
            check=True,
            capture_output=True,
            text=True,
        )
        branch_name = f"feat/{agent_id}"
        assert f"refs/heads/{branch_name}" in result.stdout
        
    finally:
        os.chdir(original_cwd)


def test_clean_removes_worktree(git_repo, monkeypatch):
    """Test that clean command removes worktree."""
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # Clear AGENT_ID
        if "AGENT_ID" in env:
            del env["AGENT_ID"]
            monkeypatch.delenv("AGENT_ID")
        
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
        monkeypatch.setenv("AGENT_ID", agent_id)
        
        worktree_path = git_repo / ".work" / agent_id
        assert worktree_path.exists()
        
        # Clean worktree
        subprocess.run(
            [sys.executable, "-m", "agt", "clean"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Verify worktree was removed
        assert not worktree_path.exists()
        
    finally:
        os.chdir(original_cwd)


@pytest.mark.integration
def test_full_workflow_with_merge(git_repo_with_remote, monkeypatch):
    """Test full workflow: start → commit → push → merge → verify main."""
    git_repo, bare_remote = git_repo_with_remote
    
    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = env["GIT_COMMITTER_NAME"] = "Test User"
    env["GIT_AUTHOR_EMAIL"] = env["GIT_COMMITTER_EMAIL"] = "test@example.com"
    
    original_cwd = os.getcwd()
    os.chdir(git_repo)
    
    try:
        # Clear AGENT_ID
        if "AGENT_ID" in env:
            del env["AGENT_ID"]
            monkeypatch.delenv("AGENT_ID")
        
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
        assert len(agent_id_line) > 0
        agent_id = agent_id_line[0].split("=", 1)[1]
        env["AGENT_ID"] = agent_id
        monkeypatch.setenv("AGENT_ID", agent_id)
        
        worktree_path = git_repo / ".work" / agent_id
        branch_name = f"feat/{agent_id}"
        
        # Create and commit file
        test_file = worktree_path / "demo.txt"
        test_file.write_text("hello from agent merge test")
        
        subprocess.run(
            [sys.executable, "-m", "agt", "commit", "feat: merge test"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Push to remote
        subprocess.run(
            [sys.executable, "-m", "agt", "push", "origin"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Merge into main
        subprocess.run(
            [sys.executable, "-m", "agt", "merge"],
            cwd=git_repo,
            env=env,
            check=True,
            capture_output=True,
        )
        
        # Verify merge: check that main branch has the commit
        result = subprocess.run(
            ["git", "log", "--oneline", "-1", "main"],
            cwd=git_repo,
            check=True,
            capture_output=True,
            text=True,
        )
        
        assert "feat: merge test" in result.stdout
        
        # Verify that main was pushed to remote
        result = subprocess.run(
            ["git", "ls-remote", "--heads", str(bare_remote), "main"],
            check=True,
            capture_output=True,
            text=True,
        )
        
        assert "refs/heads/main" in result.stdout
        
    finally:
        os.chdir(original_cwd)

