"""CLI entrypoint for agt command."""

import os
import subprocess
import sys
from pathlib import Path

from agt.worktree import (
    add_worktree,
    generate_agent_id,
    get_repo_root,
    get_worktree_path,
    remove_worktree,
)


def safe_print(msg: str, file=sys.stdout) -> None:
    """Print message with ASCII fallback for Unicode characters."""
    try:
        print(msg, file=file)
    except UnicodeEncodeError:
        # Fallback to ASCII-safe characters
        msg = msg.replace("✅", "[OK]")
        msg = msg.replace("🚀", "[PUSHED]")
        msg = msg.replace("❌", "[ERROR]")
        print(msg, file=file)


def err(msg: str) -> None:
    """Print error and exit."""
    safe_print(f"❌ {msg}", file=sys.stderr)
    sys.exit(1)


def cmd_start(base_branch: str = "main") -> None:
    """Start a new agent worktree."""
    root = get_repo_root()
    agent_id = generate_agent_id()
    
    # Store in environment for subsequent commands
    os.environ["AGENT_ID"] = agent_id
    
    worktree_path, branch_name = add_worktree(root, agent_id, base_branch)
    
    safe_print(f"✅ Worktree ready: {worktree_path} (branch {branch_name})")
    print(f"AGENT_ID={agent_id}")


def cmd_run(command: list[str]) -> None:
    """Run a command in the agent worktree."""
    agent_id = os.environ.get("AGENT_ID")
    if not agent_id:
        err("Run 'agt start' first!")
    
    root = get_repo_root()
    worktree_path = get_worktree_path(root, agent_id)
    
    if not worktree_path.exists():
        err(f"Worktree not found: {worktree_path}. Run 'agt start' first!")
    
    if not command:
        err("Missing command to run")
    
    # Execute command in worktree directory
    # Join command parts and run in shell to support pipes, redirects, etc.
    # Note: On Windows, shell=True uses cmd.exe, not PowerShell
    cmd_str = " ".join(command)
    try:
        subprocess.run(cmd_str, check=True, cwd=worktree_path, shell=True)
    except subprocess.CalledProcessError as e:
        sys.exit(e.returncode)


def cmd_commit(message: str) -> None:
    """Commit changes in the agent worktree."""
    agent_id = os.environ.get("AGENT_ID")
    if not agent_id:
        err("Run 'agt start' first!")
    
    root = get_repo_root()
    worktree_path = get_worktree_path(root, agent_id)
    
    if not worktree_path.exists():
        err(f"Worktree not found: {worktree_path}. Run 'agt start' first!")
    
    # Stage all changes
    subprocess.run("git add -A", shell=True, check=True, cwd=worktree_path)
    
    # Commit - use list form to avoid shell escaping issues
    subprocess.run(
        ["git", "commit", "-m", message],
        check=True,
        cwd=worktree_path,
    )
    
    safe_print("✅ Commit ready")


def cmd_push(remote: str = "origin") -> None:
    """Push the agent branch to remote."""
    agent_id = os.environ.get("AGENT_ID")
    if not agent_id:
        err("Run 'agt start' first!")
    
    root = get_repo_root()
    worktree_path = get_worktree_path(root, agent_id)
    
    if not worktree_path.exists():
        err(f"Worktree not found: {worktree_path}. Run 'agt start' first!")
    
    # Push branch
    subprocess.run(
        f"git push -u {remote} HEAD",
        shell=True,
        check=True,
        cwd=worktree_path,
    )
    
    safe_print("🚀 Pushed to remote; open a PR in the UI if needed")


def cmd_merge() -> None:
    """Merge agent branch into main (fast-forward only)."""
    agent_id = os.environ.get("AGENT_ID")
    if not agent_id:
        err("Run 'agt start' first!")
    
    root = get_repo_root()
    worktree_path = get_worktree_path(root, agent_id)
    
    if not worktree_path.exists():
        err(f"Worktree not found: {worktree_path}. Run 'agt start' first!")
    
    branch_name = f"feat/{agent_id}"
    
    # Fetch latest main
    subprocess.run("git fetch origin main", shell=True, check=True, cwd=worktree_path)
    
    # Rebase onto main
    subprocess.run("git rebase origin/main", shell=True, check=True, cwd=worktree_path)
    
    # Switch to main branch in root repo
    subprocess.run("git checkout main", shell=True, check=True, cwd=root)
    
    # Fast-forward merge
    subprocess.run(
        f"git merge --ff-only {branch_name}",
        shell=True,
        check=True,
        cwd=root,
    )
    
    # Push to remote
    subprocess.run("git push origin main", shell=True, check=True, cwd=root)
    
    safe_print("✅ Branch fast-forwarded to main")


def cmd_clean() -> None:
    """Remove the agent worktree."""
    agent_id = os.environ.get("AGENT_ID")
    if not agent_id:
        err("Run 'agt start' first!")
    
    root = get_repo_root()
    worktree_path = get_worktree_path(root, agent_id)
    
    if not worktree_path.exists():
        err(f"Worktree not found: {worktree_path}. Run 'agt start' first!")
    
    remove_worktree(root, agent_id)
    safe_print(f"✅ Worktree removed ({agent_id})")


def main() -> None:
    """Main CLI entrypoint."""
    if len(sys.argv) < 2:
        print("Usage: agt <start|run|commit|push|merge|clean> [args...]", file=sys.stderr)
        sys.exit(1)
    
    cmd = sys.argv[1]
    args = sys.argv[2:]
    
    if cmd == "start":
        base_branch = args[0] if args else "main"
        cmd_start(base_branch)
    
    elif cmd == "run":
        if not args:
            err("Missing command to run")
        cmd_run(args)
    
    elif cmd == "commit":
        if not args:
            err('Usage: agt commit "<message>"')
        message = args[0]
        cmd_commit(message)
    
    elif cmd == "push":
        remote = args[0] if args else "origin"
        cmd_push(remote)
    
    elif cmd == "merge":
        cmd_merge()
    
    elif cmd == "clean":
        cmd_clean()
    
    else:
        err(f"Unknown subcommand: {cmd}")


if __name__ == "__main__":
    main()

