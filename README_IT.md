<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">简体中�?/a> |
  <a href="README_TW.md">繁體中文</a> |
  <a href="README_JA.md">日本�?/a> |
  <a href="README_KO.md">한국�?/a> |
  <a href="README_FR.md">Français</a> |
  <a href="README_ES.md">Español</a> |
  <a href="README_DE.md">Deutsch</a> |
  <a href="README_IT.md">Italiano</a> |
  <a href="README_RU.md">Русский</a> |
  <a href="README_PT-BR.md">Português (Brasil)</a>
</p>

<h1 align="center">🦞AgentTeam-OpenClaw</h1>

<p align="center">
  <strong>Coordinamento multi-agente a sciame per agenti di codifica CLI �?<a href="https://openclaw.ai">OpenClaw</a> come predefinito</strong>
</p>

<p align="center">
  <a href="https://github.com/HKUDS/AgentTeam"><img src="https://img.shields.io/badge/upstream-HKUDS%2FAgentTeam-purple?style=for-the-badge" alt="Upstream"></a>
  <a href="#-avvio-rapido"><img src="https://img.shields.io/badge/Quick_Start-3_min-blue?style=for-the-badge" alt="Avvio Rapido"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="Licenza"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-�?.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/agents-OpenClaw_%7C_Claude_Code_%7C_Codex_%7C_nanobot-blueviolet" alt="Agenti">
  <img src="https://img.shields.io/badge/transport-File_%7C_ZeroMQ_P2P-orange" alt="Trasporto">
  <img src="https://img.shields.io/badge/version-0.3.0-teal" alt="Versione">
</p>

