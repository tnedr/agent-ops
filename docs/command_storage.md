### Két lehetséges “központi” tárolási forma az **ügynök-parancskészlet** ( `agt` ) számára

|                        | **Tools-repo (submodule / pip / git clone)**                                                                                                                                                                                                  | **Reusable GitHub Action (`uses: org/dev-automation/agt@v1`)**                                                                                                                                                                                                           |
| ---------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Hol fut?**           | Fejlesztői gép / Cursor terminál (lokál)                                                                                                                                                                                                      | GitHub Actions runner (felhő)                                                                                                                                                                                                                                            |
| **Előnyök**            | • Ügynök azonnal hívhatja offline<br>• Worktree-izoláció és commit gyors, hálózat nélkül is<br>• Cursorban teljes kontroll (debug, break-point, IDE-integration)<br>• Egy parancssor → ugyanúgy megy WSL-ben, Windows PowerShellben, macOS-en | • Nincs szükség fejlesztői Git/CLI tokenre → GitHub Actions saját `GITHUB_TOKEN`-nel mergel<br>• Branch-protection, audit, RBAC könnyen ráhúzható (minden merge CI-ből jön)<br>• Cache-elt runner → nagy repo-k check-outja gyors<br>• Egységes, infra-központú pipeline |
| **Hátrányok**          | • Fejlesztő gépén GitHub CLI-nak ír-jog kell a repo-hoz<br>• Ha policy tiltja a lokális merge-t, nem engedhető production-be<br>• Multi-OS kompatibilitást neked kell megírni a scriptbe (PS/Bash)                                            | • Nem tud a runner “kódot generálni” IDE-ben élőben; az ügynöknek fájlt kell push-olnia és várnia a CI-re<br>• CI-kör lefutási ideje (queue + checkout) lassabb lehet, mint lokális CLI<br>• Lokális offline fejlesztéshez nem használható                               |
| **Tipikus use-case**   | • **AI-asszisztált fejlesztés Cursor alatt**<br>• Gyors prototípus: ügynökök gyakran írják-futtatják a kódot<br>• Belső hálózaton, ahol a GitHub Actions nem érhető el                                                                        | • **Enterprise / compliance**: csak CI merge-elhet main-be<br>• Monorepók, ahol minden PR-nek végig kell futnia teljes CI-csővezetéken<br>• Ha ügynök futása is Actions-ben történik (teljesen headless)                                                                 |
| **Verzió-frissítés**   | • Submodule → `git submodule update --remote`<br>• Pip-csomag → `uv pip install -U agent-tools`                                                                                                                                               | • Release tag → csak `@v1`-et kell frissíteni új tagre<br>• Workflow-fájl minden repóban ugyanaz marad                                                                                                                                                                   |
| **Bevezetési lépések** | 1. Tools-repo létrehozás<br>2. Célrepo-ba `git submodule add … .tools`<br>3. `PATH`-be felvenni `.tools/agt`-et *vagy* `python .tools/agent_tools/...` import                                                                                 | 1. Tools-repo-ban `agent-runner` Action + release tag<br>2. Célrepo-ban workflow: <br>`yaml<br>- uses: org/dev-automation/agt@v1<br>  with: {cmd: "...", msg: "..."}<br>`                                                                                                |

---

## Mikor melyiket javaslom?

| Szenárió                                                                   | Javasolt megoldás                                                                                                                                            |
| -------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Iteratív, szem-közti AI-kódolás Cursorban** (fejlesztőnél fut az ügynök) | **Tools-repo + `agt` CLI** – gyors, offline, IDE-barát                                                                                                       |
| **Prod / compliance: branch-protection, audit trail, kötelező CI**         | **Reusable GitHub Action** – minden merge a GitHub infrastruktúrából érkezik                                                                                 |
| **Vegyes** (prototípus helyben, később prod-CI)                            | Tartsd a scriptet a tools-repo-ban *és* csomagold be composite Action-be is: lokálban `agt`, CI-ben `uses:` – ugyanazt a Python-kódot futtatja mindkét oldal |

Így könnyen váltogathatsz: a motor egy helyen él, de elérhető lokális CLI-ként **és** GitHub Actionként is.


Alap szcenárióban két központi megoldást vázoltunk ( **tools-repo** & **reusable GitHub Action** ).
Íme **még két** gyakori minta, összesen tehát **négy** jól bevált út:

