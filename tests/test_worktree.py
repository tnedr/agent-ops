"""Tests for agt.worktree module."""

import pytest
from pathlib import Path
from agt.worktree import (
    generate_agent_id,
    get_repo_root,
    get_work_dir,
    get_worktree_path,
)


def test_generate_agent_id():
    """Test that agent ID generation works and is unique."""
    id1 = generate_agent_id()
    id2 = generate_agent_id()
    
    assert id1.startswith("agent-")
    assert id2.startswith("agent-")
    assert id1 != id2
    assert len(id1) == len("agent-") + 8  # 8 hex chars
    assert len(id2) == len("agent-") + 8


def test_agent_id_format():
    """Test that agent IDs follow the expected format."""
    agent_id = generate_agent_id()
    parts = agent_id.split("-", 1)
    
    assert len(parts) == 2
    assert parts[0] == "agent"
    assert len(parts[1]) == 8
    assert all(c in "0123456789abcdef" for c in parts[1])


def test_get_repo_root():
    """Test that get_repo_root returns a valid path."""
    root = get_repo_root()
    assert isinstance(root, Path)
    assert root.exists()
    assert (root / ".git").exists() or (root.parent / ".git").exists()


def test_get_work_dir():
    """Test that get_work_dir returns correct path."""
    root = get_repo_root()
    work_dir = get_work_dir(root)
    
    assert isinstance(work_dir, Path)
    assert work_dir == root / ".work"


def test_get_worktree_path():
    """Test that get_worktree_path returns correct path."""
    root = get_repo_root()
    agent_id = "agent-test123"
    worktree_path = get_worktree_path(root, agent_id)
    
    assert isinstance(worktree_path, Path)
    assert worktree_path == root / ".work" / agent_id