> **Fork di [HKUDS/AgentTeam](https://github.com/HKUDS/AgentTeam)** con integrazione profonda di OpenClaw: agente `openclaw` predefinito, isolamento sessione per agente, configurazione automatica delle approvazioni di esecuzione e backend di spawn pronti per la produzione. Tutte le correzioni upstream vengono sincronizzate.

Tu definisci l'obiettivo. Lo sciame di agenti gestisce il resto: genera i worker, suddivide le attività, coordina e unisce i risultati.

Funziona con [OpenClaw](https://openclaw.ai) (predefinito), [Claude Code](https://claude.ai/claude-code), [Codex](https://openai.com/codex), [nanobot](https://github.com/HKUDS/nanobot), [Cursor](https://cursor.com) e qualsiasi agente CLI.

---

## Perché AgentTeam?

Gli attuali agenti IA sono potenti ma lavorano in modo **isolato**. AgentTeam permette agli agenti di auto-organizzarsi in team: suddividere il lavoro, comunicare e convergere sui risultati senza microgestione umana.

| | AgentTeam | Altri framework multi-agente |
|---|---------|----------------------------|
| **Chi lo usa** | Gli agenti IA stessi | Umani che scrivono codice di orchestrazione |
| **Configurazione** | `pip install` + un prompt | Docker, API cloud, configurazioni YAML |
| **Infrastruttura** | Filesystem + tmux | Redis, code di messaggi, database |
| **Supporto agenti** | Qualsiasi agente CLI | Solo specifici del framework |
| **Isolamento** | Git worktree (branch reali) | Container o ambienti virtuali |

---

## Come funziona

<table>
<tr>
<td width="33%">

### Gli agenti generano agenti
Il leader chiama `agentteam spawn` per creare i worker. Ciascuno ottiene il proprio **git worktree**, la propria **finestra tmux** e la propria **identità**.

```bash
agentteam spawn --team my-team \
  --agent-name worker1 \
  --task "Implement auth module"
```

</td>
<td width="33%">

### Gli agenti comunicano tra loro
I worker controllano le caselle di posta, aggiornano le attività e riportano i risultati, il tutto tramite comandi CLI **auto-iniettati** nel loro prompt.

```bash
agentteam task list my-team --owner me
agentteam inbox send my-team leader \
  "Auth done. All tests passing."
```

</td>
<td width="33%">

### Tu osservi e basta
Monitora lo sciame da una vista tmux affiancata o dalla Web UI. Il leader gestisce il coordinamento.

```bash
agentteam board attach my-team
# Or web dashboard
agentteam board serve --port 8080
```

</td>
</tr>
</table>

---

## Avvio rapido

### Opzione 1: Lascia guidare l'agente (consigliato)

Installa AgentTeam, poi dai il prompt al tuo agente:

```
"Build a web app. Use agentteam to split the work across multiple agents."
```

L'agente crea automaticamente un team, genera i worker, assegna le attività e coordina il tutto tramite la CLI `agentteam`.

### Opzione 2: Gestisci manualmente

```bash
# Create a team
agentteam team spawn-team my-team -d "Build the auth module" -n leader

# Spawn workers �?each gets a git worktree + tmux window
agentteam spawn --team my-team --agent-name alice --task "Implement OAuth2 flow"
agentteam spawn --team my-team --agent-name bob   --task "Write unit tests for auth"

# Watch them work
agentteam board attach my-team
```

### Agenti supportati

| Agente | Comando di spawn | Stato |
|-------|--------------|--------|
| [OpenClaw](https://openclaw.ai) | `agentteam spawn tmux openclaw --team ...` | **Predefinito** |
| [Claude Code](https://claude.ai/claude-code) | `agentteam spawn tmux claude --team ...` | Supporto completo |
| [Codex](https://openai.com/codex) | `agentteam spawn tmux codex --team ...` | Supporto completo |
| [nanobot](https://github.com/HKUDS/nanobot) | `agentteam spawn tmux nanobot --team ...` | Supporto completo |
| [Cursor](https://cursor.com) | `agentteam spawn subprocess cursor --team ...` | Sperimentale |
| Script personalizzati | `agentteam spawn subprocess python --team ...` | Supporto completo |

---

## Installazione

### Passo 1: Prerequisiti

AgentTeam richiede **Python 3.10+**, **tmux** e almeno un agente di codifica CLI (OpenClaw, Claude Code, Codex, ecc.).

**Verifica cosa hai già installato:**

```bash
python3 --version   # Need 3.10+
tmux -V             # Need any version
openclaw --version  # Or: claude --version / codex --version
```

**Installa i prerequisiti mancanti:**

| Strumento | macOS | Ubuntu/Debian |
|------|-------|---------------|
| Python 3.10+ | `brew install python@3.12` | `sudo apt update && sudo apt install python3 python3-pip` |
| tmux | `brew install tmux` | `sudo apt install tmux` |
| OpenClaw | `pip install openclaw` | `pip install openclaw` |

> Se usi Claude Code o Codex al posto di OpenClaw, installali secondo la loro documentazione. OpenClaw è l'agente predefinito ma non strettamente obbligatorio.

### Passo 2: Installa AgentTeam

> **⚠️ NON eseguire `pip install agentteam` o `npm install -g agentteam` direttamente:**
> - `pip install agentteam` installa la versione upstream da PyPI, che usa `claude` come predefinito e non include gli adattamenti OpenClaw.
> - `npm install -g agentteam` installa un pacchetto usurpatore non correlato (pubblicato da `a9logic`). Se `agentteam --version` mostra "Coming Soon", è il pacchetto sbagliato. Esegui prima `npm uninstall -g agentteam`.
>
> **Usa i tre comandi qui sotto �?`pip install -e .` dopo il clone è obbligatorio. Installa dal repository locale, non da PyPI.**

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
pip install -e .    # �?Obbligatorio! Installa dal repository locale, NON uguale a pip install agentteam
```

Opzionale �?Trasporto P2P (ZeroMQ):

```bash
pip install -e ".[p2p]"
```

### Passo 3: Crea il collegamento simbolico `~/bin/AgentTeam`

Gli agenti generati vengono eseguiti in shell nuove che potrebbero non avere la directory bin di pip nel PATH. Un collegamento simbolico in `~/bin` assicura che `agentteam` sia sempre raggiungibile:

```bash
mkdir -p ~/bin
ln -sf "$(which agentteam)" ~/bin/AgentTeam
```

Se `which agentteam` non restituisce nulla, trova il binario manualmente:

```bash
# Common locations:
# ~/.local/bin/AgentTeam
# /opt/homebrew/bin/AgentTeam
# /usr/local/bin/AgentTeam
# /Library/Frameworks/Python.framework/Versions/3.*/bin/AgentTeam
find / -name agentteam -type f 2>/dev/null | head -5
```

Poi assicurati che `~/bin` sia nel tuo PATH �?aggiungi questa riga al tuo `~/.zshrc` o `~/.bashrc` se non c'è già:

```bash
export PATH="$HOME/bin:$PATH"
```

### Passo 4: Installa la skill OpenClaw (solo per utenti OpenClaw)

Il file skill insegna agli agenti OpenClaw come usare AgentTeam tramite linguaggio naturale. Salta questo passo se non usi OpenClaw.

```bash
mkdir -p ~/.openclaw/workspace/skills/AgentTeam
cp skills/openclaw/SKILL.md ~/.openclaw/workspace/skills/AgentTeam/SKILL.md
```

### Passo 5: Configura le approvazioni di esecuzione (solo per utenti OpenClaw)

Gli agenti OpenClaw generati necessitano del permesso per eseguire i comandi `agentteam`. Senza questo, gli agenti si bloccheranno sui prompt di autorizzazione interattivi.

```bash
# Ensure security mode is "allowlist" (not "full")
python3 -c "
import json, pathlib
p = pathlib.Path.home() / '.openclaw' / 'exec-approvals.json'
if p.exists():
    d = json.loads(p.read_text())
    d.setdefault('defaults', {})['security'] = 'allowlist'
    p.write_text(json.dumps(d, indent=2))
    print('exec-approvals.json updated: security = allowlist')
else:
    print('exec-approvals.json not found �?run openclaw once first, then re-run this step')
"

# Add agentteam to the allowlist (use the absolute path �?OpenClaw 4.2+ requires it)
openclaw approvals allowlist add --agent "*" "$(which agentteam)"
```

> Se `openclaw approvals` fallisce, il gateway OpenClaw potrebbe non essere in esecuzione. Avvialo prima, poi riprova.

### Passo 6: Verifica

```bash
agentteam --version          # Should print version
agentteam config health      # Should show all green
```

Se usi OpenClaw, verifica anche che la skill sia caricata:

```bash
openclaw skills list | grep agentteam
```

### Installatore automatico

I passi 2-6 sopra indicati sono disponibili anche come singolo script:

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
bash scripts/install-openclaw.sh
```

### Risoluzione problemi

| Problema | Causa | Soluzione |
|---------|-------|-----|
| `agentteam: command not found` | La directory bin di pip non è nel PATH | Esegui il Passo 3 (collegamento simbolico + PATH) |
| Gli agenti generati non trovano `agentteam` | Gli agenti vengono eseguiti in shell nuove senza il PATH di pip | Verifica che il collegamento simbolico `~/bin/AgentTeam` esista e che `~/bin` sia nel PATH |
| `openclaw approvals` fallisce | Il gateway non è in esecuzione | Avvia prima `openclaw gateway`, poi riprova il Passo 5 |
| `exec-approvals.json not found` | OpenClaw non è mai stato eseguito | Esegui `openclaw` una volta per generare la configurazione, poi riprova il Passo 5 |
| Gli agenti si bloccano sui prompt di autorizzazione | La sicurezza delle approvazioni di esecuzione è impostata su "full" | Esegui il Passo 5 per passare ad "allowlist" |
| `pip install -e .` fallisce | Dipendenze di build mancanti | Esegui prima `pip install hatchling` |
| `agentteam --version` mostra "Coming Soon" | Installato per errore il pacchetto npm usurpatore (`a9logic`, non correlato a questo progetto) | `npm uninstall -g agentteam`, poi reinstallare secondo il passaggio 2 |

---

## Casi d'uso

### 1. Ricerca ML autonoma �?8 agenti x 8 GPU

Basato su [@karpathy/autoresearch](https://github.com/karpathy/autoresearch). Un singolo prompt lancia 8 agenti di ricerca su H100 che progettano oltre 2000 esperimenti in modo autonomo.

```
Human: "Use 8 GPUs to optimize train.py. Read program.md for instructions."

Leader agent:
├── Spawns 8 agents, each assigned a research direction (depth, width, LR, batch size...)
├── Each agent gets its own git worktree for isolated experiments
├── Every 30 min: checks results, cross-pollinates best configs to new agents
├── Reassigns GPUs as agents finish �?fresh agents start from best known config
└── Result: val_bpb 1.044 �?0.977 (6.4% improvement) across 2430 experiments in ~30 GPU-hours
```

Risultati completi: [novix-science/autoresearch](https://github.com/novix-science/autoresearch)

### 2. Ingegneria del software agentica

```
Human: "Build a full-stack todo app with auth, database, and React frontend."

Leader agent:
├── Creates tasks with dependency chains (API schema �?auth + DB �?frontend �?tests)
├── Spawns 5 agents (architect, 2 backend, frontend, tester) in separate worktrees
├── Dependencies auto-resolve: architect completes �?backend unblocks �?tester unblocks
├── Agents coordinate via inbox: "Here's the OpenAPI spec", "Auth endpoints ready"
└── Leader merges all worktrees into main when complete
```

### 3. Fondo speculativo IA �?Lancio da template

Un template TOML genera un team di investimento completo con 7 agenti tramite un singolo comando:

```bash
agentteam launch hedge-fund --team fund1 --goal "Analyze AAPL, MSFT, NVDA for Q2 2026"
```

5 agenti analisti (valore, crescita, tecnico, fondamentali, sentiment) lavorano in parallelo. Il risk manager sintetizza tutti i segnali. Il portfolio manager prende le decisioni finali.

I template sono file TOML �?**crea i tuoi** per qualsiasi dominio.

---

## Funzionalità

<table>
<tr>
<td width="50%">

### Auto-organizzazione degli agenti
- Il leader genera e gestisce i worker
- Prompt di coordinamento auto-iniettato �?zero configurazione manuale
- I worker segnalano autonomamente il proprio stato e lo stato di inattività
- Qualsiasi agente CLI può partecipare

### Isolamento dello spazio di lavoro
- Ogni agente ottiene il proprio **git worktree**
- Nessun conflitto di merge tra agenti paralleli
- Comandi di checkpoint, merge e pulizia
- Denominazione dei branch: `agentteam/{team}/{agent}`

### Tracciamento delle attività con dipendenze
- Kanban condiviso: `pending` �?`in_progress` �?`completed` / `blocked`
- Catene `--blocked-by` con sblocco automatico al completamento
- `task wait` blocca fino al completamento di tutte le attività

</td>
<td width="50%">

### Messaggistica tra agenti
- Caselle di posta punto-a-punto (invio, ricezione, anteprima)
- Broadcast a tutti i membri del team
- Trasporto basato su file (predefinito) o ZeroMQ P2P

### Monitoraggio e dashboard
- `board show` �?kanban nel terminale
- `board live` �?dashboard con aggiornamento automatico
- `board attach` �?vista tmux affiancata di tutti gli agenti
- `board serve` �?Web UI con aggiornamenti in tempo reale

### Template di team
- File TOML che definiscono archetipi di team (ruoli, attività, prompt)
- Un solo comando: `agentteam launch <template>`
- Sostituzione di variabili: `{goal}`, `{team_name}`, `{agent_name}`
- **Assegnazione modello per agente** (anteprima): assegna modelli diversi a ruoli diversi �?vedi [sotto](#assegnazione-modello-per-agente-anteprima)

</td>
</tr>
</table>

**Inoltre:** flussi di approvazione piani, gestione del ciclo di vita graceful, output `--json` su tutti i comandi, supporto cross-machine (NFS/SSHFS o P2P), namespacing multi-utente, validazione dello spawn con rollback automatico, locking dei file con `fcntl` per la sicurezza in concorrenza.

---

## Integrazione OpenClaw

Questo fork rende [OpenClaw](https://openclaw.ai) l'**agente predefinito**. Senza AgentTeam, ogni agente OpenClaw lavora in isolamento. AgentTeam lo trasforma in una piattaforma multi-agente.

| Funzionalità | Solo OpenClaw | OpenClaw + AgentTeam |
|-----------|---------------|-------------------|
| **Assegnazione attività** | Messaggistica manuale per agente | Il leader suddivide, assegna e monitora autonomamente |
| **Sviluppo parallelo** | Directory di lavoro condivisa | Git worktree isolati per agente |
| **Dipendenze** | Polling manuale | `--blocked-by` con sblocco automatico |
| **Comunicazione** | Solo tramite relay AGI | Casella di posta diretta punto-a-punto + broadcast |
| **Osservabilità** | Lettura dei log | Kanban board + vista tmux affiancata |

Una volta installata la skill, parla con il tuo bot OpenClaw in qualsiasi canale:

| Cosa dici | Cosa succede |
|-------------|-------------|
| "Crea un team di 5 agenti per costruire un'app web" | Crea il team, le attività, genera 5 agenti in tmux |
| "Lancia un team di analisi hedge-fund" | `agentteam launch hedge-fund` con 7 agenti |
| "Controlla lo stato del mio team di agenti" | `agentteam board show` con output kanban |

```
  You (Telegram/Discord/TUI)
         �?
         �?
  ┌──────────────────�?
  �? OpenClaw Gateway �? �?activates agentteam skill
  └────────┬─────────�?
           �?
           �?
  ┌──────────────────�?    agentteam spawn     ┌─────────────────�?
  �? Leader Agent    �?─────────────────────�?�? openclaw tui   �?
  �? (openclaw)      �?──�?                   �? (tmux window)  �?
  �?                 �?  �?                   �? git worktree   �?
  �? Manages swarm   �?  ├──────────────────�?├─────────────────�?
  �? via agentteam    �?  �?                   �? openclaw tui   �?
  �? CLI             �?  ├──────────────────�?├─────────────────�?
  └──────────────────�?  �?                   �? openclaw tui   �?
                         └──────────────────�?└─────────────────�?
                                               All coordinate via
                                               ~/.agentteam/ (tasks, inboxes)
```

---

## Architettura

```
  Human: "Optimize this LLM"
         �?
         �?
  ┌──────────────�?    agentteam spawn     ┌──────────────�?
  �? Leader      �?──────────────────────�?�? Worker      �?
  �? (any agent) �?──────�?               �? git worktree �?
  �?             �?      ├──────────────�?�? tmux window  �?
  �? spawn       �?      �?               ├──────────────�?
  �? task create �?      ├──────────────�?�? Worker      �?
  �? inbox send  �?      �?               �? git worktree �?
  �? board show  �?      └──────────────�?�? tmux window  �?
  └──────────────�?                       └──────────────�?
                                                 �?
                                                 �?
                                      ┌─────────────────────�?
                                      �?   ~/.agentteam/     �?
                                      �?├── teams/   (who) �?
                                      �?├── tasks/   (what)�?
                                      �?├── inboxes/ (talk)�?
                                      �?└── workspaces/    �?
                                      └─────────────────────�?
```

Tutto lo stato risiede in `~/.agentteam/` come file JSON. Nessun database, nessun server. Scritture atomiche con locking dei file tramite `fcntl` garantiscono la sicurezza in caso di crash.

| Impostazione | Variabile d'ambiente | Predefinito |
|---------|---------|---------|
| Directory dati | `AgentTeam_DATA_DIR` | `~/.agentteam` |
| Trasporto | `AgentTeam_TRANSPORT` | `file` |
| Modalità workspace | `AgentTeam_WORKSPACE` | `auto` |
| Backend di spawn | `AgentTeam_DEFAULT_BACKEND` | `tmux` |

---

## Riferimento comandi

<details open>
<summary><strong>Comandi principali</strong></summary>

```bash
# Team lifecycle
agentteam team spawn-team <team> -d "description" -n <leader>
agentteam team discover                    # List all teams
agentteam team status <team>               # Show members
agentteam team cleanup <team> --force      # Delete team

# Spawn agents
agentteam spawn --team <team> --agent-name <name> --task "do this"
agentteam spawn tmux codex --team <team> --agent-name <name> --task "do this"

# Task management
agentteam task create <team> "subject" -o <owner> --blocked-by <id1>,<id2>
agentteam task update <team> <id> --status completed   # auto-unblocks dependents
agentteam task list <team> --status blocked --owner worker1
agentteam task wait <team> --timeout 300

# Messaging
agentteam inbox send <team> <to> "message"
agentteam inbox broadcast <team> "message"
agentteam inbox receive <team>             # consume messages
agentteam inbox peek <team>                # read without consuming

# Monitoring
agentteam board show <team>                # terminal kanban
agentteam board live <team> --interval 3   # auto-refresh
agentteam board attach <team>              # tiled tmux view
agentteam board serve --port 8080          # web UI
```

</details>

<details>
<summary><strong>Workspace, Piani, Ciclo di vita, Configurazione</strong></summary>

```bash
# Workspace (git worktree management)
agentteam workspace list <team>
agentteam workspace checkpoint <team> <agent>    # auto-commit
agentteam workspace merge <team> <agent>         # merge back to main
agentteam workspace cleanup <team> <agent>       # remove worktree

# Plan approval
agentteam plan submit <team> <agent> "plan" --summary "TL;DR"
agentteam plan approve <team> <plan-id> <agent> --feedback "LGTM"
agentteam plan reject <team> <plan-id> <agent> --feedback "Revise X"

# Lifecycle
agentteam lifecycle request-shutdown <team> <agent> --reason "done"
agentteam lifecycle approve-shutdown <team> <request-id> <agent>
agentteam lifecycle idle <team>

# Templates
agentteam launch <template> --team <name> --goal "Build X"
agentteam template list

# Config
agentteam config show
agentteam config set transport p2p
agentteam config health
```

</details>

---

## Assegnazione modello per agente (Anteprima)

> **Branch:** [`feat/per-agent-model-assignment`](https://github.com/win4r/AgentTeam-OpenClaw/tree/feat/per-agent-model-assignment)
>
> Questa funzionalità è disponibile per test preliminari su un branch separato. Verrà unita al `main` una volta che il flag `--model` companion di OpenClaw sarà rilasciato.

Assegna modelli diversi a ruoli di agente diversi per un miglior rapporto costo/prestazioni negli sciami multi-agente.

```bash
# Install from the feature branch
pip install -e "git+https://github.com/win4r/AgentTeam-OpenClaw.git@feat/per-agent-model-assignment#egg=agentteam"
```

**Modello per agente nei template:**
```toml
[template]
name = "my-team"
command = ["openclaw"]
model = "sonnet-4.6"              # default for all agents
model_strategy = "auto"           # or: leaders→strong, workers→balanced

[template.leader]
name = "lead"
model = "opus"                    # override for leader

[[template.agents]]
name = "worker"
model_tier = "cheap"              # cost tiers: strong / balanced / cheap
```

**Flag CLI:**
```bash
agentteam spawn --model opus                          # single agent
agentteam launch my-template --model gpt-5.4          # override all agents
agentteam launch my-template --model-strategy auto     # auto-assign by role
```

Vedi [issue #1](https://github.com/win4r/AgentTeam-OpenClaw/issues/1) per la richiesta di funzionalità completa e la discussione.

---

## Roadmap

| Versione | Cosa | Stato |
|---------|------|--------|
| v0.3 | Trasporto File + P2P, Web UI, multi-utente, template | Rilasciato |
| v0.4 | Trasporto Redis �?messaggistica cross-machine | Pianificato |
| v0.5 | Livello di stato condiviso �?configurazione team tra macchine | Pianificato |
| v0.6 | Marketplace agenti �?template della comunità | In esplorazione |
| v0.7 | Schedulazione adattiva �?riassegnazione dinamica delle attività | In esplorazione |
| v1.0 | Produzione �?autenticazione, permessi, log di audit | In esplorazione |

---

## Contribuire

Accogliamo con piacere i contributi:

- **Integrazioni di agenti** �?supporto per più agenti CLI
- **Template di team** �?template TOML per nuovi domini
- **Backend di trasporto** �?Redis, NATS, ecc.
- **Miglioramenti della dashboard** �?Web UI, Grafana
- **Documentazione** �?tutorial e buone pratiche

---

## Ringraziamenti

- [@karpathy/autoresearch](https://github.com/karpathy/autoresearch) �?framework di ricerca ML autonoma
- [OpenClaw](https://openclaw.ai) �?backend agente predefinito
- [Claude Code](https://claude.ai/claude-code) e [Codex](https://openai.com/codex) �?agenti di codifica IA supportati
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) �?ispirazione per il template hedge fund
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) �?progetto gemello

## Licenza

MIT �?libero di usare, modificare e distribuire.

---

<div align="center">

**AgentTeam** �?*Intelligenza a sciame di agenti.*

</div>
