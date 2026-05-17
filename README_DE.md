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
  <strong>Multi-Agenten-Schwarm-Koordination für CLI-Coding-Agenten �?<a href="https://openclaw.ai">OpenClaw</a> als Standard</strong>
</p>

<p align="center">
  <a href="https://github.com/HKUDS/AgentTeam"><img src="https://img.shields.io/badge/upstream-HKUDS%2FAgentTeam-purple?style=for-the-badge" alt="Upstream"></a>
  <a href="#-schnellstart"><img src="https://img.shields.io/badge/Quick_Start-3_min-blue?style=for-the-badge" alt="Schnellstart"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="Lizenz"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-�?.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/agents-OpenClaw_%7C_Claude_Code_%7C_Codex_%7C_nanobot-blueviolet" alt="Agents">
  <img src="https://img.shields.io/badge/transport-File_%7C_ZeroMQ_P2P-orange" alt="Transport">
  <img src="https://img.shields.io/badge/version-0.3.0-teal" alt="Version">
</p>

> **Fork von [HKUDS/AgentTeam](https://github.com/HKUDS/AgentTeam)** mit tiefer OpenClaw-Integration: Standard-Agent `openclaw`, sitzungsisolierte Agenten, automatische Konfiguration der Ausführungsgenehmigungen und produktionsgehärtete Spawn-Backends. Alle Upstream-Fixes werden synchronisiert.

Sie setzen das Ziel. Der Agenten-Schwarm erledigt den Rest �?Worker erzeugen, Aufgaben aufteilen, koordinieren und Ergebnisse zusammenführen.

Funktioniert mit [OpenClaw](https://openclaw.ai) (Standard), [Claude Code](https://claude.ai/claude-code), [Codex](https://openai.com/codex), [nanobot](https://github.com/HKUDS/nanobot), [Cursor](https://cursor.com) und jedem CLI-Agenten.

---

## Warum AgentTeam?

Aktuelle KI-Agenten sind leistungsfähig, arbeiten aber **isoliert**. AgentTeam ermöglicht es Agenten, sich selbst in Teams zu organisieren �?Arbeit aufzuteilen, zu kommunizieren und Ergebnisse zusammenzuführen, ohne menschliches Mikromanagement.

| | AgentTeam | Andere Multi-Agenten-Frameworks |
|---|---------|----------------------------|
| **Wer nutzt es** | Die KI-Agenten selbst | Menschen, die Orchestrierungscode schreiben |
| **Einrichtung** | `pip install` + ein Prompt | Docker, Cloud-APIs, YAML-Konfigurationen |
| **Infrastruktur** | Dateisystem + tmux | Redis, Nachrichtenwarteschlangen, Datenbanken |
| **Agenten-Unterstützung** | Jeder CLI-Agent | Nur framework-spezifische |
| **Isolation** | Git Worktrees (echte Branches) | Container oder virtuelle Umgebungen |

---

## So funktioniert es

<table>
<tr>
<td width="33%">

### Agenten erzeugen Agenten
Der Leiter ruft `agentteam spawn` auf, um Worker zu erstellen. Jeder bekommt seinen eigenen **Git Worktree**, sein eigenes **tmux-Fenster** und seine eigene **Identität**.

```bash
agentteam spawn --team my-team \
  --agent-name worker1 \
  --task "Implement auth module"
```

</td>
<td width="33%">

### Agenten kommunizieren
Worker prüfen ihre Posteingänge, aktualisieren Aufgaben und melden Ergebnisse �?alles über CLI-Befehle, die **automatisch** in ihren Prompt eingefügt werden.

```bash
agentteam task list my-team --owner me
agentteam inbox send my-team leader \
  "Auth done. All tests passing."
```

</td>
<td width="33%">

### Sie schauen einfach zu
Überwachen Sie den Schwarm über eine gekachelte tmux-Ansicht oder die Web-Oberfläche. Der Leiter übernimmt die Koordination.

```bash
agentteam board attach my-team
# Or web dashboard
agentteam board serve --port 8080
```

</td>
</tr>
</table>

---

## Schnellstart

### Option 1: Den Agenten steuern lassen (Empfohlen)

Installieren Sie AgentTeam und geben Sie Ihrem Agenten folgenden Prompt:

```
"Build a web app. Use agentteam to split the work across multiple agents."
```

Der Agent erstellt automatisch ein Team, erzeugt Worker, weist Aufgaben zu und koordiniert �?alles über die `agentteam`-CLI.

### Option 2: Manuell steuern

```bash
# Create a team
agentteam team spawn-team my-team -d "Build the auth module" -n leader

# Spawn workers �?each gets a git worktree + tmux window
agentteam spawn --team my-team --agent-name alice --task "Implement OAuth2 flow"
agentteam spawn --team my-team --agent-name bob   --task "Write unit tests for auth"

# Watch them work
agentteam board attach my-team
```

### Unterstützte Agenten

| Agent | Spawn-Befehl | Status |
|-------|--------------|--------|
| [OpenClaw](https://openclaw.ai) | `agentteam spawn tmux openclaw --team ...` | **Standard** |
| [Claude Code](https://claude.ai/claude-code) | `agentteam spawn tmux claude --team ...` | Volle Unterstützung |
| [Codex](https://openai.com/codex) | `agentteam spawn tmux codex --team ...` | Volle Unterstützung |
| [nanobot](https://github.com/HKUDS/nanobot) | `agentteam spawn tmux nanobot --team ...` | Volle Unterstützung |
| [Cursor](https://cursor.com) | `agentteam spawn subprocess cursor --team ...` | Experimentell |
| Benutzerdefinierte Skripte | `agentteam spawn subprocess python --team ...` | Volle Unterstützung |

---

## Installation

### Schritt 1: Voraussetzungen

AgentTeam erfordert **Python 3.10+**, **tmux** und mindestens einen CLI-Coding-Agenten (OpenClaw, Claude Code, Codex usw.).

**Prüfen Sie, was Sie bereits haben:**

```bash
python3 --version   # Need 3.10+
tmux -V             # Need any version
openclaw --version  # Or: claude --version / codex --version
```

**Fehlende Voraussetzungen installieren:**

| Werkzeug | macOS | Ubuntu/Debian |
|------|-------|---------------|
| Python 3.10+ | `brew install python@3.12` | `sudo apt update && sudo apt install python3 python3-pip` |
| tmux | `brew install tmux` | `sudo apt install tmux` |
| OpenClaw | `pip install openclaw` | `pip install openclaw` |

> Falls Sie Claude Code oder Codex anstelle von OpenClaw verwenden, installieren Sie diese gemäß deren eigener Dokumentation. OpenClaw ist der Standard, aber nicht zwingend erforderlich.

### Schritt 2: AgentTeam installieren

> **⚠️ Führen Sie NICHT `pip install agentteam` oder `npm install -g agentteam` direkt aus:**
> - `pip install agentteam` installiert die Upstream-Version von PyPI, die standardmäßig `claude` nutzt und die OpenClaw-Anpassungen nicht enthält.
> - `npm install -g agentteam` installiert ein fremdes Squatting-Paket (Herausgeber `a9logic`). Wenn `agentteam --version` "Coming Soon" anzeigt, haben Sie das falsche Paket. Führen Sie zuerst `npm uninstall -g agentteam` aus.
>
> **Verwenden Sie die drei Befehle unten �?`pip install -e .` nach dem Clone ist erforderlich. Es installiert aus dem lokalen Repository, nicht von PyPI.**

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
pip install -e .    # �?Erforderlich! Installiert aus dem lokalen Repository, NICHT identisch mit pip install agentteam
```

Optional �?P2P-Transport (ZeroMQ):

```bash
pip install -e ".[p2p]"
```

### Schritt 3: Symlink `~/bin/AgentTeam` erstellen

Erzeugte Agenten laufen in frischen Shells, die möglicherweise kein pip-bin-Verzeichnis im PATH haben. Ein Symlink in `~/bin` stellt sicher, dass `agentteam` immer erreichbar ist:

```bash
mkdir -p ~/bin
ln -sf "$(which agentteam)" ~/bin/AgentTeam
```

Falls `which agentteam` nichts zurückgibt, suchen Sie die Binärdatei manuell:

```bash
# Common locations:
# ~/.local/bin/AgentTeam
# /opt/homebrew/bin/AgentTeam
# /usr/local/bin/AgentTeam
# /Library/Frameworks/Python.framework/Versions/3.*/bin/AgentTeam
find / -name agentteam -type f 2>/dev/null | head -5
```

Stellen Sie dann sicher, dass `~/bin` in Ihrem PATH ist �?fügen Sie dies zu `~/.zshrc` oder `~/.bashrc` hinzu, falls nicht vorhanden:

```bash
export PATH="$HOME/bin:$PATH"
```

### Schritt 4: OpenClaw-Skill installieren (nur für OpenClaw-Nutzer)

Die Skill-Datei bringt OpenClaw-Agenten bei, wie sie AgentTeam per natürlicher Sprache nutzen. Überspringen Sie diesen Schritt, wenn Sie OpenClaw nicht verwenden.

```bash
mkdir -p ~/.openclaw/workspace/skills/AgentTeam
cp skills/openclaw/SKILL.md ~/.openclaw/workspace/skills/AgentTeam/SKILL.md
```

### Schritt 5: Ausführungsgenehmigungen konfigurieren (nur für OpenClaw-Nutzer)

Erzeugte OpenClaw-Agenten benötigen die Berechtigung, `agentteam`-Befehle auszuführen. Ohne diese blockieren Agenten bei interaktiven Berechtigungsabfragen.

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

> Falls `openclaw approvals` fehlschlägt, läuft das OpenClaw-Gateway möglicherweise nicht. Starten Sie es zuerst und versuchen Sie es erneut.

### Schritt 6: Überprüfung

```bash
agentteam --version          # Should print version
agentteam config health      # Should show all green
```

Falls Sie OpenClaw verwenden, überprüfen Sie auch, ob der Skill geladen ist:

```bash
openclaw skills list | grep agentteam
```

### Automatischer Installer

Die Schritte 2�? oben sind auch als einzelnes Skript verfügbar:

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
bash scripts/install-openclaw.sh
```

### Fehlerbehebung

| Problem | Ursache | Lösung |
|---------|---------|--------|
| `agentteam: command not found` | pip-bin-Verzeichnis nicht im PATH | Schritt 3 ausführen (Symlink + PATH) |
| Erzeugte Agenten finden `agentteam` nicht | Agenten laufen in frischen Shells ohne pip-PATH | Prüfen Sie, ob der Symlink `~/bin/AgentTeam` existiert und `~/bin` im PATH ist |
| `openclaw approvals` schlägt fehl | Gateway läuft nicht | Zuerst `openclaw gateway` starten, dann Schritt 5 wiederholen |
| `exec-approvals.json not found` | OpenClaw wurde nie ausgeführt | Führen Sie `openclaw` einmal aus, um die Konfiguration zu generieren, dann Schritt 5 wiederholen |
| Agenten blockieren bei Berechtigungsabfragen | Ausführungsgenehmigungen stehen auf "full" | Schritt 5 ausführen, um auf "allowlist" umzuschalten |
| `pip install -e .` schlägt fehl | Fehlende Build-Abhängigkeiten | Zuerst `pip install hatchling` ausführen |
| `agentteam --version` zeigt "Coming Soon" | Falsches npm-Squatting-Paket installiert (`a9logic`, ohne Bezug zu diesem Projekt) | `npm uninstall -g agentteam`, dann gemäß Schritt 2 neu installieren |

---

## Anwendungsfälle

### 1. Autonome ML-Forschung �?8 Agenten x 8 GPUs

Basierend auf [@karpathy/autoresearch](https://github.com/karpathy/autoresearch). Ein einziger Prompt startet 8 Forschungsagenten auf H100s, die über 2000 Experimente autonom entwerfen.

```
Human: "Use 8 GPUs to optimize train.py. Read program.md for instructions."

Leader agent:
├── Spawns 8 agents, each assigned a research direction (depth, width, LR, batch size...)
├── Each agent gets its own git worktree for isolated experiments
├── Every 30 min: checks results, cross-pollinates best configs to new agents
├── Reassigns GPUs as agents finish �?fresh agents start from best known config
└── Result: val_bpb 1.044 �?0.977 (6.4% improvement) across 2430 experiments in ~30 GPU-hours
```

Vollständige Ergebnisse: [novix-science/autoresearch](https://github.com/novix-science/autoresearch)

### 2. Agentische Softwareentwicklung

```
Human: "Build a full-stack todo app with auth, database, and React frontend."

Leader agent:
├── Creates tasks with dependency chains (API schema �?auth + DB �?frontend �?tests)
├── Spawns 5 agents (architect, 2 backend, frontend, tester) in separate worktrees
├── Dependencies auto-resolve: architect completes �?backend unblocks �?tester unblocks
├── Agents coordinate via inbox: "Here's the OpenAPI spec", "Auth endpoints ready"
└── Leader merges all worktrees into main when complete
```

### 3. KI-Hedgefonds �?Template-Start

Ein TOML-Template erzeugt ein komplettes 7-Agenten-Investmentteam mit einem einzigen Befehl:

```bash
agentteam launch hedge-fund --team fund1 --goal "Analyze AAPL, MSFT, NVDA for Q2 2026"
```

5 Analysten-Agenten (Value, Growth, Technik, Fundamentaldaten, Sentiment) arbeiten parallel. Der Risikomanager synthetisiert alle Signale. Der Portfoliomanager trifft die endgültigen Entscheidungen.

Templates sind TOML-Dateien �?**erstellen Sie Ihre eigenen** für jeden beliebigen Bereich.

---

## Funktionen

<table>
<tr>
<td width="50%">

### Selbstorganisation der Agenten
- Der Leiter erzeugt und verwaltet Worker
- Automatisch eingefügter Koordinations-Prompt �?kein manuelles Setup
- Worker melden selbstständig ihren Status und Leerlaufzustand
- Jeder CLI-Agent kann teilnehmen

### Arbeitsbereich-Isolation
- Jeder Agent bekommt seinen eigenen **Git Worktree**
- Keine Merge-Konflikte zwischen parallelen Agenten
- Checkpoint-, Merge- und Cleanup-Befehle
- Branch-Benennung: `agentteam/{team}/{agent}`

### Aufgabenverfolgung mit Abhängigkeiten
- Gemeinsames Kanban: `pending` �?`in_progress` �?`completed` / `blocked`
- `--blocked-by`-Ketten mit automatischer Entsperrung bei Fertigstellung
- `task wait` blockiert, bis alle Aufgaben abgeschlossen sind

</td>
<td width="50%">

### Inter-Agenten-Nachrichtenverkehr
- Punkt-zu-Punkt-Posteingänge (senden, empfangen, einsehen)
- Broadcast an alle Teammitglieder
- Dateibasiert (Standard) oder ZeroMQ-P2P-Transport

### Überwachung und Dashboards
- `board show` �?Terminal-Kanban
- `board live` �?automatisch aktualisierendes Dashboard
- `board attach` �?gekachelte tmux-Ansicht aller Agenten
- `board serve` �?Web-Oberfläche mit Echtzeit-Updates

### Team-Templates
- TOML-Dateien definieren Team-Archetypen (Rollen, Aufgaben, Prompts)
- Ein Befehl: `agentteam launch <template>`
- Variablenersetzung: `{goal}`, `{team_name}`, `{agent_name}`
- **Modellzuweisung pro Agent** (Vorschau): verschiedene Modelle für verschiedene Rollen zuweisen �?siehe [unten](#modellzuweisung-pro-agent-vorschau)

</td>
</tr>
</table>

**Außerdem:** Plan-Genehmigungsworkflows, sanftes Lifecycle-Management, `--json`-Ausgabe bei allen Befehlen, maschinenübergreifende Unterstützung (NFS/SSHFS oder P2P), Multi-User-Namespacing, Spawn-Validierung mit automatischem Rollback, `fcntl`-Dateisperren für Nebenläufigkeitssicherheit.

---

## OpenClaw-Integration

Dieser Fork macht [OpenClaw](https://openclaw.ai) zum **Standard-Agenten**. Ohne AgentTeam arbeitet jeder OpenClaw-Agent isoliert. AgentTeam verwandelt es in eine Multi-Agenten-Plattform.

| Fähigkeit | OpenClaw allein | OpenClaw + AgentTeam |
|-----------|---------------|-------------------|
| **Aufgabenzuweisung** | Manuelles Messaging pro Agent | Leiter teilt, weist zu und überwacht autonom |
| **Parallele Entwicklung** | Gemeinsames Arbeitsverzeichnis | Isolierte Git Worktrees pro Agent |
| **Abhängigkeiten** | Manuelles Polling | `--blocked-by` mit automatischer Entsperrung |
| **Kommunikation** | Nur über AGI-Relay | Direkter Punkt-zu-Punkt-Posteingang + Broadcast |
| **Beobachtbarkeit** | Logs lesen | Kanban-Board + gekachelte tmux-Ansicht |

Sobald der Skill installiert ist, sprechen Sie mit Ihrem OpenClaw-Bot in jedem Kanal:

| Was Sie sagen | Was passiert |
|-------------|-------------|
| "Erstelle ein 5-Agenten-Team zum Bau einer Web-App" | Erstellt Team, Aufgaben, erzeugt 5 Agenten in tmux |
| "Starte ein Hedgefonds-Analyseteam" | `agentteam launch hedge-fund` mit 7 Agenten |
| "Zeige den Status meines Agenten-Teams" | `agentteam board show` mit Kanban-Ausgabe |

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

## Architektur

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

Der gesamte Zustand liegt als JSON-Dateien in `~/.agentteam/`. Keine Datenbank, kein Server. Atomare Schreibvorgänge mit `fcntl`-Dateisperren gewährleisten Absturzsicherheit.

| Einstellung | Umgebungsvariable | Standardwert |
|---------|---------|---------|
| Datenverzeichnis | `AgentTeam_DATA_DIR` | `~/.agentteam` |
| Transport | `AgentTeam_TRANSPORT` | `file` |
| Arbeitsbereich-Modus | `AgentTeam_WORKSPACE` | `auto` |
| Spawn-Backend | `AgentTeam_DEFAULT_BACKEND` | `tmux` |

---

## Befehlsreferenz

<details open>
<summary><strong>Kernbefehle</strong></summary>

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
<summary><strong>Arbeitsbereich, Plan, Lifecycle, Konfiguration</strong></summary>

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

## Modellzuweisung pro Agent (Vorschau)

> **Branch:** [`feat/per-agent-model-assignment`](https://github.com/win4r/AgentTeam-OpenClaw/tree/feat/per-agent-model-assignment)
>
> Diese Funktion steht auf einem separaten Branch zum frühen Testen bereit. Sie wird in `main` zusammengeführt, sobald das zugehörige OpenClaw-`--model`-Flag veröffentlicht ist.

Weisen Sie verschiedenen Agentenrollen unterschiedliche Modelle zu, um bessere Kosten-/Leistungsverhältnisse in Multi-Agenten-Schwärmen zu erzielen.

```bash
# Install from the feature branch
pip install -e "git+https://github.com/win4r/AgentTeam-OpenClaw.git@feat/per-agent-model-assignment#egg=agentteam"
```

**Modell pro Agent in Templates:**
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

**CLI-Flags:**
```bash
agentteam spawn --model opus                          # single agent
agentteam launch my-template --model gpt-5.4          # override all agents
agentteam launch my-template --model-strategy auto     # auto-assign by role
```

Siehe [Issue #1](https://github.com/win4r/AgentTeam-OpenClaw/issues/1) für die vollständige Funktionsanfrage und Diskussion.

---

## Roadmap

| Version | Was | Status |
|---------|------|--------|
| v0.3 | Datei- + P2P-Transport, Web-Oberfläche, Multi-User, Templates | Ausgeliefert |
| v0.4 | Redis-Transport �?maschinenübergreifendes Messaging | Geplant |
| v0.5 | Gemeinsame Zustandsebene �?Team-Konfiguration über Maschinen hinweg | Geplant |
| v0.6 | Agenten-Marktplatz �?Community-Templates | In Erkundung |
| v0.7 | Adaptive Planung �?dynamische Aufgabenneuzuweisung | In Erkundung |
| v1.0 | Produktionsreife �?Authentifizierung, Berechtigungen, Audit-Logs | In Erkundung |

---

## Mitwirken

Beiträge sind willkommen:

- **Agenten-Integrationen** �?Unterstützung für weitere CLI-Agenten
- **Team-Templates** �?TOML-Templates für neue Bereiche
- **Transport-Backends** �?Redis, NATS usw.
- **Dashboard-Verbesserungen** �?Web-Oberfläche, Grafana
- **Dokumentation** �?Tutorials und bewährte Verfahren

---

## Danksagungen

- [@karpathy/autoresearch](https://github.com/karpathy/autoresearch) �?Framework für autonome ML-Forschung
- [OpenClaw](https://openclaw.ai) �?Standard-Agenten-Backend
- [Claude Code](https://claude.ai/claude-code) und [Codex](https://openai.com/codex) �?unterstützte KI-Coding-Agenten
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) �?Inspiration für das Hedgefonds-Template
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) �?Schwesterprojekt

## Lizenz

MIT �?frei nutzbar, modifizierbar und verteilbar.

---

<div align="center">

**AgentTeam** �?*Agenten-Schwarm-Intelligenz.*

</div>
