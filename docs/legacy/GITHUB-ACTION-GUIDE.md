# GitHub Action Módszer - Részletes Útmutató

## Mi az a GitHub Action?

A GitHub Action egy **automatizált workflow**, ami a GitHub repository-ban fut, amikor bizonyos események történnek (pl. PR létrehozva, commit push-olva).

**Kulcsfontosságú:** A GitHub Action **nem egy script, amit futtatunk**, hanem egy **konfigurációs fájl**, amit a repository-ban tárolunk, és a GitHub automatikusan végrehajtja.

---

## Hogyan működik?

### 1. Workflow Fájl Létrehozása

A workflow fájl egy **YAML fájl**, ami leírja, hogy mit kell csinálni.

**Helye:** `.github/workflows/auto-merge.yml`

**Miért itt?**
- A `.github/workflows/` mappa speciális - a GitHub automatikusan felismeri
- Itt lehet több workflow fájl is (pl. `test.yml`, `deploy.yml`, stb.)

### 2. A Workflow Fájl Struktúra

```yaml
name: Auto-merge PR                    # Workflow neve (látható az Actions tab-ban)

on:                                     # MIKOR fusson?
  pull_request:                         # PR eseményekre
    types: [labeled]                    # Pontosan: label hozzáadásakor

jobs:                                   # MIT csináljon?
  merge:                                # Job neve (bármi lehet)
    if: contains(...)                   # FELTÉTEL: csak akkor, ha...
    runs-on: ubuntu-latest              # HOL fusson? (Linux server)
    steps:                              # LÉPÉSEK
      - uses: actions/checkout@v4       # 1. Checkout a kódot
      - uses: tnedr/agent-ops/...       # 2. Futtasd a PR bot-ot
```

---

## Részletes Végigmegyünk Egy Példán

### Teljes Workflow Fájl

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

### Soronkénti Magyarázat

#### 1. `name: Auto-merge PR`
- Ez a workflow neve
- Látható lesz a GitHub Actions tab-ban
- Tetszőleges lehet

#### 2. `on: pull_request:`
- **"Mikor fusson?"**
- `pull_request` = PR eseményekre figyel
- Más lehetőségek: `push`, `workflow_dispatch`, `schedule`, stb.

#### 3. `types: [opened, synchronize, reopened, ready_for_review, labeled]`
- **Pontosan melyik PR eseményekre?**
- `opened` - PR létrehozva
- `synchronize` - Új commit push-olva a PR branch-re
- `reopened` - Zárt PR újra megnyitva
- `ready_for_review` - Draft PR ready-re állítva
- `labeled` - **Label hozzáadva** (ez a legfontosabb!)

#### 4. `jobs: merge:`
- **"Mit csináljon?"**
- `jobs` = feladatok/munkák
- `merge` = ennek a job-nak a neve (bármi lehet)

#### 5. `if: contains(github.event.pull_request.labels.*.name, 'automerge')`
- **FELTÉTEL: csak akkor fusson, ha...**
- `github.event` = az aktuális esemény adatai
- `pull_request.labels` = a PR label-jei
- `.*.name` = minden label neve
- `contains(..., 'automerge')` = tartalmazza-e az 'automerge' labelt?

**Tehát:** Csak akkor fut, ha a PR-en van `automerge` label!

#### 6. `runs-on: ubuntu-latest`
- **Hol fusson?**
- GitHub futtat egy Linux virtuális gépet
- Ez a gépen fut le minden

#### 7. `steps:`
- **Lépések sorrendben**
- Minden `-` egy lépés

#### 8. `- uses: actions/checkout@v4`
- **Első lépés:** Checkout a repository kódját
- `actions/checkout@v4` = egy előre kész action
- Ez szükséges, hogy a kód elérhető legyen

#### 9. `- name: Auto-merge with PR-bot`
- **Második lépés neve**
- Csak log-ban látható, tetszőleges

#### 10. `uses: tnedr/agent-ops/actions/pr-bot@main`
- **Itt hívódik meg a PR bot!**
- `tnedr/agent-ops` = GitHub repo (owner/repo)
- `actions/pr-bot` = az action mappája
- `@main` = branch (vagy tag, pl. `@v1`)

**Ez mi?**
- A GitHub letölti az `agent-ops` repo `actions/pr-bot/` mappáját
- Megkeresi az `action.yml` fájlt
- Az `action.yml` leírja, hogy mit kell csinálni (Docker image futtatása)
- Elindítja a Docker konténert, ami futtatja a `pr_bot.py` scriptet

#### 11. `with: ci: "false"`
- **Input paraméterek**
- Ezeket kapja meg az action
- `ci: "false"` = ne várjon CI check-ekre

