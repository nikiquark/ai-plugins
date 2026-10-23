---
title: "ansible-conventions"
---

Соглашения по деплою и харденингу через Ansible: структура в репозитории, inventories, vault, идемпотентные роли, атомарные релизы с откатом, базовая роль харденинга, порядок «сначала check и diff».

| | |
|---|---|
| Вызов | `/web-pipeline:ansible-conventions` или автоматически при работе с деплоем и серверами |
| Предзагружен в | [architect](../agents/architect.md), [security-reviewer](../agents/security-reviewer.md), [ops-auditor](../agents/ops-auditor.md) |
| Используют | [`deploy`](../commands/deploy.md), [`secure-maintain`](../commands/secure-maintain.md) |
| Исходник | `plugins/web-pipeline/skills/ansible-conventions/SKILL.md` |

## Когда срабатывает

> Conventions for deploying and hardening this user's web projects with Ansible - repo layout, inventories, vault, idempotent roles, atomic releases with rollback, base hardening role, check/diff-first workflow. Load when writing deploy code, deploying or changing servers.

## Структура

```text
deploy/ansible/
  ansible.cfg
  requirements.yml                # закреплённые коллекции и роли
  inventories/
    staging/hosts.yml
    staging/group_vars/all/{vars.yml,vault.yml}
    production/hosts.yml
    production/group_vars/all/{vars.yml,vault.yml}
  roles/
    base/                         # харденинг: пользователи, ssh, ufw, fail2ban, unattended-upgrades, время
    app/                          # рантайм приложения, каталоги релизов, systemd или compose
    proxy/                        # nginx/caddy, TLS, заголовки безопасности
    db/                           # только при собственном хостинге БД
    backup/
  playbooks/
    site.yml                      # полная конвергенция (base + все роли)
    deploy.yml                    # только релиз приложения
    rollback.yml                  # переключение на предыдущий релиз
    smoke.yml                     # health-проверки с управляющего хоста
```

## Правила

- **Любое изменение сервера — через роль.** Никаких ручных исправлений по SSH. Исправление, сделанное вручную, сразу переносится в роль.
- **Идемпотентность:** повторный запуск даёт `changed=0`. Модули лучше `shell` и `command`. Если `shell` неизбежен — `creates:`/`removes:` или `changed_when:`.
- **Сначала check:** `ansible-playbook … --check --diff` перед каждым реальным запуском, и вы видите diff. [Guard-хук](../hooks.md#guard-bash) запрашивает подтверждение на любой запуск без `--check`.
- **Секреты** в `vault.yml`, зашифрованы `ansible-vault`, используются как переменные `vault_*` из `vars.yml`. Содержимое vault не печатается, пароль vault не передаётся в командной строке: `--vault-password-file` вне репозитория или `--ask-vault-pass`.
- **Версии закреплены:** коллекции в `requirements.yml`, пакеты, где важно, образы — по тегу и digest.
- `ansible-lint` в `make check` (профиль production).
- Теги для частичных запусков (`--tags app`), handlers для перезапусков, `serial` и `until:` с health-check для нескольких хостов.
- Только хосты из inventory этого проекта.

## Атомарные релизы и откат

```text
/srv/<app>/releases/<timestamp>-<gitsha>/
/srv/<app>/shared/        # .env, загрузки, постоянное состояние
/srv/<app>/current -> releases/<…>
```

`deploy.yml`:

1. выкладывает или собирает новый каталог релиза;
2. подключает `shared/`;
3. запускает миграции (только вперёд);
4. атомарно переключает `current`;
5. перезапускает через handler;
6. ждёт `/readyz`;
7. хранит последние 5 релизов.

`rollback.yml` возвращает `current` на предыдущий релиз и перезапускает. Необратимая миграция должна быть отмечена до деплоя.

Для контейнеров аналог — стек `docker compose` с закреплёнными на релиз тегами образов и записанным предыдущим тегом для отката.

## Роль base (харденинг)

- Отдельный пользователь для деплоя, SSH только по ключу. `PasswordAuthentication` и `PermitRootLogin` выключены.
- `ufw` разрешает только 22 (или свой порт SSH), 80 и 443.
- `fail2ban` защищает sshd.
- `unattended-upgrades` ставит обновления безопасности, с автоматической перезагрузкой в заданное окно, если вы разрешите.
- `chrony` для времени, `logrotate`, swap-файл при нехватке памяти.
- TLS через certbot или Caddy, автопродление проверяется таймером.
- Прокси отдаёт заголовки безопасности: HSTS, CSP, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, frame-ancestors.
- У роли прокси есть переменная `proxy_noindex`. Когда она `true`, каждый ответ получает `X-Robots-Tag: noindex, nofollow`. В `inventories/staging/group_vars/all/vars.yml` она `true`, в production — `false`, если приложение не закрытое ([`seo-standards`](seo-standards.md)).
- Прокси редиректит http на https и неканонический хост на канонический через 301.
