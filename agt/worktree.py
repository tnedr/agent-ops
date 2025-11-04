"""Low-level Git worktree helper functions."""

import os
import subprocess
import uuid
from pathlib import Path
from typing import Optional


def get_repo_root() -> Path:
    """Get the root of the current Git repository."""
    result = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        capture_output=True,
        text=True,
        check=True,
    )
    return Path(result.stdout.strip())


def generate_agent_id() -> str:
    """Generate a unique agent ID."""
    return f"agent-{uuid.uuid4().hex[:8]}"


def get_work_dir(root: Optional[Path] = None) -> Path:
    """Get the work directory path (.work in repo root)."""
    if root is None:
        root = get_repo_root()
    return root / ".work"


def add_worktree(root: Path, agent_id: str, base_branch: str = "main") -> tuple[Path, str]:
    """
    Add a new Git worktree for an agent.
    
    Returns:
        tuple: (worktree_path, branch_name)
    """
    work_dir = get_work_dir(root)
    work_dir.mkdir(parents=True, exist_ok=True)
    
    worktree_path = work_dir / agent_id
    branch_name = f"feat/{agent_id}"
    
    subprocess.run(
        ["git", "worktree", "add", str(worktree_path), "-b", branch_name, base_branch],
        check=True,
        cwd=root,
    )
    
    return worktree_path, branch_name


def remove_worktree(root: Path, agent_id: str) -> None:
    """Remove a Git worktree."""
    work_dir = get_work_dir(root)
    worktree_path = work_dir / agent_id
    
    if worktree_path.exists():
        subprocess.run(
            ["git", "worktree", "remove", str(worktree_path)],
            check=True,
            cwd=root,
        )


def get_worktree_path(root: Path, agent_id: str) -> Path:
    """Get the worktree path for an agent ID."""
    work_dir = get_work_dir(root)
    return work_dir / agent_id

