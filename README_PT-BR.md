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
  <strong>CoordenaÃ§Ã£o de enxame multi-agente para agentes de codificaÃ§Ã£o CLI â?<a href="https://openclaw.ai">OpenClaw</a> como padrÃ£o</strong>
</p>

<p align="center">
  <a href="https://github.com/HKUDS/AgentTeam"><img src="https://img.shields.io/badge/upstream-HKUDS%2FAgentTeam-purple?style=for-the-badge" alt="Upstream"></a>
  <a href="#-inÃ­cio-rÃ¡pido"><img src="https://img.shields.io/badge/Quick_Start-3_min-blue?style=for-the-badge" alt="InÃ­cio RÃ¡pido"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="LicenÃ§a"></a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-â?.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/agents-OpenClaw_%7C_Claude_Code_%7C_Codex_%7C_nanobot-blueviolet" alt="Agents">
  <img src="https://img.shields.io/badge/transport-File_%7C_ZeroMQ_P2P-orange" alt="Transport">
  <img src="https://img.shields.io/badge/version-0.3.0-teal" alt="Version">
</p>

> **Fork de [HKUDS/AgentTeam](https://github.com/HKUDS/AgentTeam)** com integraÃ§Ã£o profunda ao OpenClaw: agente `openclaw` como padrÃ£o, isolamento de sessÃ£o por agente, autoconfiguraÃ§Ã£o de aprovaÃ§Ã£o de execuÃ§Ã£o e backends de spawn robustecidos para produÃ§Ã£o. Todas as correÃ§Ãµes do upstream sÃ£o sincronizadas.

VocÃª define o objetivo. O enxame de agentes cuida do resto â?criando workers, dividindo tarefas, coordenando e mesclando resultados.

Funciona com [OpenClaw](https://openclaw.ai) (padrÃ£o), [Claude Code](https://claude.ai/claude-code), [Codex](https://openai.com/codex), [nanobot](https://github.com/HKUDS/nanobot), [Cursor](https://cursor.com) e qualquer agente CLI.

---

## Por que AgentTeam?

Os agentes de IA atuais sÃ£o poderosos, mas trabalham de forma **isolada**. O AgentTeam permite que os agentes se auto-organizem em equipes â?dividindo trabalho, comunicando-se e convergindo em resultados sem microgerenciamento humano.

| | AgentTeam | Outros frameworks multi-agente |
|---|---------|----------------------------|
| **Quem usa** | Os prÃ³prios agentes de IA | Humanos escrevendo cÃ³digo de orquestraÃ§Ã£o |
| **ConfiguraÃ§Ã£o** | `pip install` + um prompt | Docker, APIs na nuvem, configs YAML |
| **Infraestrutura** | Sistema de arquivos + tmux | Redis, filas de mensagens, bancos de dados |
| **Suporte a agentes** | Qualquer agente CLI | Apenas especÃ­ficos do framework |
| **Isolamento** | Git worktrees (branches reais) | Containers ou ambientes virtuais |

---

## Como funciona

<table>
<tr>
<td width="33%">

### Agentes geram agentes
O lÃ­der chama `agentteam spawn` para criar workers. Cada um recebe sua prÃ³pria **git worktree**, **janela tmux** e **identidade**.

```bash
agentteam spawn --team my-team \
  --agent-name worker1 \
  --task "Implement auth module"
```

</td>
<td width="33%">

### Agentes conversam entre si
Workers verificam caixas de entrada, atualizam tarefas e reportam resultados â?tudo atravÃ©s de comandos CLI **auto-injetados** no prompt.

```bash
agentteam task list my-team --owner me
agentteam inbox send my-team leader \
  "Auth done. All tests passing."
```

</td>
<td width="33%">

### VocÃª sÃ³ observa
Monitore o enxame a partir de uma visualizaÃ§Ã£o tmux em mosaico ou da Interface Web. O lÃ­der cuida da coordenaÃ§Ã£o.

```bash
agentteam board attach my-team
# Or web dashboard
agentteam board serve --port 8080
```

</td>
</tr>
</table>

---

## InÃ­cio rÃ¡pido

### OpÃ§Ã£o 1: Deixe o agente conduzir (Recomendado)

Instale o AgentTeam e depois dÃª o prompt ao seu agente:

```
"Build a web app. Use agentteam to split the work across multiple agents."
```

O agente cria automaticamente uma equipe, gera workers, atribui tarefas e coordena â?tudo via CLI `agentteam`.

### OpÃ§Ã£o 2: Conduza manualmente

```bash
# Create a team
agentteam team spawn-team my-team -d "Build the auth module" -n leader

# Spawn workers â?each gets a git worktree + tmux window
agentteam spawn --team my-team --agent-name alice --task "Implement OAuth2 flow"
agentteam spawn --team my-team --agent-name bob   --task "Write unit tests for auth"

# Watch them work
agentteam board attach my-team
```

### Agentes suportados

| Agente | Comando de spawn | Status |
|-------|--------------|--------|
| [OpenClaw](https://openclaw.ai) | `agentteam spawn tmux openclaw --team ...` | **PadrÃ£o** |
| [Claude Code](https://claude.ai/claude-code) | `agentteam spawn tmux claude --team ...` | Suporte completo |
| [Codex](https://openai.com/codex) | `agentteam spawn tmux codex --team ...` | Suporte completo |
| [nanobot](https://github.com/HKUDS/nanobot) | `agentteam spawn tmux nanobot --team ...` | Suporte completo |
| [Cursor](https://cursor.com) | `agentteam spawn subprocess cursor --team ...` | Experimental |
| Scripts personalizados | `agentteam spawn subprocess python --team ...` | Suporte completo |

---

## InstalaÃ§Ã£o

### Passo 1: PrÃ©-requisitos

O AgentTeam requer **Python 3.10+**, **tmux** e pelo menos um agente de codificaÃ§Ã£o CLI (OpenClaw, Claude Code, Codex, etc.).

**Verifique o que vocÃª jÃ¡ tem:**

```bash
python3 --version   # Need 3.10+
tmux -V             # Need any version
openclaw --version  # Or: claude --version / codex --version
```

**Instale os prÃ©-requisitos faltantes:**

| Ferramenta | macOS | Ubuntu/Debian |
|------|-------|---------------|
| Python 3.10+ | `brew install python@3.12` | `sudo apt update && sudo apt install python3 python3-pip` |
| tmux | `brew install tmux` | `sudo apt install tmux` |
| OpenClaw | `pip install openclaw` | `pip install openclaw` |

> Se estiver usando Claude Code ou Codex em vez de OpenClaw, instale-os conforme suas respectivas documentaÃ§Ãµes. OpenClaw Ã© o padrÃ£o, mas nÃ£o Ã© estritamente obrigatÃ³rio.

### Passo 2: Instalar o AgentTeam

> **â ï¸ NÃO execute `pip install agentteam` ou `npm install -g agentteam` diretamente:**
> - `pip install agentteam` instala a versÃ£o upstream do PyPI, que usa `claude` como padrÃ£o e nÃ£o possui adaptaÃ§Ãµes OpenClaw.
> - `npm install -g agentteam` instala um pacote usurpador sem relaÃ§Ã£o (publicado por `a9logic`). Se `agentteam --version` mostrar "Coming Soon", Ã© o pacote errado. Execute primeiro `npm uninstall -g agentteam`.
>
> **Use os trÃªs comandos abaixo â?o `pip install -e .` apÃ³s o clone Ã© obrigatÃ³rio. Ele instala a partir do repositÃ³rio local, nÃ£o do PyPI.**

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
pip install -e .    # â?ObrigatÃ³rio! Instala do repositÃ³rio local, NÃO Ã© o mesmo que pip install agentteam
```

Opcional â?Transporte P2P (ZeroMQ):

```bash
pip install -e ".[p2p]"
```

### Passo 3: Criar o symlink `~/bin/AgentTeam`

Agentes criados rodam em shells novos que podem nÃ£o ter o diretÃ³rio bin do pip no PATH. Um symlink em `~/bin` garante que o `agentteam` esteja sempre acessÃ­vel:

```bash
mkdir -p ~/bin
ln -sf "$(which agentteam)" ~/bin/AgentTeam
```

Se `which agentteam` nÃ£o retornar nada, encontre o binÃ¡rio manualmente:

```bash
# Common locations:
# ~/.local/bin/AgentTeam
# /opt/homebrew/bin/AgentTeam
# /usr/local/bin/AgentTeam
# /Library/Frameworks/Python.framework/Versions/3.*/bin/AgentTeam
find / -name agentteam -type f 2>/dev/null | head -5
```

Depois certifique-se de que `~/bin` esteja no seu PATH â?adicione isso ao `~/.zshrc` ou `~/.bashrc` se ainda nÃ£o estiver:

```bash
export PATH="$HOME/bin:$PATH"
```

### Passo 4: Instalar a skill do OpenClaw (apenas para usuÃ¡rios do OpenClaw)

O arquivo de skill ensina os agentes OpenClaw a usar o AgentTeam atravÃ©s de linguagem natural. Pule este passo se nÃ£o estiver usando OpenClaw.

```bash
mkdir -p ~/.openclaw/workspace/skills/AgentTeam
cp skills/openclaw/SKILL.md ~/.openclaw/workspace/skills/AgentTeam/SKILL.md
```

### Passo 5: Configurar aprovaÃ§Ãµes de execuÃ§Ã£o (apenas para usuÃ¡rios do OpenClaw)

Agentes OpenClaw criados precisam de permissÃ£o para executar comandos `agentteam`. Sem isso, os agentes ficarÃ£o bloqueados em prompts interativos de permissÃ£o.

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

> Se `openclaw approvals` falhar, o gateway do OpenClaw pode nÃ£o estar em execuÃ§Ã£o. Inicie-o primeiro e tente novamente.

### Passo 6: Verificar

```bash
agentteam --version          # Should print version
agentteam config health      # Should show all green
```

Se estiver usando OpenClaw, verifique tambÃ©m se a skill foi carregada:

```bash
openclaw skills list | grep agentteam
```

### Instalador automÃ¡tico

Os passos 2 a 6 acima tambÃ©m estÃ£o disponÃ­veis como um Ãºnico script:

```bash
git clone https://github.com/win4r/AgentTeam-OpenClaw.git
cd AgentTeam-OpenClaw
bash scripts/install-openclaw.sh
```

### SoluÃ§Ã£o de problemas

| Problema | Causa | SoluÃ§Ã£o |
|---------|-------|-----|
| `agentteam: command not found` | DiretÃ³rio bin do pip nÃ£o estÃ¡ no PATH | Execute o Passo 3 (symlink + PATH) |
| Agentes criados nÃ£o encontram o `agentteam` | Agentes rodam em shells novos sem o PATH do pip | Verifique se o symlink `~/bin/AgentTeam` existe e se `~/bin` estÃ¡ no PATH |
| `openclaw approvals` falha | Gateway nÃ£o estÃ¡ em execuÃ§Ã£o | Inicie o `openclaw gateway` primeiro e repita o Passo 5 |
| `exec-approvals.json not found` | OpenClaw nunca foi executado | Execute `openclaw` uma vez para gerar a configuraÃ§Ã£o e repita o Passo 5 |
| Agentes bloqueiam em prompts de permissÃ£o | SeguranÃ§a de aprovaÃ§Ã£o de execuÃ§Ã£o estÃ¡ em "full" | Execute o Passo 5 para mudar para "allowlist" |
| `pip install -e .` falha | DependÃªncias de build ausentes | Execute `pip install hatchling` primeiro |
| `agentteam --version` mostra "Coming Soon" | Pacote npm usurpador instalado por engano (`a9logic`, sem relaÃ§Ã£o com este projeto) | `npm uninstall -g agentteam`, depois reinstalar conforme o passo 2 |

---

## Casos de uso

### 1. Pesquisa autÃ´noma de ML â?8 agentes x 8 GPUs

Baseado em [@karpathy/autoresearch](https://github.com/karpathy/autoresearch). Um Ãºnico prompt lanÃ§a 8 agentes de pesquisa em H100s que projetam mais de 2000 experimentos de forma autÃ´noma.

```
Human: "Use 8 GPUs to optimize train.py. Read program.md for instructions."

Leader agent:
âââ Spawns 8 agents, each assigned a research direction (depth, width, LR, batch size...)
âââ Each agent gets its own git worktree for isolated experiments
âââ Every 30 min: checks results, cross-pollinates best configs to new agents
âââ Reassigns GPUs as agents finish â?fresh agents start from best known config
âââ Result: val_bpb 1.044 â?0.977 (6.4% improvement) across 2430 experiments in ~30 GPU-hours
```

Resultados completos: [novix-science/autoresearch](https://github.com/novix-science/autoresearch)

### 2. Engenharia de software agÃªntica

```
Human: "Build a full-stack todo app with auth, database, and React frontend."

Leader agent:
âââ Creates tasks with dependency chains (API schema â?auth + DB â?frontend â?tests)
âââ Spawns 5 agents (architect, 2 backend, frontend, tester) in separate worktrees
âââ Dependencies auto-resolve: architect completes â?backend unblocks â?tester unblocks
âââ Agents coordinate via inbox: "Here's the OpenAPI spec", "Auth endpoints ready"
âââ Leader merges all worktrees into main when complete
```

### 3. Fundo de investimento com IA â?LanÃ§amento via template

Um template TOML gera uma equipe completa de 7 agentes de investimento com um Ãºnico comando:

```bash
agentteam launch hedge-fund --team fund1 --goal "Analyze AAPL, MSFT, NVDA for Q2 2026"
```

5 agentes analistas (valor, crescimento, tÃ©cnico, fundamentalista, sentimento) trabalham em paralelo. O gerente de risco sintetiza todos os sinais. O gerente de portfÃ³lio toma as decisÃµes finais.

Templates sÃ£o arquivos TOML â?**crie os seus prÃ³prios** para qualquer domÃ­nio.

---

## Funcionalidades

<table>
<tr>
<td width="50%">

### Auto-organizaÃ§Ã£o de agentes
- O lÃ­der cria e gerencia workers
- Prompt de coordenaÃ§Ã£o auto-injetado â?zero configuraÃ§Ã£o manual
- Workers reportam automaticamente status e estado ocioso
- Qualquer agente CLI pode participar

### Isolamento de workspace
- Cada agente recebe sua prÃ³pria **git worktree**
- Sem conflitos de merge entre agentes paralelos
- Comandos de checkpoint, merge e limpeza
- Nomenclatura de branches: `agentteam/{team}/{agent}`

### Rastreamento de tarefas com dependÃªncias
- Kanban compartilhado: `pending` â?`in_progress` â?`completed` / `blocked`
- Cadeias `--blocked-by` com desbloqueio automÃ¡tico ao completar
- `task wait` bloqueia atÃ© que todas as tarefas sejam concluÃ­das

</td>
<td width="50%">

### Mensagens entre agentes
- Caixas de entrada ponto-a-ponto (enviar, receber, espiar)
- Broadcast para todos os membros da equipe
- Transporte baseado em arquivo (padrÃ£o) ou ZeroMQ P2P

### Monitoramento e painÃ©is
- `board show` â?kanban no terminal
- `board live` â?painel com atualizaÃ§Ã£o automÃ¡tica
- `board attach` â?visualizaÃ§Ã£o tmux em mosaico de todos os agentes
- `board serve` â?Interface Web com atualizaÃ§Ãµes em tempo real

### Templates de equipe
- Arquivos TOML definem arquÃ©tipos de equipe (papÃ©is, tarefas, prompts)
- Um comando: `agentteam launch <template>`
- SubstituiÃ§Ã£o de variÃ¡veis: `{goal}`, `{team_name}`, `{agent_name}`
- **AtribuiÃ§Ã£o de modelo por agente** (prÃ©via): atribua modelos diferentes a papÃ©is diferentes â?veja [abaixo](#atribuiÃ§Ã£o-de-modelo-por-agente-prÃ©via)

</td>
</tr>
</table>

**TambÃ©m:** fluxos de aprovaÃ§Ã£o de planos, gerenciamento gracioso de ciclo de vida, saÃ­da `--json` em todos os comandos, suporte entre mÃ¡quinas (NFS/SSHFS ou P2P), namespacing multi-usuÃ¡rio, validaÃ§Ã£o de spawn com rollback automÃ¡tico, travamento de arquivos `fcntl` para seguranÃ§a em concorrÃªncia.

---

## IntegraÃ§Ã£o com OpenClaw

Este fork torna o [OpenClaw](https://openclaw.ai) o **agente padrÃ£o**. Sem o AgentTeam, cada agente OpenClaw trabalha isoladamente. O AgentTeam o transforma em uma plataforma multi-agente.

| Capacidade | OpenClaw sozinho | OpenClaw + AgentTeam |
|-----------|---------------|-------------------|
| **AtribuiÃ§Ã£o de tarefas** | Mensagens manuais por agente | O lÃ­der divide, atribui e monitora autonomamente |
| **Desenvolvimento paralelo** | DiretÃ³rio de trabalho compartilhado | Git worktrees isoladas por agente |
| **DependÃªncias** | Polling manual | `--blocked-by` com desbloqueio automÃ¡tico |
| **ComunicaÃ§Ã£o** | Apenas atravÃ©s do relay AGI | Caixa de entrada ponto-a-ponto direta + broadcast |
| **Observabilidade** | Ler logs | Quadro kanban + visualizaÃ§Ã£o tmux em mosaico |

ApÃ³s a skill ser instalada, converse com seu bot OpenClaw em qualquer canal:

| O que vocÃª diz | O que acontece |
|-------------|-------------|
| "Crie uma equipe de 5 agentes para construir um app web" | Cria equipe, tarefas e gera 5 agentes no tmux |
| "Lance uma equipe de anÃ¡lise de fundo de investimento" | `agentteam launch hedge-fund` com 7 agentes |
| "Verifique o status da minha equipe de agentes" | `agentteam board show` com saÃ­da kanban |

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

## Arquitetura

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

Todo o estado fica em `~/.agentteam/` como arquivos JSON. Sem banco de dados, sem servidor. Escritas atÃ´micas com travamento de arquivos `fcntl` garantem seguranÃ§a contra falhas.

| ConfiguraÃ§Ã£o | VariÃ¡vel de ambiente | PadrÃ£o |
|---------|---------|---------|
| DiretÃ³rio de dados | `AgentTeam_DATA_DIR` | `~/.agentteam` |
| Transporte | `AgentTeam_TRANSPORT` | `file` |
| Modo de workspace | `AgentTeam_WORKSPACE` | `auto` |
| Backend de spawn | `AgentTeam_DEFAULT_BACKEND` | `tmux` |

---

## ReferÃªncia de comandos

<details open>
<summary><strong>Comandos principais</strong></summary>

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
<summary><strong>Workspace, plano, ciclo de vida, configuraÃ§Ã£o</strong></summary>

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

## AtribuiÃ§Ã£o de modelo por agente (PrÃ©via)

> **Branch:** [`feat/per-agent-model-assignment`](https://github.com/win4r/AgentTeam-OpenClaw/tree/feat/per-agent-model-assignment)
>
> Esta funcionalidade estÃ¡ disponÃ­vel para testes antecipados em uma branch separada. SerÃ¡ mesclada na `main` assim que a flag `--model` complementar do OpenClaw for lanÃ§ada.

Atribua modelos diferentes a papÃ©is de agentes diferentes para melhores compensaÃ§Ãµes de custo/desempenho em enxames multi-agente.

```bash
# Install from the feature branch
pip install -e "git+https://github.com/win4r/AgentTeam-OpenClaw.git@feat/per-agent-model-assignment#egg=agentteam"
```

**Modelo por agente em templates:**
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

**Flags de CLI:**
```bash
agentteam spawn --model opus                          # single agent
agentteam launch my-template --model gpt-5.4          # override all agents
agentteam launch my-template --model-strategy auto     # auto-assign by role
```

Veja a [issue #1](https://github.com/win4r/AgentTeam-OpenClaw/issues/1) para a solicitaÃ§Ã£o completa da funcionalidade e discussÃ£o.

---

## Roteiro

| VersÃ£o | O quÃª | Status |
|---------|------|--------|
| v0.3 | Transporte por arquivo + P2P, Interface Web, multi-usuÃ¡rio, templates | LanÃ§ado |
| v0.4 | Transporte Redis â?mensagens entre mÃ¡quinas | Planejado |
| v0.5 | Camada de estado compartilhado â?configuraÃ§Ã£o de equipe entre mÃ¡quinas | Planejado |
| v0.6 | Marketplace de agentes â?templates da comunidade | Em exploraÃ§Ã£o |
| v0.7 | Agendamento adaptativo â?reatribuiÃ§Ã£o dinÃ¢mica de tarefas | Em exploraÃ§Ã£o |
| v1.0 | Grau de produÃ§Ã£o â?autenticaÃ§Ã£o, permissÃµes, logs de auditoria | Em exploraÃ§Ã£o |

---

## Contribuindo

ContribuiÃ§Ãµes sÃ£o bem-vindas:

- **IntegraÃ§Ãµes de agentes** â?suporte para mais agentes CLI
- **Templates de equipe** â?templates TOML para novos domÃ­nios
- **Backends de transporte** â?Redis, NATS, etc.
- **Melhorias no painel** â?Interface Web, Grafana
- **DocumentaÃ§Ã£o** â?tutoriais e boas prÃ¡ticas

---

## Agradecimentos

- [@karpathy/autoresearch](https://github.com/karpathy/autoresearch) â?framework de pesquisa autÃ´noma de ML
- [OpenClaw](https://openclaw.ai) â?backend de agente padrÃ£o
- [Claude Code](https://claude.ai/claude-code) e [Codex](https://openai.com/codex) â?agentes de codificaÃ§Ã£o com IA suportados
- [ai-hedge-fund](https://github.com/virattt/ai-hedge-fund) â?inspiraÃ§Ã£o para o template de fundo de investimento
- [CLI-Anything](https://github.com/HKUDS/CLI-Anything) â?projeto irmÃ£o

## LicenÃ§a

MIT â?livre para uso, modificaÃ§Ã£o e distribuiÃ§Ã£o.

---

<div align="center">

**AgentTeam** â?*InteligÃªncia de enxame de agentes.*

</div>
