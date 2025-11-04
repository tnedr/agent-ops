# Agent Integration Guide

## Overview

Az agensek két módon használhatják a PR bot-ot:

1. **GitHub Action-ként** (új, ajánlott) - Workflow fájlt hoz létre
2. **CLI-ról** (régi módszer) - Közvetlenül meghívja a scriptet

---

## 🆕 Módszer 1: GitHub Action-ként (Ajánlott)

### Mit kell csinálnia az agentnek?

Az agentnek **workflow fájlt kell létrehoznia** a target repository-ban.

### Pontos Syntax amit be kell írnia:

**Fájl helye:** `.github/workflows/auto-merge.yml`

**Tartalom:**
```yaml
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Agent lépések (pseudocode):

```python
# 1. Létrehozni a workflow fájlt
workflow_content = """
name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

# 2. Fájl létrehozása
write_file(".github/workflows/auto-merge.yml", workflow_content)

# 3. Commit és push
git_add(".github/workflows/auto-merge.yml")
git_commit("feat: add PR bot auto-merge workflow")
git_push()

# 4. PR létrehozása (ha még nincs)
# 5. 'automerge' label hozzáadása a PR-hez
gh_pr_edit(pr_number, add_label="automerge")
```

### Fontos változások:

**Korábban (konzolból):**
```bash
python pr_bot.py --message "fix" --title "Fix bug" --ci
```

**Most (GitHub Action):**
- Workflow fájlt kell létrehozni
- Az action automatikusan fut PR eseményekre
- `automerge` label szükséges a triggerhez

---

## 🔧 Módszer 2: CLI-ról (Régi módszer, még működik)

Ha az agent közvetlenül a scriptet hívja meg (pl. lokális gépen vagy CI-ben), akkor még mindig működik a régi módszer.

### Script helye:

A script az `agent-ops` repo-ban van: `actions/pr-bot/pr_bot.py`

### CLI meghívás:

```bash
python actions/pr-bot/pr_bot.py \
  --message "Your commit message" \
  --title "PR Title" \
  --body "PR Description" \
  --branch "feat/my-branch" \
  --base "main" \
  --wait 5 \
  --ci \
  --force
```

### Agent lépések (CLI módszer):

```python
# 1. Clone vagy pull az agent-ops repo-t
git_clone("https://github.com/tnedr/agent-ops.git")
# vagy
git_pull()  # ha már van

# 2. Script meghívása
run_command([
    "python", "actions/pr-bot/pr_bot.py",
    "--message", commit_message,
    "--title", pr_title,
    "--body", pr_body,
    "--base", "main",
    "--ci" if wait_for_ci else "",
    "--force" if force_merge else ""
])
```

### CLI argumentumok:

| Argument | Típus | Leírás | Alapértelmezett |
|----------|-------|--------|-----------------|
| `--message` | string | Commit message | `""` (required in standalone) |
| `--title` | string | PR title | `""` (required in standalone) |
| `--body` | string | PR description | `""` |
| `--branch` | string | Branch name | `feat/auto-{timestamp}` |
| `--base` | string | Base branch | `main` |
| `--wait` | int | Wait seconds before merge | `5` |
| `--ci` | flag | Wait for CI checks | `false` |
| `--force` | flag | Force merge (admin) | `false` |

### CLI vs Action különbség:

**CLI módban:**
- A script létrehozza a branch-et, commit-ol, push-ol, PR-t nyit
- Teljes standalone workflow

**Action módban:**
- A PR már létezik (a workflow PR event-re fut)
- A script csak merge-el (nem hoz létre PR-t)

---

## 🤖 Agent Implementation Examples

### Python Agent Example

```python
def setup_pr_bot_workflow(repo_path: str):
    """Setup PR bot as GitHub Action in target repo."""
    workflow_dir = os.path.join(repo_path, ".github", "workflows")
    os.makedirs(workflow_dir, exist_ok=True)
    
    workflow_content = """name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    
    workflow_file = os.path.join(workflow_dir, "auto-merge.yml")
    with open(workflow_file, "w") as f:
        f.write(workflow_content)
    
    return workflow_file

