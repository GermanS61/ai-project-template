# CONTRIBUTING

## Ветки

Не вносите функциональные изменения напрямую в `main`.

Рекомендуемые имена:

```text
feature/<task>
fix/<task>
docs/<task>
refactor/<task>
codex/<task>
```

## Commits

Используйте короткие осмысленные сообщения в стиле Conventional Commits:

```text
feat: add threads health check
fix: handle expired token
docs: document vps diagnostics
test: cover response parser
refactor: split policy checks
chore: add env example
```

Один commit — одна логическая группа изменений. Не смешивайте независимые темы.

## Pull Request

Одна законченная задача — один PR. PR должен быть понятен разработчику, который впервые видит изменение.

Перед PR:

- проверьте diff/status;
- исключите собственные scratch/debug-файлы из PR; не удаляйте неизвестные или чужие файлы без подтверждения владельца;
- запустите релевантные tests/lint/typecheck/pre-commit;
- выполните smoke-test при необходимости;
- обновите документацию;
- укажите, если какую-либо проверку выполнить невозможно.

## Scope

Не исправляйте несвязанные проблемы в текущем PR. Создайте отдельный Issue.

Не реализуйте Feature Request только потому, что он существует. Он должен быть утверждён или явно включён в текущую задачу.

Создание или изменение GitHub Issues/PR и других внешних сущностей требует явного разрешения текущей задачи. При read-only запросе подготовьте черновик вместо публикации.

## Review

Ревьюер проверяет:

- соответствие задаче и acceptance criteria;
- архитектурную консистентность;
- читаемость и простоту;
- backward compatibility;
- тесты и граничные случаи;
- документацию;
- безопасность и секреты;
- отсутствие scope creep.

Подробный checklist: [docs/review-checklist.md](docs/review-checklist.md).
