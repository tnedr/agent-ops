# Teljes Workflow - Agent Lépései

## Fontos: Két Fázis van!

### 1. FÁZIS: Agent dolgozik (Branch → Commit → PR)
### 2. FÁZIS: GitHub Action fut (PR Merge)

---

## 1. FÁZIS: Agent Munkája

### Lépésről Lépésre

#### 1.1. Agent létrehozza a workflow fájlt (csak első alkalommal)

```python
# Agent kód
workflow_content = """name: Auto-merge PR
on:
  pull_request:
    types: [labeled]
jobs:
  merge:
    if: contains(github.event.pull_request.labels.*.name, 'automerge')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""

# Létrehozás
write_file(".github/workflows/auto-merge.yml", workflow_content)
git_add(".github/workflows/auto-merge.yml")
git_commit("feat: add PR bot workflow")
git_push()
```

**Ez csak egyszer kell!** Ha már van workflow fájl, kihagyható.

---

#### 1.2. Agent létrehoz egy branch-et

```python
# Agent kód
branch_name = f"feat/agent-{int(time.time())}"  # pl. "feat/agent-1234567890"

# Branch létrehozása
git_checkout_new_branch(branch_name)
```

**Miért?**
- Nem commit-olhat közvetlenül a `main`-be (ha van protection)
- Minden agent saját branch-en dolgozik
- Több agent is dolgozhat egyszerre, nem ütköznek

---

#### 1.3. Agent commit-olja a változásait

```python
# Agent kód
# Tegyük fel, hogy az agent módosít egy fájlt
write_file("src/main.py", new_code)

# Commit
git_add("src/main.py")
git_commit("fix: resolve bug in main.py")
```

**Mit commit-ol az agent?**
- A saját változásait (kód, fájlok, stb.)
- **NEM** commit-olja a workflow fájlt újra (ha már létezik)

---

#### 1.4. Agent push-ol a branch-re

```python
# Agent kód
git_push(branch_name, set_upstream=True)
```

**Mit csinál?**
- Feltölti a branch-et a GitHub-ra
- A commit-ok most már láthatók a GitHub-on

---

#### 1.5. Agent létrehozza a PR-t

```python
# Agent kód
pr_number = gh_pr_create(
    title="Fix bug in main.py",
    body="This PR fixes the issue described in #123",
    head=branch_name,      # A branch, amit létrehozott
    base="main"            # Base branch (általában main)
)
```

**Mit csinál?**
- Létrehoz egy Pull Request-et
- `head` = az agent branch-je
- `base` = main (vagy más target branch)

---

#### 1.6. Agent hozzáadja az `automerge` labelt

```python
# Agent kód
gh_pr_edit(pr_number, add_label="automerge")
```

**Ez a kritikus lépés!**
- Ez triggereli a `labeled` event-et
- Ez indítja el a GitHub Action workflow-t

---

## 2. FÁZIS: GitHub Action Automatikusan Fut

### Mikor történik?

**AZONNAL** amikor az agent hozzáadja az `automerge` labelt!

### Lépésről Lépésre

#### 2.1. GitHub észleli a `labeled` event-et

```
GitHub szerver: "Egy PR-re hozzáadtak egy labelt!"
→ Megkeresi az összes workflow fájlt
→ Találja: .github/workflows/auto-merge.yml
→ Nézi: "Ez PR event-et figyel, és van 'labeled' type"
→ ELLENŐRZI: "Van 'automerge' label a PR-en?" → ✅ Igen!
```

#### 2.2. GitHub elindít egy virtuális gépet

```
→ Ubuntu Linux server
→ Tiszta környezet
→ Minden workflow futáskor új gép
```

#### 2.3. Checkout lépés

```yaml
- uses: actions/checkout@v4
```

**Mit csinál?**
- Letölti a repository kódját a virtuális gépre
- Checkout-olja a PR branch-et (vagy main-t, attól függ)

#### 2.4. PR Bot Action lépés

```yaml
- uses: tnedr/agent-ops/actions/pr-bot@main
```

**Mit csinál?**
- Letölti az `agent-ops` repo `actions/pr-bot/` mappáját
- Olvassa az `action.yml`-t
- Docker image-t épít és futtat
- A `pr_bot.py` script fut

#### 2.5. PR Bot merge-el

```python
# pr_bot.py script
pr_number = get_current_pr_number()  # Megtalálja a PR számot
time.sleep(5)  # Vár 5 másodpercet
gh_pr_merge(pr_number, method="squash", delete_branch=True)
```

**Mit csinál?**
- Squash merge-el (összevonja a commit-okat)
- Törli a source branch-et
- Kész!

---

## Teljes Idővonal Példa

### Több Agent Egyszerre