| #     | Forma                                   | Hogyan hívod?                     | Mikor jó?                                 | Előny                                      | Hátrány                           |
| ----- | --------------------------------------- | --------------------------------- | ----------------------------------------- | ------------------------------------------ | --------------------------------- |
| **1** | **Tools-repo (submodule / clone)**      | `tools/agt start …`               | IDE-/Cursor-fókuszú lokál fejlesztés      | • Offline • Gyors                          | • Frissítést kézzel húzod be      |
| **2** | **Reusable GitHub Action**              | `uses: org/dev-automation/agt@v1` | Prod CI, audit, RBAC                      | • Branch-védelem, napló                    | • Runner-késleltetés, nem offline |
| **3** | **Telepíthető CLI-csomag** (PyPI / npm) | `pipx run agt …` v. `npx agt …`   | Vegyes nyelvű csapat, ügynökök több gépen | • Egy sorral telepíthető • Verziózva       | • Frissítés = `pipx upgrade …`    |
| **4** | **Docker / Dev-container CLI**          | `docker run ghcr.io/org/agt:1 …`  | OS-független sandbox, build-farm          | • Null telepítés • Mindig azonos környezet | • Lassabb indítás • Kell Docker   |

### Gyors döntési matrica

| Igény                                                               | Válassz              |
| ------------------------------------------------------------------- | -------------------- |
| **Cursor-ban kódolok, internet nélkül is menjen**                   | **#1 Tools-repo**    |
| **Prod-merge csak CI-n át, audit kell**                             | **#2 GitHub Action** |
| **Sok gép / több nyelv, szeretem az `pipx` vagy `npm -g` módszert** | **#3 CLI-csomag**    |
| **Nem akarok semmit telepíteni a hostra, OS-agnosztikusan futnék**  | **#4 Docker-CLI**    |

Mindegyik ugyanazt a “motor-kódot” futtathatja (pl. a `git worktree` + `pr_bot.py` wrappert); csak más csomagolás, más életciklus-kezelés. Ha kell, szívesen kidolgozom bármelyik konkrét lépéseit.


---------------

Tools-repo beemelése submodule-ként
bash<br>git submodule add -b main https://github.com/<ORG>/agent-tools .tools<br>git commit -m "chore: add agent-tools submodule"<br>
A .tools/ mappában jelenik meg az agt script és minden közös helper.

--------
## Két megoldás, egy cél

* **Jelenlegi modell** – külső repo kézi klónja, abszolút/relatív path-hivatkozás a VS Code tasks-ban
* **Új modell** – ugyanaz a repo **Git submodule-ként** behúzva (pl. `.tools/agent-tools`)

|                              | **Kézi klón & path-hivatkozás**                                                            | **Git submodule (.tools/)**                                                   |
| ---------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------------- |
| **Telepítés**                | Fejlesztő külön `git clone …` <br>- VS Code-ban abszolút vagy - néha törékeny - relatív út | `git submodule add https://… .tools`  (egyszer)                               |
| **Verzió-rögzítés**          | Nincs; mindenki épp a saját branch/commitján van                                           | Szülőrepo commitja *pointert* tárol → reprodukálható                          |
| **Frissítés**                | Minden fejlesztő saját maga `git pull` + path-játír, CI-be külön lépés kell                | `git submodule update --remote --merge .tools` + 1 commit                     |
| **Új klón**                  | README-ben: „klónozd le még a tools repót ide-meg-ide”                                     | `git clone … && git submodule update --init --recursive` – mindent egyben kap |
| **VS Code útvonal**          | Gépfüggő (pl. `../agent-tools/agt`) – ha a klón mappa más, a task elromlik                 | Stabil: `${workspaceFolder}/.tools/agt` (mindenkinél ugyanott)                |
| **CI checkout**              | Külön `actions/checkout` a tools-repo-hoz v. extra `curl`                                  | Fő `checkout` hozza a submodule-t ( `submodules: recursive`)                  |
| **Jogosultság / review**     | Fejlesztő a projektben is átírhatja a tools-kódot                                          | Tools-repo saját PR-folyamattal védhető; projekt csak pointert frissít        |
| **Kód-szinkron**             | Könnyen eltér a tools-API és a projekt-task                                                | Minden gép, CI, ügynök *ugyanarra* a commitra épül                            |
| **Összetett repo-struktúra** | Két külön sibling-mappa a fában                                                            | Minden modul a projektfa alatt → IDE-workspace egyszerűbb                     |

### Mikor maradhat a kézi klón?

* Egyetlen fejlesztő / prototípus
* Offline, sosem fut CI-n, nem kell auditálható verzió

### Mikor lépj át submodule-ra?

* Több fejlesztő / több AI-ügynök használja ugyanazt a parancskészletet
* CI-pipeline fut (branch-védelem, audit)
* Szeretnéd, hogy minden munkaállomáson és runneren **ugyanaz** a tools-commit fusson
* Stabil VS Code-task-útvonalat akarsz telepítés nélkül

**Bottom line:** a submodule egy *pointert* ment a projekt-történetbe → garantáltan ugyanazt a tools-verziót kapja fejlesztő, ügynök és CI is, frissíteni pedig egyetlen parancs és commit.
