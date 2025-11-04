# Git Worktree Használata Agensekhez

## Mi az a Git Worktree?

A Git worktree lehetővé teszi, hogy **egy repository-t többször is checkout-oljunk különböző mappákban**, különböző branch-ekre.

**Előnyök agenseknek:**
- ✅ Több branch-en dolgozhat párhuzamosan
- ✅ Nincs állandó branch váltás
- ✅ Minden branch külön mappában van
- ✅ Könnyű követni, melyik mappában melyik branch van

---

## Alapvető Használat

### Worktree Listázása

```bash
git worktree list
```

**Output:**
```
E:/Repos/agent-ops  9bdf99e [main]
```

Ez azt jelenti: 
- `E:/Repos/agent-ops` - fő worktree (main branch)
- `9bdf99e` - commit hash
- `[main]` - branch név

### Új Worktree Létrehozása

```bash
# Új branch-hez új worktree
git worktree add ../agent-ops-feature feat/my-feature

# Meglévő branch-hez worktree
git worktree add ../agent-ops-hotfix hotfix/bug-123
```

**Mit csinál?**
- Létrehoz egy új mappát (`../agent-ops-feature`)
- Checkout-olja a branch-et oda
- A két worktree párhuzamosan használható

### Worktree Törlése

```bash
# Worktree eltávolítása (de branch megmarad)
git worktree remove ../agent-ops-feature

# Vagy ha már törölted a mappát
git worktree prune
```

---

## Agent Használati Példa

### Több Task Párhuzamosan

```python
class Agent:
    def __init__(self, repo_path):
        self.repo_path = repo_path
        self.worktrees = {}
    
    def create_worktree_for_task(self, task_id, branch_name):
        """Worktree létrehozása egy task-hoz"""
        worktree_path = f"{self.repo_path}-{task_id}"
        
        # Worktree létrehozása
        git_worktree_add(
            path=worktree_path,
            branch=branch_name,
            create_branch=True  # Ha még nincs, létrehozza
        )
        
        self.worktrees[task_id] = {
            'path': worktree_path,
            'branch': branch_name
        }
        
        return worktree_path
    
    def work_on_task(self, task_id, changes):
        """Dolgozik egy task-on a saját worktree-ében"""
        worktree_path = self.worktrees[task_id]['path']
        
        # Változtatások a worktree-ben
        for file, content in changes.items():
            write_file(f"{worktree_path}/{file}", content)
            git_add(f"{worktree_path}/{file}")
        
        # Commit a worktree-ben
        git_commit(
            repo_path=worktree_path,
            message=f"feat: task {task_id}"
        )
        
        # Push
        git_push(
            repo_path=worktree_path,
            branch=self.worktrees[task_id]['branch']
        )
    
    def cleanup_worktree(self, task_id):
        """Worktree törlése task után"""
        worktree_path = self.worktrees[task_id]['path']
        git_worktree_remove(worktree_path)
        del self.worktrees[task_id]
```

### Példa Használat

```python
agent = Agent("E:/Repos/agent-ops")

# Task 1: Feature branch
wt1 = agent.create_worktree_for_task("task-1", "feat/agent-task-1")
agent.work_on_task("task-1", {"src/main.py": new_code})

# Task 2: Bugfix branch (párhuzamosan!)
wt2 = agent.create_worktree_for_task("task-2", "feat/agent-task-2")
agent.work_on_task("task-2", {"src/bug.py": bugfix_code})

# Mindkét worktree egyszerre aktív!
# Cursor-ban mindkettő megnyitható külön ablakban
```

---

## Cursor Integráció

### Cursor-ban Worktree Használata

1. **Terminal-ben:**
   ```bash
   git worktree add ../agent-ops-feature feat/my-feature
   ```

2. **Cursor-ban:**
   - File → Open Folder
   - Válaszd ki az új worktree mappát (`../agent-ops-feature`)
   - Most már külön Cursor ablakban van a branch

3. **Párhuzamosan:**
   - Fő repo: `E:/Repos/agent-ops` (main branch)
   - Feature repo: `E:/Repos/agent-ops-feature` (feat/my-feature branch)
   - Mindkettő nyitva lehet külön ablakban!

---

## Gyakorlati Használat

### Scenario: Több Agent, Több Task

