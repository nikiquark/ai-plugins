# Шаблоны

Шаблоны лежат в `plugins/web-pipeline/templates/`. Скиллы обращаются к ним через `${CLAUDE_PLUGIN_ROOT}/templates/…`.

| Файл | Кто использует | Куда попадает |
|---|---|---|
| [`spec.md`](#specmd) | [`new-project`](commands/new-project.md) → grill-me | `docs/spec.md` |
| [`change.md`](#changemd) | [`change`](commands/change.md) → grill-me, architect | `docs/changes/NNNN-<slug>.md` |
| [`web-pipeline.json`](configuration.md) | [`init`](commands/init.md) | `.claude/web-pipeline.json` |
| [`claude-md-section.md`](#claude-md-sectionmd) | [`init`](commands/init.md) | Раздел в `CLAUDE.md` проекта |
| [`anti_slop.py`](anti-slop.md) | [`init`](commands/init.md) | `scripts/anti_slop.py` |

## spec.md

Спецификация нового проекта. Её заполняет [grill-me](../dev-core/skills/grill-me.md) после подтверждения общего понимания.

| Раздел | Содержимое |
|---|---|
| Статус | draft или approved, дата |
| 1. Problem and purpose | Какую проблему решает, для кого и почему сейчас. Один абзац |
| 2. Users | Таблица: персона · задача, ради которой придут · контекст (устройство, частота, навык) |
| 3. User stories and acceptance criteria | `US-n` с критериями `AC-n.m` в форме Given / when / then. Каждый критерий проверяем: QA может написать по нему e2e без вопросов |
| 4. Non-goals | Что точно не будет сделано в этой версии |
| 5. Data | Сущности, владение, хранение, чувствительность; применимы ли GDPR или 152-ФЗ |
| 6. Integrations | Внешние сервисы, API, платёжные провайдеры, почта и SMS, их лимиты и стоимость |
| 7. Auth and roles | Кто что может, способы входа |
| 8. Non-functional requirements | Нагрузка, бюджет производительности, доступность, локали, уровень доступности (WCAG 2.2 AA по умолчанию), SEO, браузеры |
| 9. Hosting and operations | Серверы (inventory Ansible), окружения, домены, бэкапы, мониторинг |
| 10. Visual mood | Референсы, которые нравятся и не нравятся, со ссылками и причинами; ваши слова; жёсткие запреты |
| 11. Open questions | Сознательно не решённое, с ответственным |

Id критериев (`AC-1.2`) сквозные: по ним architect привязывает задачи плана, а qa-engineer называет тесты.

## change.md

Документ изменения существующего проекта. Разделы 1–4 заполняются по итогам интервью, 5–7 дописывает [architect](agents/architect.md).

| Раздел | Содержимое |
|---|---|
| Статус | draft, approved или done, ветка `change/<slug>`, дата |
| 1. What and why | Текущее поведение → желаемое. Кто попросил и зачем |
| 2. Acceptance criteria | `AC-n` в форме Given / when / then |
| 3. Must not change | Поведение, URL, поля API и данные, которые должны остаться прежними. Каждый пункт получает характеризационный тест до изменения кода |
| 4. Compatibility and rollout | Миграции, потребители API, URL и SEO, feature flag, план отката |
| 5. Impact analysis | Таблица: модуль или файл · изменение · риск |
| 6. Build vs reuse | Таблица: потребность · есть в проекте · библиотека или встроенное · решение |
| 7. Plan | Задачи `T1…` с критериями готовности |
| 8. Open questions | Открытые вопросы |

## claude-md-section.md

Раздел «Web pipeline», который [init](commands/init.md) добавляет в `CLAUDE.md` проекта. Он сообщает любой сессии Claude Code в этом проекте:

- что проект использует плагин и хуки включены через `.claude/web-pipeline.json`;
- стек, как запустить локально (`make dev` → URL);
- что `make check` — обязательная проверка качества и что она включает;
- где лежат документы: `docs/spec.md`, `architecture.md`, `adr/`, `design.md`, `plan.md`, `changes/`;
- что деплой идёт через `deploy/ansible/` и `/web-pipeline:deploy <env>`, а `ansible-playbook` без `--check` вне этой команды не запускается.

И правила: `dev-core:reuse-first` и `reuse:`-заметка перед новым модулем; фронтенд по `frontend-style` и `docs/design.md` с проходящим `anti_slop.py`; бэкенд по `backend-standards`, тесты по `testing-standards`.

Благодаря этому разделу правила действуют и в обычной сессии без запуска оркестратора.
