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
  <strong>Coordinación de enjambre multi-agente para agentes de codificación CLI �?<a href="https://openclaw.ai">OpenClaw</a> por defecto</strong>
</p>

<p align="center">
  <a href="https://github.com/HKUDS/AgentTeam"><img src="https://img.shields.io/badge/upstream-HKUDS%2FAgentTeam-purple?style=for-the-badge" alt="Upstream"></a>
  <a href="#-inicio-rápido"><img src="https://img.shields.io/badge/Quick_Start-3_min-blue?style=for-the-badge" alt="Inicio rápido"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="Licencia"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-�?.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/agents-OpenClaw_%7C_Claude_Code_%7C_Codex_%7C_nanobot-blueviolet" alt="Agents">
  <img src="https://img.shields.io/badge/transport-File_%7C_ZeroMQ_P2P-orange" alt="Transport">
  <img src="https://img.shields.io/badge/version-0.3.0-teal" alt="Version">
</p>

> **Fork de [HKUDS/AgentTeam](https://github.com/HKUDS/AgentTeam)** con integración profunda de OpenClaw: agente `openclaw` por defecto, aislamiento de sesión por agente, autoconfiguración de aprobación de ejecución y backends de creación endurecidos para producción. Todas las correcciones del upstream se sincronizan.

Tú defines el objetivo. El enjambre de agentes se encarga del resto �?generando trabajadores, dividiendo tareas, coordinando y fusionando resultados.

Funciona con [OpenClaw](https://openclaw.ai) (por defecto), [Claude Code](https://claude.ai/claude-code), [Codex](https://openai.com/codex), [nanobot](https://github.com/HKUDS/nanobot), [Cursor](https://cursor.com) y cualquier agente CLI.

---

## ¿Por qué AgentTeam?

Los agentes de IA actuales son potentes pero trabajan de forma **aislada**. AgentTeam permite que los agentes se auto-organicen en equipos �?dividiendo trabajo, comunicándose y convergiendo en resultados sin microgestión humana.

| | AgentTeam | Otros frameworks multi-agente |
|---|---------|----------------------------|
| **Quién lo usa** | Los propios agentes de IA | Humanos escribiendo código de orquestación |
| **Configuración** | `pip install` + un prompt | Docker, APIs en la nube, configuraciones YAML |
| **Infraestructura** | Sistema de archivos + tmux | Redis, colas de mensajes, bases de datos |
| **Soporte de agentes** | Cualquier agente CLI | Solo específico del framework |
| **Aislamiento** | Git worktrees (ramas reales) | Contenedores o entornos virtuales |

---

## Cómo funciona

<table>
<tr>
<td width="33%">

### Los agentes generan agentes
El líder llama a `agentteam spawn` para crear trabajadores. Cada uno recibe su propio **git worktree**, **ventana tmux** e **identidad**.

```bash
agentteam spawn --team my-team \
  --agent-name worker1 \
  --task "Implement auth module"
```

</td>
<td width="33%">

### Los agentes se comunican
Los trabajadores revisan bandejas de entrada, actualizan tareas e informan resultados �?todo mediante comandos CLI **auto-inyectados** en su prompt.

```bash
agentteam task list my-team --owner me
agentteam inbox send my-team leader \
  "Auth done. All tests passing."
```

</td>
<td width="33%">

### Solo observa
Monitorea el enjambre desde una vista tmux en mosaico o la interfaz web. El líder gestiona la coordinación.

```bash
agentteam board attach my-team
# Or web dashboard
agentteam board serve --port 8080
```

</td>
</tr>
</table>

---

## Inicio rápido

### Opción 1: Deja que el agente conduzca (Recomendado)

Instala AgentTeam, luego indica a tu agente:

```
"Build a web app. Use agentteam to split the work across multiple agents."
```

El agente crea automáticamente un equipo, genera trabajadores, asigna tareas y coordina �?todo a través del CLI `agentteam`.

### Opción 2: Condúcelo manualmente

```bash
# Create a team
agentteam team spawn-team my-team -d "Build the auth module" -n leader

# Spawn workers �?each gets a git worktree + tmux window
agentteam spawn --team my-team --agent-name alice --task "Implement OAuth2 flow"
agentteam spawn --team my-team --agent-name bob   --task "Write unit tests for auth"

# Watch them work
agentteam board attach my-team
```

### Agentes soportados

| Agente | Comando de generación | Estado |
|-------|--------------|--------|
| [OpenClaw](https://openclaw.ai) | `agentteam spawn tmux openclaw --team ...` | **Por defecto** |
| [Claude Code](https://claude.ai/claude-code) | `agentteam spawn tmux claude --team ...` | Soporte completo |
| [Codex](https://openai.com/codex) | `agentteam spawn tmux codex --team ...` | Soporte completo |
| [nanobot](https://github.com/HKUDS/nanobot) | `agentteam spawn tmux nanobot --team ...` | Soporte completo |
| [Cursor](https://cursor.com) | `agentteam spawn subprocess cursor --team ...` | Experimental |
| Scripts personalizados | `agentteam spawn subprocess python --team ...` | Soporte completo |

---

## Instalación

### Paso 1: Requisitos previos

AgentTeam requiere **Python 3.10+**, **tmux** y al menos un agente de codificación CLI (OpenClaw, Claude Code, Codex, etc.).

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

> Si usas Claude Code o Codex en lugar de OpenClaw, instálalos según su propia documentación. OpenClaw es el predeterminado pero no es estrictamente obligatorio.

### Paso 2: Instalar AgentTeam

> **⚠️ NO ejecutes `pip install agentteam` ni `npm install -g agentteam` directamente:**
> - `pip install agentteam` instala la versión upstream de PyPI, que usa `claude` por defecto y carece de adaptaciones OpenClaw.
> - `npm install -g agentteam` instala un paquete usurpador sin relación (publicado por `a9logic`). Si `agentteam --version` muestra "Coming Soon", es el paquete incorrecto. Ejecuta primero `npm uninstall -g agentteam`.
>
> **Usa los tres comandos de abajo �?el `pip install -e .` después del clone es obligatorio. Instala desde el repositorio local, no desde PyPI.**

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
pip install -e .    # �?¡Obligatorio! Instala desde el repositorio local, NO es lo mismo que pip install agentteam
```

Opcional �?transporte P2P (ZeroMQ):

```bash
pip install -e ".[p2p]"
```

### Paso 3: Crear el enlace simbólico `~/bin/AgentTeam`

Los agentes generados se ejecutan en shells nuevos que pueden no tener el directorio bin de pip en PATH. Un enlace simbólico en `~/bin` asegura que `agentteam` siempre sea accesible:

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

Luego asegúrate de que `~/bin` esté en tu PATH �?añade esto a `~/.zshrc` o `~/.bashrc` si no lo está:

```bash
export PATH="$HOME/bin:$PATH"
```

### Paso 4: Instalar el skill de OpenClaw (solo usuarios de OpenClaw)

El archivo de skill enseña a los agentes de OpenClaw cómo usar AgentTeam a través de lenguaje natural. Omite este paso si no usas OpenClaw.

```bash
mkdir -p ~/.openclaw/workspace/skills/AgentTeam
cp skills/openclaw/SKILL.md ~/.openclaw/workspace/skills/AgentTeam/SKILL.md
```

### Paso 5: Configurar aprobaciones de ejecución (solo usuarios de OpenClaw)

Los agentes de OpenClaw generados necesitan permiso para ejecutar comandos `agentteam`. Sin esto, los agentes se bloquearán en prompts interactivos de permisos.

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

> Si `openclaw approvals` falla, es posible que el gateway de OpenClaw no esté en ejecución. Inícialo primero y luego reintenta.

### Paso 6: Verificar

```bash
agentteam --version          # Should print version
agentteam config health      # Should show all green
```

Si usas OpenClaw, verifica también que el skill esté cargado:

```bash
openclaw skills list | grep agentteam
```

### Instalador automático

Los pasos 2 a 6 anteriores también están disponibles como un único script:

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
bash scripts/install-openclaw.sh
```

### Solución de problemas

| Problema | Causa | Solución |
|---------|-------|-----|
| `agentteam: command not found` | El directorio bin de pip no está en PATH | Ejecuta el Paso 3 (enlace simbólico + PATH) |
| Los agentes generados no encuentran `agentteam` | Los agentes se ejecutan en shells nuevos sin PATH de pip | Verifica que el enlace simbólico `~/bin/AgentTeam` exista y que `~/bin` esté en PATH |
| `openclaw approvals` falla | El gateway no está en ejecución | Inicia `openclaw gateway` primero, luego reintenta el Paso 5 |
| `exec-approvals.json not found` | OpenClaw nunca se ejecutó | Ejecuta `openclaw` una vez para generar la configuración, luego reintenta el Paso 5 |
| Los agentes se bloquean en prompts de permisos | La seguridad de aprobaciones de ejecución está en "full" | Ejecuta el Paso 5 para cambiar a "allowlist" |
| `pip install -e .` falla | Faltan dependencias de compilación | Ejecuta `pip install hatchling` primero |
| `agentteam --version` muestra "Coming Soon" | Se instaló el paquete npm usurpador (`a9logic`, sin relación con este proyecto) | `npm uninstall -g agentteam`, luego reinstalar según el paso 2 |

---

## Casos de uso

### 1. Investigación autónoma de ML �?8 agentes x 8 GPUs

Basado en [@karpathy/autoresearch](https://github.com/karpathy/autoresearch). Un solo prompt lanza 8 agentes de investigación a través de H100s que diseñan más de 2000 experimentos de forma autónoma.

```
Humano: "Use 8 GPUs to optimize train.py. Read program.md for instructions."

Agente líder:
├── Genera 8 agentes, cada uno asignado a una dirección de investigación (profundidad, ancho, LR, tamaño de lote...)
├── Cada agente recibe su propio git worktree para experimentos aislados
├── Cada 30 min: revisa resultados, poliniza las mejores configuraciones a nuevos agentes
├── Reasigna GPUs cuando los agentes terminan �?nuevos agentes parten de la mejor configuración conocida
└── Resultado: val_bpb 1.044 �?0.977 (mejora del 6.4%) en 2430 experimentos en ~30 horas-GPU
```

Resultados completos: [novix-science/autoresearch](https://github.com/novix-science/autoresearch)

### 2. Ingeniería de software agéntica

```
Humano: "Build a full-stack todo app with auth, database, and React frontend."

Agente líder:
├── Crea tareas con cadenas de dependencias (esquema API �?auth + BD �?frontend �?pruebas)
├── Genera 5 agentes (arquitecto, 2 backend, frontend, tester) en worktrees separados
├── Las dependencias se resuelven automáticamente: arquitecto completa �?backend se desbloquea �?tester se desbloquea
├── Los agentes coordinan vía bandeja de entrada: "Aquí está la especificación OpenAPI", "Endpoints de auth listos"
└── El líder fusiona todos los worktrees en main cuando se completa
```

### 3. Fondo de cobertura con IA �?Lanzamiento con plantilla

Una plantilla TOML genera un equipo completo de inversión con 7 agentes con un solo comando:

```bash
agentteam launch hedge-fund --team fund1 --goal "Analyze AAPL, MSFT, NVDA for Q2 2026"
```

5 agentes analistas (valor, crecimiento, técnico, fundamentales, sentimiento) trabajan en paralelo. El gestor de riesgos sintetiza todas las señales. El gestor de cartera toma las decisiones finales.

Las plantillas son archivos TOML �?**crea las tuyas** para cualquier dominio.

---

## Características

<table>
<tr>
<td width="50%">

### Auto-organización de agentes
- El líder genera y gestiona trabajadores
- Prompt de coordinación auto-inyectado �?cero configuración manual
- Los trabajadores auto-reportan estado e inactividad
- Cualquier agente CLI puede participar

### Aislamiento de espacio de trabajo
- Cada agente recibe su propio **git worktree**
- Sin conflictos de fusión entre agentes en paralelo
- Comandos de checkpoint, fusión y limpieza
- Nomenclatura de ramas: `agentteam/{team}/{agent}`

### Seguimiento de tareas con dependencias
- Kanban compartido: `pending` �?`in_progress` �?`completed` / `blocked`
- Cadenas `--blocked-by` con desbloqueo automático al completar
- `task wait` bloquea hasta que todas las tareas se completen

</td>
<td width="50%">

### Mensajería entre agentes
- Bandejas de entrada punto a punto (enviar, recibir, espiar)
- Difusión a todos los miembros del equipo
- Transporte basado en archivos (por defecto) o ZeroMQ P2P

### Monitoreo y paneles
- `board show` �?kanban en terminal
- `board live` �?panel con actualización automática
- `board attach` �?vista tmux en mosaico de todos los agentes
- `board serve` �?interfaz web con actualizaciones en tiempo real

### Plantillas de equipo
- Los archivos TOML definen arquetipos de equipo (roles, tareas, prompts)
- Un solo comando: `agentteam launch <template>`
- Sustitución de variables: `{goal}`, `{team_name}`, `{agent_name}`
- **Asignación de modelo por agente** (vista previa): asigna diferentes modelos a diferentes roles �?consulta [más abajo](#asignación-de-modelo-por-agente-vista-previa)

</td>
</tr>
</table>

**También:** flujos de aprobación de planes, gestión elegante del ciclo de vida, salida `--json` en todos los comandos, soporte multi-máquina (NFS/SSHFS o P2P), espacios de nombres multi-usuario, validación de generación con reversión automática, bloqueo de archivos `fcntl` para seguridad en concurrencia.

---

## Integración con OpenClaw

Este fork hace de [OpenClaw](https://openclaw.ai) el **agente por defecto**. Sin AgentTeam, cada agente de OpenClaw trabaja de forma aislada. AgentTeam lo transforma en una plataforma multi-agente.

| Capacidad | OpenClaw solo | OpenClaw + AgentTeam |
|-----------|---------------|-------------------|
| **Asignación de tareas** | Mensajería manual por agente | El líder divide, asigna y monitorea autónomamente |
| **Desarrollo en paralelo** | Directorio de trabajo compartido | Git worktrees aislados por agente |
| **Dependencias** | Sondeo manual | `--blocked-by` con desbloqueo automático |
| **Comunicación** | Solo a través del relay AGI | Bandeja de entrada directa punto a punto + difusión |
| **Observabilidad** | Leer logs | Tablero kanban + vista tmux en mosaico |

Una vez instalado el skill, habla con tu bot de OpenClaw en cualquier canal:

| Lo que dices | Lo que sucede |
|-------------|-------------|
| "Crea un equipo de 5 agentes para construir una app web" | Crea equipo, tareas, genera 5 agentes en tmux |
| "Lanza un equipo de análisis de fondo de cobertura" | `agentteam launch hedge-fund` con 7 agentes |
| "Revisa el estado de mi equipo de agentes" | `agentteam board show` con salida kanban |

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

## Arquitectura

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

Todo el estado se almacena en `~/.agentteam/` como archivos JSON. Sin base de datos, sin servidor. Las escrituras atómicas con bloqueo de archivos `fcntl` garantizan seguridad ante fallos.

| Configuración | Variable de entorno | Valor por defecto |
|---------|---------|---------|
| Directorio de datos | `AgentTeam_DATA_DIR` | `~/.agentteam` |
| Transporte | `AgentTeam_TRANSPORT` | `file` |
| Modo de espacio de trabajo | `AgentTeam_WORKSPACE` | `auto` |
| Backend de generación | `AgentTeam_DEFAULT_BACKEND` | `tmux` |

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
<summary><strong>Espacio de trabajo, Plan, Ciclo de vida, Configuración</strong></summary>

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

## Asignación de modelo por agente (Vista previa)

> **Rama:** [`feat/per-agent-model-assignment`](https://github.com/win4r/AgentTeam-OpenClaw/tree/feat/per-agent-model-assignment)
>
> Esta funcionalidad está disponible para pruebas tempranas en una rama separada. Se fusionará en `main` una vez que se envíe el flag `--model` complementario de OpenClaw.

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
model_strategy = "auto"           # or: leaders→strong, workers→balanced

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

Consulta el [issue #1](https://github.com/win4r/AgentTeam-OpenClaw/issues/1) para la solicitud de funcionalidad completa y la discusión.

---

## Hoja de ruta

| Versión | Qué | Estado |
|---------|------|--------|
| v0.3 | Transporte de archivos + P2P, interfaz web, multi-usuario, plantillas | Publicado |
| v0.4 | Transporte Redis �?mensajería entre máquinas | Planificado |
| v0.5 | Capa de estado compartido �?configuración de equipo entre máquinas | Planificado |
| v0.6 | Mercado de agentes �?plantillas de la comunidad | En exploración |
| v0.7 | Programación adaptativa �?reasignación dinámica de tareas | En exploración |
| v1.0 | Nivel de producción �?autenticación, permisos, logs de auditoría | En exploración |

---

## Contribuir

Damos la bienvenida a contribuciones:

- **Integraciones de agentes** �?soporte para más agentes CLI
- **Plantillas de equipo** �?plantillas TOML para nuevos dominios
- **Backends de transporte** �?Redis, NATS, etc.
- **Mejoras del panel** �?interfaz web, Grafana
- **Documentación** �?tutoriales y mejores prácticas

---

## Agradecimientos

- [@karpathy/autoresearch](https://github.com/karpathy/autoresearch) �?framework de investigación autónoma de ML
- [OpenClaw](https://openclaw.ai) �?backend de agente por defecto
- [Claude Code](https://claude.ai/claude-code) y [Codex](https://openai.com/codex) �?agentes de codificación con IA soportados
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) �?inspiración para la plantilla de fondo de cobertura
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) �?proyecto hermano

## Licencia

MIT �?libre para usar, modificar y distribuir.

---

<div align="center">

**AgentTeam** �?*Inteligencia de enjambre de agentes.*

</div>