```python
# Agent 1: Dolgozik task-1-en
git worktree add ../agent-ops-task1 feat/task-1
cd ../agent-ops-task1
# ... dolgozik ...
git commit -m "feat: task 1"
git push origin feat/task-1

# Agent 2: Dolgozik task-2-en (ugyanabban a repo-ban!)
git worktree add ../agent-ops-task2 feat/task-2
cd ../agent-ops-task2
# ... dolgozik párhuzamosan ...
git commit -m "feat: task 2"
git push origin feat/task-2

# Mindkettő fut egyszerre, nem zavarják egymást!
```

### Worktree Lista

```bash
git worktree list
```

**Output:**
```
E:/Repos/agent-ops          9bdf99e [main]
E:/Repos/agent-ops-task1     abc1234 [feat/task-1]
E:/Repos/agent-ops-task2     def5678 [feat/task-2]
```

---

## Hasznos Parancsok

### Worktree Információ

```bash
# Lista
git worktree list

# Részletes információ
git worktree list --verbose

# Prune (törölt worktree-ek eltávolítása)
git worktree prune
```

### Worktree Műveletek

```bash
# Új worktree új branch-hez
git worktree add ../new-path -b new-branch

# Új worktree meglévő branch-hez
git worktree add ../new-path existing-branch

# Worktree törlése
git worktree remove ../new-path

# Worktree törlése (force, ha locked)
git worktree remove --force ../new-path
```

### Branch Műveletek Worktree-ben

```bash
# Worktree-ben vagyunk
cd ../agent-ops-feature

# Branch műveletek ugyanúgy működnek
git status
git add .
git commit -m "feat: something"
git push origin feat/my-feature

# PR létrehozása
gh pr create --title "Feature" --body "Description"
```

---

## Agent Workflow Worktree-vel

### Teljes Workflow

```python
def process_task_with_worktree(task_id, task):
    """Task feldolgozása worktree-ben"""
    
    # 1. Worktree létrehozása
    branch_name = f"feat/agent-{task_id}"
    worktree_path = f"../agent-ops-{task_id}"
    
    git_worktree_add(
        path=worktree_path,
        branch=branch_name,
        create_branch=True
    )
    
    # 2. Dolgozik a worktree-ben
    os.chdir(worktree_path)
    
    # Változások
    make_changes(task)
    git_add(".")
    git_commit(f"feat: {task_id}")
    git_push(branch_name)
    
    # 3. PR létrehozása
    pr_number = gh_pr_create(
        title=f"Task {task_id}",
        head=branch_name,
        base="main"
    )
    
    # 4. Label hozzáadása (triggereli a GitHub Action-t)
    gh_pr_edit(pr_number, add_label="automerge")
    
    # 5. Cleanup (opcionális - ha már nem kell)
    # git_worktree_remove(worktree_path)
    
    return pr_number
```

---

## Előnyök Agensekhez

### ✅ Párhuzamos Munka

```
Agent 1: ../agent-ops-task1 → feat/task-1 → PR #100
Agent 2: ../agent-ops-task2 → feat/task-2 → PR #101
Agent 3: ../agent-ops-task3 → feat/task-3 → PR #102

Mindegyik párhuzamosan, nem zavarják egymást!
```

### ✅ Könnyű Követés

- Minden task külön mappában
- Minden branch külön worktree-ben
- Nincs állandó branch váltás

### ✅ Cursor Integráció

- Minden worktree külön Cursor ablakban nyitható
- File → Open Folder → worktree mappa
- Párhuzamosan szerkeszthető

---

## Figyelmeztetések

### ⚠️ Ugyanaz a Branch

```bash
# NEM lehet! Egy branch csak egy worktree-ben lehet egyszerre
git worktree add ../path1 feat/my-branch
git worktree add ../path2 feat/my-branch  # ❌ Error!
```

### ⚠️ Worktree Lock

Ha a worktree "locked" (pl. crash után):
```bash
git worktree remove --force ../path
```

### ⚠️ Cleanup

Törölt worktree-ek automatikusan nem törlődnek:
```bash
git worktree prune  # Törölt worktree-ek eltávolítása
```

---

## Összefoglaló

**Git Worktree = Több branch, külön mappákban**

1. ✅ `git worktree add ../path branch` - Worktree létrehozása
2. ✅ `cd ../path` - Worktree-be váltás
3. ✅ Dolgozik, commit-ol, push-ol
4. ✅ PR létrehozása
5. ✅ `git worktree remove ../path` - Cleanup (opcionális)

**Agenseknek:** Több task párhuzamosan, mindegyik saját worktree-ben!

