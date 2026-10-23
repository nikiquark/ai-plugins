# new-project

Новый веб-проект от идеи до локальной проверки: интервью, архитектура, дизайн-концепты, реализация с контрактом в начале, проверки качества, ограниченное ревью.

| | |
|---|---|
| Вызов | `/web-pipeline:new-project [идея в нескольких словах]` |
| Автовызов | Нет (`disable-model-invocation: true`), только вручную |
| Точки решения | Подтверждение интервью, GATE 1 (архитектура), GATE 2 (дизайн), D5 (локальная проверка) |
| Состояние | `.claude/state/pipeline.json` с `"flow": "new-project"` |
| Исходник | `plugins/web-pipeline/skills/new-project/SKILL.md` |

Пошаговый пример есть на странице [Первый проект](../../getting-started/first-project.md).

## Этапы

```mermaid
flowchart TB
  R{pipeline.json есть?} -- да --> RES[Продолжить с сохранённой фазы]
  R -- нет --> P0
  P0[0. Bootstrap: git init, init, pipeline.json] --> P1
  P1[1. grill-me → docs/spec.md] --> P2
  P2[2. architect → architecture.md, adr/, plan.md] --> G1{{✋ GATE 1}}
  G1 -- изменения --> P2
  G1 -- утверждено --> P3[3. designer → 3 концепта в docs/design/concepts/]
  P3 --> G2{{✋ GATE 2}}
  G2 -- новый раунд --> P3
  G2 -- выбран --> DS[designer → docs/design.md]
  DS --> SNAP[git-snapshot → implementation_base]
  SNAP --> D[D1 → D2 → D3 → D4 → D5 ✋]
```

### Resume first

Если `.claude/state/pipeline.json` существует, оркестратор говорит, на какой фазе остановился прошлый запуск, и продолжает с неё. Подробнее на странице [Состояние и возобновление](../../concepts/state.md).

### Фаза 0. Bootstrap

1. `git init` (ветка `main`), если папка ещё не репозиторий.
2. Скилл [`init`](init.md): `.claude/web-pipeline.json`, anti-slop, папка состояния, раздел в `CLAUDE.md`. Стек на этом этапе неизвестен, поэтому записывается `TBD`.
3. `.claude/state/pipeline.json`: `{ "flow": "new-project", "phase": "requirements" }`.

### Фаза 1. Требования

[`dev-core:grill-me`](../../dev-core/skills/grill-me.md) по идее. Результат пишется в `docs/spec.md` по [шаблону spec.md](../templates.md#specmd).

Дерево решений обязательно покрывает:

- пользователей и задачу, ради которой они придут;
- user stories с **проверяемыми критериями приёмки**;
- что не входит в проект;
- данные и их чувствительность (персональные данные, платежи);
- интеграции, модель авторизации, ожидаемую нагрузку;
- языки и локали, SEO;
- хостинг (ваши серверы через Ansible) и бюджет на платные сервисы;
- визуальное настроение: ссылки на то, что нравится и не нравится, а не прилагательные.

### Фаза 2. Архитектура → GATE 1

[`architect`](../agents/architect.md) получает путь к `docs/spec.md` и пишет `docs/architecture.md`, `docs/adr/NNNN-*.md` и `docs/plan.md`.

Вам показывают стек с причинами, таблицу «готовое или своё», главные риски, число задач и отвергнутые варианты. **GATE 1**: явное утверждение или изменения. При изменениях architect перерабатывает документы с учётом ваших замечаний. После утверждения стек записывается в `.claude/web-pipeline.json` и `CLAUDE.md`.

### Фаза 3. Дизайн-концепты → GATE 2

[`designer`](../agents/designer.md) получает пути к спецификации и архитектуре и делает 3 намеренно разных концепта в `docs/design/concepts/` (самостоятельные HTML). К каждому прилагается описание: название, одна смелая идея, палитра, пара шрифтов, компромиссы.

**GATE 2**: вы открываете файлы в браузере и выбираете один, смешиваете («шрифты из A, сетка из C») или просите новый раунд. После выбора designer пишет `docs/design.md`: токены, шкалу шрифтов, правила раскладки, движение, перечень компонентов.

### Фаза 4 и дальше. Реализация

Дерево фиксируется [`git-snapshot`](../../dev-core/git-snapshot.md), хэш сохраняется как `implementation_base`. Затем выполняются фазы [D1–D5](../delivery.md) из `shared/delivery-phases.md`. D5 — финальная точка решения.

## Кто задействован

| Этап | Агенты и скиллы |
|---|---|
| 0 | [`init`](init.md) |
| 1 | [`dev-core:grill-me`](../../dev-core/skills/grill-me.md) |
| 2 | [architect](../agents/architect.md) |
| 3 | [designer](../agents/designer.md) |
| D1–D3 | [backend-dev](../agents/backend-dev.md), [frontend-dev](../agents/frontend-dev.md), [qa-engineer](../agents/qa-engineer.md) |
| D4 | [`dev-core:review-loop`](../../dev-core/skills/review-loop.md) с [code-reviewer](../agents/code-reviewer.md), [security-reviewer](../agents/security-reviewer.md), [design-critic](../agents/design-critic.md) |

## Какие файлы создаёт

`docs/spec.md`, `docs/architecture.md`, `docs/adr/`, `docs/plan.md`, `docs/design/concepts/*.html`, `docs/design.md`, `TODO.md`, код приложения, `Makefile`, тесты, а также всё, что создаёт [`init`](init.md). Полный список на странице [Файлы в проекте](../project-files.md).

## Язык

Оркестратор общается с вами на вашем языке. Документы в `docs/` тоже пишутся на вашем языке, если вы не попросите иначе.

## Типичные проблемы

- **Хочу начать заново, а он продолжает старый запуск.** Удалите `.claude/state/pipeline.json`.
- **Концепты получились похожими.** Попросите новый раунд на GATE 2 и прямо назовите, что не понравилось. Designer обязан делать концепты намеренно разными.
- **`make check` красный из-за отсутствующего инструмента.** Установите его по подсказке из вывода ([Зависимости](../../getting-started/requirements.md)).
