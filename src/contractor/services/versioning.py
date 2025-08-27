
from git import Repo, GitCommandError
from pathlib import Path

def ensure_repo(root: Path) -> Repo | None:
    try:
        if (root / ".git").exists():
            return Repo(root)
        return Repo.init(root)
    except Exception as e:
        print(f"[WARN] Git init failed: {e}")
        return None

def commit_all(root: Path, message: str) -> bool:
    repo = ensure_repo(root)
    if not repo:
        return False
    try:
        repo.git.add(A=True)
        if repo.is_dirty():
            repo.index.commit(message)
        return True
    except GitCommandError as e:
        print(f"[WARN] Git commit failed: {e}")
        return False
