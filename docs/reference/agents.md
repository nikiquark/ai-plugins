# Все агенты

| Агент | Модель | Effort | `maxTurns` | Инструменты | Навыки | Вызывается из | Префикс |
|---|---|---|---|---|---|---|---|
| [content-strategist](../web-pipeline/agents/content-strategist.md) | opus | high | — | Read, Grep, Glob, Write, Edit, WebSearch, WebFetch, Skill | seo-standards | new-project, change | — |
| [architect](../web-pipeline/agents/architect.md) | opus | high | — | Read, Grep, Glob, Bash, Write, Edit, WebSearch, WebFetch, Skill | backend-standards, ansible-conventions, seo-standards, reuse-first | new-project, change | — |
| [designer](../web-pipeline/agents/designer.md) | opus | high | — | Read, Grep, Glob, Bash, Write, Edit, WebSearch, WebFetch, Skill | frontend-style | new-project, change | — |
| [backend-dev](../web-pipeline/agents/backend-dev.md) | sonnet | medium | — | все | backend-standards, testing-standards, reuse-first | D1–D4 | — |
| [frontend-dev](../web-pipeline/agents/frontend-dev.md) | sonnet | high | — | все | frontend-style, seo-standards, testing-standards, reuse-first | D1, D3, D4 | — |
| [qa-engineer](../web-pipeline/agents/qa-engineer.md) | sonnet | medium | — | все | testing-standards | D3, D4 | — |
| [code-reviewer](../web-pipeline/agents/code-reviewer.md) | opus | high | 40 | все, кроме Write, Edit, NotebookEdit, Agent | backend-standards, testing-standards, reuse-first | review-loop | `CR-` |
| [security-reviewer](../web-pipeline/agents/security-reviewer.md) | opus | high | 40 | все, кроме Write, Edit, NotebookEdit, Agent | backend-standards, ansible-conventions | review-loop, secure-maintain | `SEC-` |
| [design-critic](../web-pipeline/agents/design-critic.md) | opus | medium | 40 | все, кроме Write, Edit, NotebookEdit, Agent | frontend-style, seo-standards | review-loop (если менялся UI) | `DES-` |
| [ops-auditor](../web-pipeline/agents/ops-auditor.md) | haiku | medium | 60 | все, кроме Write, Edit, NotebookEdit, Agent | ansible-conventions | secure-maintain | — |

Stop-gate запускает `make check` при `SubagentStop` только для `backend-dev`, `frontend-dev` и `qa-engineer` ([Хуки](../web-pipeline/hooks.md#stop-gate)).
