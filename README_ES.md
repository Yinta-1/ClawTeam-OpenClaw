<p align="center">
  <a href="README.md">English</a> |
  <a href="README_CN.md">ç®ä½ä¸­æ?/a> |
  <a href="README_TW.md">ç¹é«ä¸­æ</a> |
  <a href="README_JA.md">æ¥æ¬èª?/a> |
  <a href="README_KO.md">íêµ­ì?/a> |
  <a href="README_FR.md">FranÃ§ais</a> |
  <a href="README_ES.md">EspaÃ±ol</a> |
  <a href="README_DE.md">Deutsch</a> |
  <a href="README_IT.md">Italiano</a> |
  <a href="README_RU.md">Ð ÑÑÑÐºÐ¸Ð¹</a> |
  <a href="README_PT-BR.md">PortuguÃªs (Brasil)</a>
</p>

<h1 align="center">ð¦AgentTeam-OpenClaw</h1>

<p align="center">
  <strong>CoordinaciÃ³n de enjambre multi-agente para agentes de codificaciÃ³n CLI â?<a href="https://openclaw.ai">OpenClaw</a> por defecto</strong>
</p>

<p align="center">
  <a href="https://github.com/HKUDS/AgentTeam"><img src="https://img.shields.io/badge/upstream-HKUDS%2FAgentTeam-purple?style=for-the-badge" alt="Upstream"></a>
  <a href="#-inicio-rÃ¡pido"><img src="https://img.shields.io/badge/Quick_Start-3_min-blue?style=for-the-badge" alt="Inicio rÃ¡pido"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="Licencia"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-â?.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/agents-OpenClaw_%7C_Claude_Code_%7C_Codex_%7C_nanobot-blueviolet" alt="Agents">
  <img src="https://img.shields.io/badge/transport-File_%7C_ZeroMQ_P2P-orange" alt="Transport">
  <img src="https://img.shields.io/badge/version-0.3.0-teal" alt="Version">
</p>

