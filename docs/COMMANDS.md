# AGT CLI – Parancs-referencia (v0.3)

## Alapstruktúra

```bash
agt <domain> <action> [args...]
```

## Domain-ok

| Domain | Action(ök) | Rövid leírás |
|--------|-----------|--------------|
| `ws` | `new`, `run`, `save`, `push`, `merge`, `clean` | Git-worktree műveletek |
| `task` | `list`, `add`, `pick`, `done` | 🟡 Preview – feladatkezelés (jövőbeli fejlesztés) |
| `cfg` | `vscode` | VS Code Command Runner beállítás generálása |
| `env` | `check`, `python` | Környezet-diagnosztika |

## Aliasok (v0.2-ről)

A régi egy-szavas parancsok továbbra is működnek, de deprecated státuszban vannak. v0.4-től eltávolítjuk.

| Régi parancs | Új parancs |
|-------------|-----------|
| `agt start` | `agt ws new` |
| `agt commit` | `agt ws save` |
| `agt run` | `agt ws run` |
| `agt push` | `agt ws push` |
| `agt merge` | `agt ws merge` |
| `agt clean` | `agt ws clean` |
| `agt vscode init` | `agt cfg vscode` |

## Gyorspélda – teljes workflow

```bash
agt ws new                         # 1. izolált munka
agt ws run "pytest -q"             # 2. teszt
agt ws save "feat: tests"          # 3. commit
agt ws push                        # 4. push
agt cfg vscode                     # 5. VS Code integráció
agt ws clean                       # 6. takarítás
```

## Workspace (ws) parancsok

### `agt ws new [base-branch]`

Új agent worktree létrehozása.

```bash
agt ws new              # main branch alapján
agt ws new develop      # develop branch alapján
```

### `agt ws run <command> [--agent <id>]`

Parancs futtatása az agent worktree-ben.

```bash
agt ws run "pytest -q"
agt ws run "python script.py arg1 arg2"
agt ws run --agent agent-123 "pytest"
```

### `agt ws save "<message>" [--agent <id>]`

Változások commitolása az agent worktree-ben.

```bash
agt ws save "feat: add new feature"
agt ws save --agent agent-123 "fix: bug fix"
```

### `agt ws push [remote] [--agent <id>]`

Branch push-olása a remote repository-ba.

```bash
agt ws push
agt ws push origin
agt ws push --agent agent-123
```

### `agt ws merge [--agent <id>]`

Agent branch fast-forward merge-je a main branch-be.

```bash
agt ws merge
agt ws merge --agent agent-123
```

### `agt ws clean [--agent <id>]`

Agent worktree eltávolítása.

```bash
agt ws clean
agt ws clean --agent agent-123
```

## Task modul (Preview)

A task modul jelenleg preview státuszban van, funkcionalitás még nincs implementálva. A parancsnevek lefoglalva vannak a jövőbeli fejlesztéshez.

### `agt task list [--status STATUS]`

🟡 Preview – Feladatok listázása (még nincs implementálva)

### `agt task add <id> <description>`

🟡 Preview – Új feladat hozzáadása (még nincs implementálva)

### `agt task pick <id> [--agent AGENT_ID]`

🟡 Preview – Feladat kiválasztása (még nincs implementálva)

### `agt task done <id>`

🟡 Preview – Feladat befejezése (még nincs implementálva)

## Config (cfg) parancsok

### `agt cfg vscode`

VS Code Command Runner beállítások generálása a projekt `.vscode/settings.json` fájlban.

```bash
agt cfg vscode
```

Ez a parancs létrehozza vagy frissíti a `.vscode/settings.json` fájlt az `agt` parancsokkal.

## Environment (env) parancsok

### `agt env check`

Környezet-információk megjelenítése.

```bash
agt env check
```

### `agt env python <script> [args...]`

Python script futtatása a rendszer Python-jával.

```bash
agt env python script.py arg1 arg2
```

## Deprecated parancsok

A következő parancsok v0.3-ban még működnek, de DeprecationWarning-et adnak. v0.4-től eltávolítjuk:

- `agt start` → `agt ws new`
- `agt commit` → `agt ws save`
- `agt run` → `agt ws run`
- `agt push` → `agt ws push`
- `agt merge` → `agt ws merge`
- `agt clean` → `agt ws clean`
- `agt vscode init` → `agt cfg vscode`