```
Idő: 10:00:00
Agent A: Branch létrehoz → feat/agent-A-123
Agent B: Branch létrehoz → feat/agent-B-456

Idő: 10:00:30
Agent A: Commit → "fix: bug A"
Agent B: Commit → "fix: bug B"

Idő: 10:01:00
Agent A: Push → feat/agent-A-123
Agent B: Push → feat/agent-B-456

Idő: 10:01:30
Agent A: PR létrehoz → PR #100
Agent B: PR létrehoz → PR #101

Idő: 10:02:00
Agent A: Label hozzáad → 'automerge' → PR #100
        → GitHub Action elindul PR #100-hez
        → 5 mp múlva merge-eli

Idő: 10:02:30
Agent B: Label hozzáad → 'automerge' → PR #101
        → GitHub Action elindul PR #101-hez
        → 5 mp múlva merge-eli

Idő: 10:02:05
PR #100 → Merged ✅
         → Branch feat/agent-A-123 törlődött

Idő: 10:02:35
PR #101 → Merged ✅
         → Branch feat/agent-B-456 törlődött
```

**Fontos:**
- Minden agent saját branch-en dolgozik
- Nem ütköznek
- Mindegyik PR külön merge-elődik

---

## Konkrét Agent Kód (Teljes Flow)

```python
class Agent:
    def process_task(self, task):
        """Agent teljes munkafolyamata"""
        
        # 1. WORKFLOW FÁJL (csak ha még nincs)
        if not self.workflow_exists():
            self.create_workflow_file()
            self.commit_and_push_workflow()
        
        # 2. BRANCH LÉTREHOZÁSA
        branch_name = f"feat/agent-{int(time.time())}"
        self.git_checkout_new_branch(branch_name)
        
        # 3. VÁLTOZÁSOK ELKÉSZÍTÉSE
        changes = self.make_changes(task)  # Agent dolga
        
        # 4. COMMIT
        for file, content in changes.items():
            write_file(file, content)
            git_add(file)
        
        commit_message = self.generate_commit_message(task)
        git_commit(commit_message)
        
        # 5. PUSH
        git_push(branch_name, set_upstream=True)
        
        # 6. PR LÉTREHOZÁSA
        pr_title = self.generate_pr_title(task)
        pr_body = self.generate_pr_body(task)
        
        pr_number = gh_pr_create(
            title=pr_title,
            body=pr_body,
            head=branch_name,
            base="main"
        )
        
        # 7. AUTOMERGE LABEL (ez triggereli a GitHub Action-t!)
        gh_pr_edit(pr_number, add_label="automerge")
        
        # 8. KÉSZ! A GitHub Action automatikusan merge-eli
        return pr_number
```

---

## Mikor Fut a GitHub Action?

### Trigger Események

```yaml
on:
  pull_request:
    types: [opened, synchronize, reopened, ready_for_review, labeled]
```

**Pontosabban:**

1. **`opened`** - PR létrehozva
   - **DE:** Csak akkor fut, ha már van `automerge` label!
   - Ha nincs label → workflow fut, de a `if:` condition kihagyja

2. **`synchronize`** - Új commit push-olva a PR branch-re
   - **DE:** Csak akkor fut, ha már van `automerge` label!

3. **`labeled`** - Label hozzáadva ← **EZ A LEGFONTOSABB!**
   - **MINDIG fut**, ha `automerge` label hozzáadódik
   - Ez a legbiztonságosabb trigger!

### Ajánlott Módszer

```python
# 1. PR létrehozása (label nélkül)
pr_number = gh_pr_create(...)

# 2. UTÁNNA label hozzáadása
gh_pr_edit(pr_number, add_label="automerge")
# → Ez triggereli a 'labeled' event-et
# → Workflow azonnal elindul
```

---

## Több Agent - Konfliktusok?

### Nem ütköznek, mert:

1. **Minden agent saját branch-en dolgozik**
   - `feat/agent-A-123`
   - `feat/agent-B-456`
   - `feat/agent-C-789`

2. **Minden agent saját PR-t hoz létre**
   - PR #100 (Agent A)
   - PR #101 (Agent B)
   - PR #102 (Agent C)

3. **Minden PR külön merge-elődik**
   - Sequential vagy parallel
   - GitHub kezeli a sorrendet

### Ha Konfliktus Van?

**Példa:**
- Agent A: Módosítja `main.py`-t
- Agent B: Módosítja ugyanazt a `main.py`-t
- Agent A merge-elődik először
- Agent B PR-je konfliktust mutat

**Megoldás:**
- Agent B PR-je nem merge-elődik automatikusan
- Konfliktust kell megoldani (manuálisan vagy agent újra dolgozik)

---

## Összefoglaló

### Agent Munkája:

1. ✅ Workflow fájl (egyszer, ha még nincs)
2. ✅ Branch létrehozása
3. ✅ Változások elkészítése
4. ✅ Commit
5. ✅ Push
6. ✅ PR létrehozása
7. ✅ `automerge` label hozzáadása ← **Ez triggereli a GitHub Action-t!**

### GitHub Action Munkája:

1. ✅ Észleli a `labeled` event-et
2. ✅ Ellenőrzi a feltételt (`automerge` label)
3. ✅ Elindít egy virtuális gépet
4. ✅ Futtatja a PR bot-ot
5. ✅ Merge-el (squash)
6. ✅ Törli a branch-et

### Több Agent:

- ✅ Minden agent saját branch-en dolgozik
- ✅ Minden agent saját PR-t hoz létre
- ✅ Nem ütköznek (hacsak nem ugyanazt a fájlt módosítják)
- ✅ Mindegyik PR külön merge-elődik