> **Fork de [HKUDS/AgentTeam](https://github.com/HKUDS/AgentTeam)** con integraciÃ³n profunda de OpenClaw: agente `openclaw` por defecto, aislamiento de sesiÃ³n por agente, autoconfiguraciÃ³n de aprobaciÃ³n de ejecuciÃ³n y backends de creaciÃ³n endurecidos para producciÃ³n. Todas las correcciones del upstream se sincronizan.

TÃº defines el objetivo. El enjambre de agentes se encarga del resto â?generando trabajadores, dividiendo tareas, coordinando y fusionando resultados.

Funciona con [OpenClaw](https://openclaw.ai) (por defecto), [Claude Code](https://claude.ai/claude-code), [Codex](https://openai.com/codex), [nanobot](https://github.com/HKUDS/nanobot), [Cursor](https://cursor.com) y cualquier agente CLI.

---

## Â¿Por quÃ© AgentTeam?

Los agentes de IA actuales son potentes pero trabajan de forma **aislada**. AgentTeam permite que los agentes se auto-organicen en equipos â?dividiendo trabajo, comunicÃ¡ndose y convergiendo en resultados sin microgestiÃ³n humana.

| | AgentTeam | Otros frameworks multi-agente |
|---|---------|----------------------------|
| **QuiÃ©n lo usa** | Los propios agentes de IA | Humanos escribiendo cÃ³digo de orquestaciÃ³n |
| **ConfiguraciÃ³n** | `pip install` + un prompt | Docker, APIs en la nube, configuraciones YAML |
| **Infraestructura** | Sistema de archivos + tmux | Redis, colas de mensajes, bases de datos |
| **Soporte de agentes** | Cualquier agente CLI | Solo especÃ­fico del framework |
| **Aislamiento** | Git worktrees (ramas reales) | Contenedores o entornos virtuales |

---

## CÃ³mo funciona

<table>
<tr>
<td width="33%">

### Los agentes generan agentes
El lÃ­der llama a `agentteam spawn` para crear trabajadores. Cada uno recibe su propio **git worktree**, **ventana tmux** e **identidad**.

```bash
agentteam spawn --team my-team \
  --agent-name worker1 \
  --task "Implement auth module"
```

</td>
<td width="33%">

### Los agentes se comunican
Los trabajadores revisan bandejas de entrada, actualizan tareas e informan resultados â?todo mediante comandos CLI **auto-inyectados** en su prompt.

```bash
agentteam task list my-team --owner me
agentteam inbox send my-team leader \
  "Auth done. All tests passing."
```

</td>
<td width="33%">

### Solo observa
Monitorea el enjambre desde una vista tmux en mosaico o la interfaz web. El lÃ­der gestiona la coordinaciÃ³n.

```bash
agentteam board attach my-team
# Or web dashboard
agentteam board serve --port 8080
```

</td>
</tr>
</table>

---

## Inicio rÃ¡pido

### OpciÃ³n 1: Deja que el agente conduzca (Recomendado)

Instala AgentTeam, luego indica a tu agente:

```
"Build a web app. Use agentteam to split the work across multiple agents."
```

El agente crea automÃ¡ticamente un equipo, genera trabajadores, asigna tareas y coordina â?todo a travÃ©s del CLI `agentteam`.

### OpciÃ³n 2: CondÃºcelo manualmente

```bash
# Create a team
agentteam team spawn-team my-team -d "Build the auth module" -n leader

# Spawn workers â?each gets a git worktree + tmux window
agentteam spawn --team my-team --agent-name alice --task "Implement OAuth2 flow"
agentteam spawn --team my-team --agent-name bob   --task "Write unit tests for auth"

# Watch them work
agentteam board attach my-team
```

### Agentes soportados

| Agente | Comando de generaciÃ³n | Estado |
|-------|--------------|--------|
| [OpenClaw](https://openclaw.ai) | `agentteam spawn tmux openclaw --team ...` | **Por defecto** |
| [Claude Code](https://claude.ai/claude-code) | `agentteam spawn tmux claude --team ...` | Soporte completo |
| [Codex](https://openai.com/codex) | `agentteam spawn tmux codex --team ...` | Soporte completo |
| [nanobot](https://github.com/HKUDS/nanobot) | `agentteam spawn tmux nanobot --team ...` | Soporte completo |
| [Cursor](https://cursor.com) | `agentteam spawn subprocess cursor --team ...` | Experimental |
| Scripts personalizados | `agentteam spawn subprocess python --team ...` | Soporte completo |

---

## InstalaciÃ³n

### Paso 1: Requisitos previos

AgentTeam requiere **Python 3.10+**, **tmux** y al menos un agente de codificaciÃ³n CLI (OpenClaw, Claude Code, Codex, etc.).

**Verifica lo que ya tienes:**

```bash
python3 --version   # Need 3.10+
tmux -V             # Need any version
openclaw --version  # Or: claude --version / codex --version
```

**Instala los requisitos previos faltantes:**

| Herramienta | macOS | Ubuntu/Debian |
|------|-------|---------------|
| Python 3.10+ | `brew install python@3.12` | `sudo apt update && sudo apt install python3 python3-pip` |
| tmux | `brew install tmux` | `sudo apt install tmux` |
| OpenClaw | `pip install openclaw` | `pip install openclaw` |

> Si usas Claude Code o Codex en lugar de OpenClaw, instÃ¡lalos segÃºn su propia documentaciÃ³n. OpenClaw es el predeterminado pero no es estrictamente obligatorio.

### Paso 2: Instalar AgentTeam

> **â ï¸ NO ejecutes `pip install agentteam` ni `npm install -g agentteam` directamente:**
> - `pip install agentteam` instala la versiÃ³n upstream de PyPI, que usa `claude` por defecto y carece de adaptaciones OpenClaw.
> - `npm install -g agentteam` instala un paquete usurpador sin relaciÃ³n (publicado por `a9logic`). Si `agentteam --version` muestra "Coming Soon", es el paquete incorrecto. Ejecuta primero `npm uninstall -g agentteam`.
>
> **Usa los tres comandos de abajo â?el `pip install -e .` despuÃ©s del clone es obligatorio. Instala desde el repositorio local, no desde PyPI.**

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
pip install -e .    # â?Â¡Obligatorio! Instala desde el repositorio local, NO es lo mismo que pip install agentteam
```

Opcional â?transporte P2P (ZeroMQ):

```bash
pip install -e ".[p2p]"
```

### Paso 3: Crear el enlace simbÃ³lico `~/bin/AgentTeam`

Los agentes generados se ejecutan en shells nuevos que pueden no tener el directorio bin de pip en PATH. Un enlace simbÃ³lico en `~/bin` asegura que `agentteam` siempre sea accesible:

```bash
mkdir -p ~/bin
ln -sf "$(which agentteam)" ~/bin/AgentTeam
```

Si `which agentteam` no devuelve nada, busca el binario manualmente:

```bash
# Common locations:
# ~/.local/bin/AgentTeam
# /opt/homebrew/bin/AgentTeam
# /usr/local/bin/AgentTeam
# /Library/Frameworks/Python.framework/Versions/3.*/bin/AgentTeam
find / -name agentteam -type f 2>/dev/null | head -5
```

Luego asegÃºrate de que `~/bin` estÃ© en tu PATH â?aÃ±ade esto a `~/.zshrc` o `~/.bashrc` si no lo estÃ¡:

```bash
export PATH="$HOME/bin:$PATH"
```

### Paso 4: Instalar el skill de OpenClaw (solo usuarios de OpenClaw)

El archivo de skill enseÃ±a a los agentes de OpenClaw cÃ³mo usar AgentTeam a travÃ©s de lenguaje natural. Omite este paso si no usas OpenClaw.

```bash
mkdir -p ~/.openclaw/workspace/skills/AgentTeam
cp skills/openclaw/SKILL.md ~/.openclaw/workspace/skills/AgentTeam/SKILL.md
```

### Paso 5: Configurar aprobaciones de ejecuciÃ³n (solo usuarios de OpenClaw)

Los agentes de OpenClaw generados necesitan permiso para ejecutar comandos `agentteam`. Sin esto, los agentes se bloquearÃ¡n en prompts interactivos de permisos.

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
    print('exec-approvals.json not found â?run openclaw once first, then re-run this step')
"

# Add agentteam to the allowlist (use the absolute path â?OpenClaw 4.2+ requires it)
openclaw approvals allowlist add --agent "*" "$(which agentteam)"
```

> Si `openclaw approvals` falla, es posible que el gateway de OpenClaw no estÃ© en ejecuciÃ³n. InÃ­cialo primero y luego reintenta.

### Paso 6: Verificar

```bash
agentteam --version          # Should print version
agentteam config health      # Should show all green
```

Si usas OpenClaw, verifica tambiÃ©n que el skill estÃ© cargado:

```bash
openclaw skills list | grep agentteam
```

### Instalador automÃ¡tico

Los pasos 2 a 6 anteriores tambiÃ©n estÃ¡n disponibles como un Ãºnico script:

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
bash scripts/install-openclaw.sh
```

### SoluciÃ³n de problemas

| Problema | Causa | SoluciÃ³n |
|---------|-------|-----|
| `agentteam: command not found` | El directorio bin de pip no estÃ¡ en PATH | Ejecuta el Paso 3 (enlace simbÃ³lico + PATH) |
| Los agentes generados no encuentran `agentteam` | Los agentes se ejecutan en shells nuevos sin PATH de pip | Verifica que el enlace simbÃ³lico `~/bin/AgentTeam` exista y que `~/bin` estÃ© en PATH |
| `openclaw approvals` falla | El gateway no estÃ¡ en ejecuciÃ³n | Inicia `openclaw gateway` primero, luego reintenta el Paso 5 |
| `exec-approvals.json not found` | OpenClaw nunca se ejecutÃ³ | Ejecuta `openclaw` una vez para generar la configuraciÃ³n, luego reintenta el Paso 5 |
| Los agentes se bloquean en prompts de permisos | La seguridad de aprobaciones de ejecuciÃ³n estÃ¡ en "full" | Ejecuta el Paso 5 para cambiar a "allowlist" |
| `pip install -e .` falla | Faltan dependencias de compilaciÃ³n | Ejecuta `pip install hatchling` primero |
| `agentteam --version` muestra "Coming Soon" | Se instalÃ³ el paquete npm usurpador (`a9logic`, sin relaciÃ³n con este proyecto) | `npm uninstall -g agentteam`, luego reinstalar segÃºn el paso 2 |

---

## Casos de uso

### 1. InvestigaciÃ³n autÃ³noma de ML â?8 agentes x 8 GPUs

Basado en [@karpathy/autoresearch](https://github.com/karpathy/autoresearch). Un solo prompt lanza 8 agentes de investigaciÃ³n a travÃ©s de H100s que diseÃ±an mÃ¡s de 2000 experimentos de forma autÃ³noma.

```
Humano: "Use 8 GPUs to optimize train.py. Read program.md for instructions."

Agente lÃ­der:
âââ Genera 8 agentes, cada uno asignado a una direcciÃ³n de investigaciÃ³n (profundidad, ancho, LR, tamaÃ±o de lote...)
âââ Cada agente recibe su propio git worktree para experimentos aislados
âââ Cada 30 min: revisa resultados, poliniza las mejores configuraciones a nuevos agentes
âââ Reasigna GPUs cuando los agentes terminan â?nuevos agentes parten de la mejor configuraciÃ³n conocida
âââ Resultado: val_bpb 1.044 â?0.977 (mejora del 6.4%) en 2430 experimentos en ~30 horas-GPU
```

Resultados completos: [novix-science/autoresearch](https://github.com/novix-science/autoresearch)

### 2. IngenierÃ­a de software agÃ©ntica

```
Humano: "Build a full-stack todo app with auth, database, and React frontend."

Agente lÃ­der:
âââ Crea tareas con cadenas de dependencias (esquema API â?auth + BD â?frontend â?pruebas)
âââ Genera 5 agentes (arquitecto, 2 backend, frontend, tester) en worktrees separados
âââ Las dependencias se resuelven automÃ¡ticamente: arquitecto completa â?backend se desbloquea â?tester se desbloquea
âââ Los agentes coordinan vÃ­a bandeja de entrada: "AquÃ­ estÃ¡ la especificaciÃ³n OpenAPI", "Endpoints de auth listos"
âââ El lÃ­der fusiona todos los worktrees en main cuando se completa
```

### 3. Fondo de cobertura con IA â?Lanzamiento con plantilla

Una plantilla TOML genera un equipo completo de inversiÃ³n con 7 agentes con un solo comando:

```bash
agentteam launch hedge-fund --team fund1 --goal "Analyze AAPL, MSFT, NVDA for Q2 2026"
```

5 agentes analistas (valor, crecimiento, tÃ©cnico, fundamentales, sentimiento) trabajan en paralelo. El gestor de riesgos sintetiza todas las seÃ±ales. El gestor de cartera toma las decisiones finales.

Las plantillas son archivos TOML â?**crea las tuyas** para cualquier dominio.

---

## CaracterÃ­sticas

<table>
<tr>
<td width="50%">

### Auto-organizaciÃ³n de agentes
- El lÃ­der genera y gestiona trabajadores
- Prompt de coordinaciÃ³n auto-inyectado â?cero configuraciÃ³n manual
- Los trabajadores auto-reportan estado e inactividad
- Cualquier agente CLI puede participar

### Aislamiento de espacio de trabajo
- Cada agente recibe su propio **git worktree**
- Sin conflictos de fusiÃ³n entre agentes en paralelo
- Comandos de checkpoint, fusiÃ³n y limpieza
- Nomenclatura de ramas: `agentteam/{team}/{agent}`

### Seguimiento de tareas con dependencias
- Kanban compartido: `pending` â?`in_progress` â?`completed` / `blocked`
- Cadenas `--blocked-by` con desbloqueo automÃ¡tico al completar
- `task wait` bloquea hasta que todas las tareas se completen

</td>
<td width="50%">

### MensajerÃ­a entre agentes
- Bandejas de entrada punto a punto (enviar, recibir, espiar)
- DifusiÃ³n a todos los miembros del equipo
- Transporte basado en archivos (por defecto) o ZeroMQ P2P

### Monitoreo y paneles
- `board show` â?kanban en terminal
- `board live` â?panel con actualizaciÃ³n automÃ¡tica
- `board attach` â?vista tmux en mosaico de todos los agentes
- `board serve` â?interfaz web con actualizaciones en tiempo real

### Plantillas de equipo
- Los archivos TOML definen arquetipos de equipo (roles, tareas, prompts)
- Un solo comando: `agentteam launch <template>`
- SustituciÃ³n de variables: `{goal}`, `{team_name}`, `{agent_name}`
- **AsignaciÃ³n de modelo por agente** (vista previa): asigna diferentes modelos a diferentes roles â?consulta [mÃ¡s abajo](#asignaciÃ³n-de-modelo-por-agente-vista-previa)

</td>
</tr>
</table>

**TambiÃ©n:** flujos de aprobaciÃ³n de planes, gestiÃ³n elegante del ciclo de vida, salida `--json` en todos los comandos, soporte multi-mÃ¡quina (NFS/SSHFS o P2P), espacios de nombres multi-usuario, validaciÃ³n de generaciÃ³n con reversiÃ³n automÃ¡tica, bloqueo de archivos `fcntl` para seguridad en concurrencia.

---

## IntegraciÃ³n con OpenClaw

Este fork hace de [OpenClaw](https://openclaw.ai) el **agente por defecto**. Sin AgentTeam, cada agente de OpenClaw trabaja de forma aislada. AgentTeam lo transforma en una plataforma multi-agente.

| Capacidad | OpenClaw solo | OpenClaw + AgentTeam |
|-----------|---------------|-------------------|
| **AsignaciÃ³n de tareas** | MensajerÃ­a manual por agente | El lÃ­der divide, asigna y monitorea autÃ³nomamente |
| **Desarrollo en paralelo** | Directorio de trabajo compartido | Git worktrees aislados por agente |
| **Dependencias** | Sondeo manual | `--blocked-by` con desbloqueo automÃ¡tico |
| **ComunicaciÃ³n** | Solo a travÃ©s del relay AGI | Bandeja de entrada directa punto a punto + difusiÃ³n |
| **Observabilidad** | Leer logs | Tablero kanban + vista tmux en mosaico |

Una vez instalado el skill, habla con tu bot de OpenClaw en cualquier canal:

| Lo que dices | Lo que sucede |
|-------------|-------------|
| "Crea un equipo de 5 agentes para construir una app web" | Crea equipo, tareas, genera 5 agentes en tmux |
| "Lanza un equipo de anÃ¡lisis de fondo de cobertura" | `agentteam launch hedge-fund` con 7 agentes |
| "Revisa el estado de mi equipo de agentes" | `agentteam board show` con salida kanban |

```
  You (Telegram/Discord/TUI)
         â?
         â?
  ââââââââââââââââââââ?
  â? OpenClaw Gateway â? â?activates agentteam skill
  ââââââââââ¬ââââââââââ?
           â?
           â?
  ââââââââââââââââââââ?    agentteam spawn     âââââââââââââââââââ?
  â? Leader Agent    â?ââââââââââââââââââââââ?â? openclaw tui   â?
  â? (openclaw)      â?âââ?                   â? (tmux window)  â?
  â?                 â?  â?                   â? git worktree   â?
  â? Manages swarm   â?  ââââââââââââââââââââ?âââââââââââââââââââ?
  â? via agentteam    â?  â?                   â? openclaw tui   â?
  â? CLI             â?  ââââââââââââââââââââ?âââââââââââââââââââ?
  ââââââââââââââââââââ?  â?                   â? openclaw tui   â?
                         ââââââââââââââââââââ?âââââââââââââââââââ?
                                               All coordinate via
                                               ~/.agentteam/ (tasks, inboxes)
```

---

## Arquitectura

```
  Human: "Optimize this LLM"
         â?
         â?
  ââââââââââââââââ?    agentteam spawn     ââââââââââââââââ?
  â? Leader      â?âââââââââââââââââââââââ?â? Worker      â?
  â? (any agent) â?âââââââ?               â? git worktree â?
  â?             â?      ââââââââââââââââ?â? tmux window  â?
  â? spawn       â?      â?               ââââââââââââââââ?
  â? task create â?      ââââââââââââââââ?â? Worker      â?
  â? inbox send  â?      â?               â? git worktree â?
  â? board show  â?      ââââââââââââââââ?â? tmux window  â?
  ââââââââââââââââ?                       ââââââââââââââââ?
                                                 â?
                                                 â?
                                      âââââââââââââââââââââââ?
                                      â?   ~/.agentteam/     â?
                                      â?âââ teams/   (who) â?
                                      â?âââ tasks/   (what)â?
                                      â?âââ inboxes/ (talk)â?
                                      â?âââ workspaces/    â?
                                      âââââââââââââââââââââââ?
```

Todo el estado se almacena en `~/.agentteam/` como archivos JSON. Sin base de datos, sin servidor. Las escrituras atÃ³micas con bloqueo de archivos `fcntl` garantizan seguridad ante fallos.

| ConfiguraciÃ³n | Variable de entorno | Valor por defecto |
|---------|---------|---------|
| Directorio de datos | `AgentTeam_DATA_DIR` | `~/.agentteam` |
| Transporte | `AgentTeam_TRANSPORT` | `file` |
| Modo de espacio de trabajo | `AgentTeam_WORKSPACE` | `auto` |
| Backend de generaciÃ³n | `AgentTeam_DEFAULT_BACKEND` | `tmux` |

---

## Referencia de comandos

<details open>
<summary><strong>Comandos principales</strong></summary>

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
<summary><strong>Espacio de trabajo, Plan, Ciclo de vida, ConfiguraciÃ³n</strong></summary>

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

## AsignaciÃ³n de modelo por agente (Vista previa)

> **Rama:** [`feat/per-agent-model-assignment`](https://github.com/win4r/AgentTeam-OpenClaw/tree/feat/per-agent-model-assignment)
>
> Esta funcionalidad estÃ¡ disponible para pruebas tempranas en una rama separada. Se fusionarÃ¡ en `main` una vez que se envÃ­e el flag `--model` complementario de OpenClaw.

Asigna diferentes modelos a diferentes roles de agente para mejores compromisos de costo/rendimiento en enjambres multi-agente.

```bash
# Install from the feature branch
pip install -e "git+https://github.com/win4r/AgentTeam-OpenClaw.git@feat/per-agent-model-assignment#egg=agentteam"
```

**Modelo por agente en plantillas:**
```toml
[template]
name = "my-team"
command = ["openclaw"]
model = "sonnet-4.6"              # default for all agents
model_strategy = "auto"           # or: leadersâstrong, workersâbalanced

[template.leader]
name = "lead"
model = "opus"                    # override for leader

[[template.agents]]
name = "worker"
model_tier = "cheap"              # cost tiers: strong / balanced / cheap
```

**Flags del CLI:**
```bash
agentteam spawn --model opus                          # single agent
agentteam launch my-template --model gpt-5.4          # override all agents
agentteam launch my-template --model-strategy auto     # auto-assign by role
```

Consulta el [issue #1](https://github.com/win4r/AgentTeam-OpenClaw/issues/1) para la solicitud de funcionalidad completa y la discusiÃ³n.

---

## Hoja de ruta

| VersiÃ³n | QuÃ© | Estado |
|---------|------|--------|
| v0.3 | Transporte de archivos + P2P, interfaz web, multi-usuario, plantillas | Publicado |
| v0.4 | Transporte Redis â?mensajerÃ­a entre mÃ¡quinas | Planificado |
| v0.5 | Capa de estado compartido â?configuraciÃ³n de equipo entre mÃ¡quinas | Planificado |
| v0.6 | Mercado de agentes â?plantillas de la comunidad | En exploraciÃ³n |
| v0.7 | ProgramaciÃ³n adaptativa â?reasignaciÃ³n dinÃ¡mica de tareas | En exploraciÃ³n |
| v1.0 | Nivel de producciÃ³n â?autenticaciÃ³n, permisos, logs de auditorÃ­a | En exploraciÃ³n |

---

## Contribuir

Damos la bienvenida a contribuciones:

- **Integraciones de agentes** â?soporte para mÃ¡s agentes CLI
- **Plantillas de equipo** â?plantillas TOML para nuevos dominios
- **Backends de transporte** â?Redis, NATS, etc.
- **Mejoras del panel** â?interfaz web, Grafana
- **DocumentaciÃ³n** â?tutoriales y mejores prÃ¡cticas

---

## Agradecimientos

- [@karpathy/autoresearch](https://github.com/karpathy/autoresearch) â?framework de investigaciÃ³n autÃ³noma de ML
- [OpenClaw](https://openclaw.ai) â?backend de agente por defecto
- [Claude Code](https://claude.ai/claude-code) y [Codex](https://openai.com/codex) â?agentes de codificaciÃ³n con IA soportados
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) â?inspiraciÃ³n para la plantilla de fondo de cobertura
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) â?proyecto hermano

## Licencia

MIT â?libre para usar, modificar y distribuir.

---

<div align="center">

**AgentTeam** â?*Inteligencia de enjambre de agentes.*

</div>