#### 12. `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`
- **Environment változó**
- `GITHUB_TOKEN` = automatikusan generált token
- A bot ezzel autentikál a GitHub API-hoz

---

## Hogyan Működik a Teljes Folyamat?

### Lépésről Lépésre

1. **Agent létrehozza a workflow fájlt**
   ```
   .github/workflows/auto-merge.yml
   ```
   - Commit-olja és push-olja

2. **Agent létrehoz egy PR-t**
   - Vagy egy már létező PR-t használ

3. **Agent hozzáadja az `automerge` labelt**
   ```bash
   gh pr edit 123 --add-label automerge
   ```
   - Ez triggereli a `labeled` event-et

4. **GitHub észleli az eseményt**
   - Látja, hogy van egy PR `labeled` event
   - Megkeresi a workflow fájlokat
   - Találja az `auto-merge.yml`-t

5. **GitHub ellenőrzi a feltételt**
   - `if: contains(...)` - van `automerge` label? → Igen!
   - A job elindul

6. **GitHub futtat egy virtuális gépet**
   - Ubuntu Linux
   - Tiszta környezet

7. **Checkout lépés**
   - `actions/checkout@v4` letölti a repository kódját

8. **PR Bot Action lépés**
   - GitHub letölti az `agent-ops/actions/pr-bot` action-t
   - Elolvassa az `action.yml`-t
   - Az `action.yml` azt mondja: "Futtasd ezt a Docker image-t"
   - A Docker image tartalmazza a `pr_bot.py` scriptet
   - A script fut, és merge-eli a PR-t

9. **Kész!**
   - PR merge-elődött
   - Branch törlődött

---

## Az `action.yml` Fájl - Mit Csinál?

Az `actions/pr-bot/action.yml` fájl:

```yaml
name: "PR Bot – auto-merge"
description: "Squash-merge PR, opcionálisan csak zöld CI után"

inputs:
  ci:
    description: "Várjon-e zöld check-ekre (true/false)"
    required: false
    default: "false"
  force:
    description: "Admin override – piros check esetén is merge"
    required: false
    default: "false"

runs:
  using: "docker"
  image: "Dockerfile"
  env:
    INPUT_CI: ${{ inputs.ci }}
    INPUT_FORCE: ${{ inputs.force }}
```

**Mit jelent ez?**

1. **`inputs:`** - Milyen paramétereket fogad?
   - `ci` és `force` string-ek

2. **`runs: using: "docker"`** - Docker konténerben fut
   - A `Dockerfile` leírja a konténert

3. **`env:`** - Environment változók
   - A `with:` paraméterekből jönnek

**Folyamat:**
1. Workflow: `with: ci: "false"`
2. Action: `INPUT_CI: ${{ inputs.ci }}` → `INPUT_CI="false"`
3. Docker: `entrypoint.sh` olvassa `INPUT_CI`-t
4. Script: `python pr_bot.py --ci` (ha true)

---

## Mi a Különbség a Régi Módszertől?

### Régi (CLI):

```bash
# Agent futtatja közvetlenül
python pr_bot.py --message "fix" --title "Fix" --ci
```

**Mit csinál?**
- Az agent gépen fut
- Létrehozza a branch-et, commit-ol, push-ol, PR-t nyit, merge-el

### Új (GitHub Action):

```yaml
# Workflow fájl a repo-ban
uses: tnedr/agent-ops/actions/pr-bot@main
```

**Mit csinál?**
- GitHub szerveren fut
- A PR már létezik (a workflow PR event-re fut)
- Csak merge-el (nem hoz létre PR-t)

---

## Konkrét Példa: Agent Kód (Teljes Flow)

### Mit kell az agentnek csinálnia?

**FONTOS:** Az agent először dolgozik (branch, commit, PR), UTÁNNA triggereli a GitHub Action-t!

```python
# 1. WORKFLOW FÁJL LÉTREHOZÁSA (csak első alkalommal, ha még nincs)
if not workflow_exists():
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
      - uses: tnedr/agent-ops/actions/pr-bot@main
        with:
          ci: "false"
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
"""
    write_file(".github/workflows/auto-merge.yml", workflow_content)
    git_add(".github/workflows/auto-merge.yml")
    git_commit("feat: add PR bot auto-merge workflow")
    git_push()

# 2. BRANCH LÉTREHOZÁSA (minden feladathoz)
branch_name = f"feat/agent-{int(time.time())}"  # pl. "feat/agent-1234567890"
git_checkout_new_branch(branch_name)

# 3. VÁLTOZÁSOK ELKÉSZÍTÉSE (agent dolga)
write_file("src/main.py", new_code)  # Agent módosít fájlokat
git_add("src/main.py")

# 4. COMMIT
git_commit("fix: resolve bug in main.py")

# 5. PUSH
git_push(branch_name, set_upstream=True)

# 6. PR LÉTREHOZÁSA
pr_number = create_pr(
    title="Fix bug",
    body="This fixes the issue",
    head=branch_name,  # Az agent branch-je
    base="main"       # Target branch
)

# 7. AUTOMERGE LABEL Hozzáadása (ez triggereli a GitHub Action-t!)
add_label_to_pr(pr_number, "automerge")

# Kész! A GitHub automatikusan futtatja a workflow-t
# → 5 másodperc múlva merge-elődik
```