def create_pr_with_automerge(repo: str, title: str, body: str, branch: str):
    """Create PR and add automerge label."""
    # Create PR
    pr_number = gh_pr_create(
        repo=repo,
        title=title,
        body=body,
        head=branch,
        base="main"
    )
    
    # Add automerge label (this triggers the workflow!)
    gh_pr_edit(pr_number, add_label="automerge")
    
    return pr_number
```

### JavaScript/TypeScript Agent Example

```typescript
async function setupPRBotWorkflow(repoPath: string): Promise<string> {
  const workflowDir = path.join(repoPath, '.github', 'workflows');
  await fs.mkdir(workflowDir, { recursive: true });
  
  const workflowContent = `name: Auto-merge PR

on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]

jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Auto-merge with PR-bot
        uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
          force: "false"
        env:
          GITHUB_TOKEN: \${{ secrets.GITHUB_TOKEN }}
`;
  
  const workflowFile = path.join(workflowDir, 'auto-merge.yml');
  await fs.writeFile(workflowFile, workflowContent);
  
  return workflowFile;
}

async function createPRWithAutomerge(
  repo: string,
  title: string,
  body: string,
  branch: string
): Promise<number> {
  // Create PR
  const pr = await octokit.rest.pulls.create({
    owner: repo.split('/')[0],
    repo: repo.split('/')[1],
    title,
    body,
    head: branch,
    base: 'main',
  });
  
  // Add automerge label (triggers workflow!)
  await octokit.rest.issues.addLabels({
    owner: repo.split('/')[0],
    repo: repo.split('/')[1],
    issue_number: pr.data.number,
    labels: ['automerge'],
  });
  
  return pr.data.number;
}
```

---

## 📋 Összefoglaló: Mit kell tudnia az agentnek?

### GitHub Action módszer (új):

1. **Workflow fájl létrehozása:**
   - Helye: `.github/workflows/auto-merge.yml`
   - Pontos syntax: lásd fentebb
   - Action reference: `tnedr/agent-ops/actions/pr-bot@main`

2. **PR workflow:**
   - Létrehozza a workflow fájlt
   - Commit-ol és push-ol
   - PR-t hoz létre (ha szükséges)
   - **Hozzáadja az `automerge` labelt** → ez triggereli a bot-ot

3. **Fontos:**
   - Az `automerge` label **kötelező** a triggerhez
   - A workflow csak akkor fut, ha ez a label rajta van

### CLI módszer (régi, még működik):

1. **Script elérése:**
   - Clone az `agent-ops` repo-t
   - Script: `actions/pr-bot/pr_bot.py`

2. **Meghívás:**
   ```bash
   python actions/pr-bot/pr_bot.py --message "..." --title "..." --ci
   ```

3. **Mit csinál:**
   - Létrehozza a branch-et
   - Commit-ol és push-ol
   - PR-t nyit
   - Vár (ha `--ci`, akkor CI-t vár)
   - Merge-el

---

## 🔄 Migration Guide (Régi → Új)

Ha az agensek korábban CLI-ról hívták:

**Régi:**
```python
# Agent code
run_command("python pr_bot.py --message 'fix' --title 'Fix' --ci")
```

**Új (GitHub Action):**
```python
# 1. Workflow fájl létrehozása (egyszer)
create_workflow_file(".github/workflows/auto-merge.yml", workflow_template)

# 2. PR workflow (minden PR-hez)
create_pr(title, body, branch)
add_label_to_pr(pr_number, "automerge")  # Ez triggereli!
```

---

## ❓ FAQ

**Q: Mi a különbség a két módszer között?**

A: 
- **CLI**: Standalone script, létrehozza a PR-t és merge-eli
- **Action**: Workflow fájl, csak merge-eli (PR már létezik)

**Q: Melyiket használjam?**

A: **GitHub Action** (új módszer) - konzisztensebb, GitHub-native

**Q: Működik még a CLI?**

A: Igen, de az Action mód ajánlott

**Q: Az agentnek kell workflow fájlt létrehoznia?**

A: Igen, ha Action módot használ. Egyszer kell létrehozni, utána automatikusan működik.

**Q: Hogyan triggereli az agent a bot-ot?**

A: Az `automerge` label hozzáadásával a PR-hez. Ez triggereli a `labeled` event-et.