**Lépések sorrendje:**
1. Branch létrehozása
2. Változások (commit)
3. Push
4. PR létrehozása
5. **Label hozzáadása** → Ez triggereli a GitHub Action-t!

---

## Vizuális Diagram

```
┌─────────────────────────────────────────────────────────┐
│ 1. Agent létrehozza a workflow fájlt                    │
│    .github/workflows/auto-merge.yml                     │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Agent commit-ol és push-ol                          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 3. Agent létrehoz egy PR-t (vagy használ egy meglévőt) │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 4. Agent hozzáadja az 'automerge' labelt                │
│    gh pr edit 123 --add-label automerge                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 5. GitHub észleli: "labeled" event!                     │
│    → Megkeresi a workflow fájlokat                      │
│    → Találja: .github/workflows/auto-merge.yml          │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 6. GitHub ellenőrzi a feltételt                         │
│    if: contains(labels, 'automerge') → ✅ Igen!         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 7. GitHub elindít egy Ubuntu virtuális gépet           │
│    runs-on: ubuntu-latest                                │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 8. Checkout lépés                                       │
│    uses: actions/checkout@v4                            │
│    → Letölti a repository kódját                         │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 9. PR Bot Action lépés                                  │
│    uses: tnedr/agent-ops/actions/pr-bot@main            │
│    → Letölti az action-t                                │
│    → Olvassa az action.yml-t                             │
│    → Dockerfile alapján épít egy image-t                │
│    → Futtatja a konténert                               │
│    → A konténer futtatja a pr_bot.py-t                  │
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 10. pr_bot.py fut                                       │
│     → Felismeri a PR számot (GITHUB_EVENT_PATH)         │
│     → Vár 5 másodpercet                                 │
│     → Merge-el: gh pr merge 123 --squash --delete-branch│
└────────────────┬────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────┐
│ 11. Kész! PR merge-elődött, branch törlődött           │
└─────────────────────────────────────────────────────────┘
```

---

## Fontos Kérdések

### Miért kell az `automerge` label?

**Válasz:** Infinite loop megelőzésére!

Ha nincs label feltétel:
1. PR létrejön → Workflow fut
2. Bot merge-el → Ez triggerel új PR event-et
3. Workflow újra fut → Végtelen loop!

Label feltétellel:
1. PR létrejön (nincs label) → Workflow nem fut
2. Label hozzáadva → Workflow fut
3. Bot merge-el → Nincs label az új commit-on → Workflow nem fut újra ✅

### Mi a különbség a `uses:` és `run:` között?

**`uses:`** = Másik action-t vagy workflow-t hív meg
```yaml
uses: tnedr/agent-ops/actions/pr-bot@main  # Másik action
uses: actions/checkout@v4                   # GitHub action
```

**`run:`** = Közvetlenül parancsot futtat
```yaml
run: echo "Hello"  # Shell parancs
run: |
  echo "Hello"
  echo "World"
```

### Mi az `${{ }}` syntax?

**GitHub Actions expression syntax**

- `${{ secrets.GITHUB_TOKEN }}` - Secret érték
- `${{ inputs.ci }}` - Input paraméter
- `${{ github.event.pull_request.number }}` - Event adatok

### Miért `@main` és nem `@v1`?

**`@main`** = Mindig a legfrissebb kód (instabil lehet)
**`@v1`** = Verzió tag (stabil, ajánlott production-hez)

Verzió tag létrehozása:
```bash
git tag v1
git push origin v1
```

Aztán használd:
```yaml
uses: tnedr/agent-ops/actions/pr-bot@v1
```

---

## Összefoglaló

1. **Workflow fájl** = Konfiguráció, amit a repo-ban tárolunk
2. **Trigger** = PR események (`labeled` a legfontosabb)
3. **Feltétel** = `automerge` label kell
4. **Action** = Másik repo-ból hívható automatizálás
5. **Folyamat** = GitHub automatikusan végrehajtja

**Agent feladata:**
- Workflow fájl létrehozása (egyszer)
- PR létrehozása
- `automerge` label hozzáadása
- Kész! A GitHub megcsinálja a többit

